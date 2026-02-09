from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import cv2, os, numpy as np
from datetime import datetime
import uuid 

app = Flask(__name__)
app.secret_key = "artify_industrial_secret_key"

# Database & File Config
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "artify_ai.db")
app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "static/uploads")

db = SQLAlchemy(app)

# --- Database Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    history = db.relationship('ImageHistory', backref='owner', lazy=True)
    transactions = db.relationship('Transaction', backref='payer', lazy=True)

class ImageHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(200))
    style = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_id = db.Column(db.String(100), unique=True)
    payment_id = db.Column(db.String(100))
    amount = db.Column(db.Integer)
    status = db.Column(db.String(20)) # Success/Failed
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    db.create_all()

# --- ALGORITHMS ---

def apply_cartoon(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 7)
    edges = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
    color = cv2.bilateralFilter(img, 9, 250, 250)
    return cv2.bitwise_and(color, color, mask=edges)

def apply_sketch(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv, (21, 21), 0)
    return cv2.divide(gray, 255 - blur, scale=256)

def apply_pencil_color(img):
    sketch = apply_sketch(img)
    sketch_3ch = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)
    return cv2.multiply(img, sketch_3ch, scale=1/256)

def apply_anime_ghibli(img):
    # 1. Edge Enhancement (Keep lines crisp)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
    # 2. Color Smoothing (Flat anime look)
    color = cv2.bilateralFilter(img, 9, 300, 300)
    # 3. Vibrancy Boost (Ghibli style saturation)
    hsv = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s = cv2.add(s, 50) # Boost saturation
    v = cv2.add(v, 20) # Boost brightness
    vibrant = cv2.cvtColor(cv2.merge([h, s, v]), cv2.COLOR_HSV2BGR)
    # 4. Combine
    return cv2.bitwise_and(vibrant, vibrant, mask=edges)

def apply_cyberpunk(img):
    # 1. High Contrast using CLAHE
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    # 2. Color Shift (Cool Tones)
    a = cv2.add(a, 10) # Shift Green-Red
    b = cv2.subtract(b, 20) # Shift Blue-Yellow (More Blue)
    result = cv2.cvtColor(cv2.merge((cl, a, b)), cv2.COLOR_LAB2BGR)
    return result

def apply_hdr(img):
    return cv2.detailEnhance(img, sigma_s=12, sigma_r=0.15)

# --- ROUTES ---
@app.route("/")
def index():
    is_pro = False
    if "user_id" in session:
        if Transaction.query.filter_by(user_id=session["user_id"], status="Success").first(): is_pro = True

    uses_left = "Unlimited (Pro)" if is_pro else (3 - session.get("guest_uses", 0))
    history = []
    if "user_id" in session:
        history = ImageHistory.query.filter_by(user_id=session["user_id"]).order_by(ImageHistory.timestamp.desc()).all()
    
    return render_template("index.html", logged_in="user_id" in session, username=session.get("username"), uses_left=uses_left, history=history, is_pro=is_pro)

@app.route("/process", methods=["POST"])
def process():
    is_pro = False
    if "user_id" in session:
        if Transaction.query.filter_by(user_id=session["user_id"], status="Success").first(): is_pro = True

    if not is_pro:
        current = session.get("guest_uses", 0)
        if current >= 3: return jsonify({"auth_required": True, "message": "Trial ended. Upgrade to Pro."})
        session["guest_uses"] = current + 1

    file = request.files["file"]
    style = request.form.get("style", "cartoon")
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # ALGORITHM SWITCH
    if style == 'pencil': result = apply_sketch(img)
    elif style == 'pencil_color': result = apply_pencil_color(img)
    elif style == 'anime': result = apply_anime_ghibli(img)
    elif style == 'cyberpunk': result = apply_cyberpunk(img)
    elif style == 'hdr': result = apply_hdr(img)
    else: result = apply_cartoon(img)
    
    name = f"proc_{datetime.now().timestamp()}.png"
    cv2.imwrite(os.path.join(app.config["UPLOAD_FOLDER"], name), result)

    if "user_id" in session:
        db.session.add(ImageHistory(user_id=session["user_id"], filename=name, style=style))
        db.session.commit()

    return jsonify({"image": url_for("static", filename="uploads/"+name), "uses_left": "Unlimited" if is_pro else (3 - session.get("guest_uses", 0))})

@app.route("/mock_payment", methods=["POST"])
def mock_payment():
    if "user_id" not in session: return jsonify({"success": False})
    new_txn = Transaction(
        user_id=session["user_id"], order_id=f"order_{uuid.uuid4().hex[:8]}",
        payment_id=f"pay_{uuid.uuid4().hex[:8]}", amount=5000, status="Success"
    )
    db.session.add(new_txn)
    db.session.commit()
    return jsonify({"success": True})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get("username")).first()
    if user and check_password_hash(user.password, data.get("password")):
        session["user_id"] = user.id
        session["username"] = user.username
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Invalid credentials"})

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    if User.query.filter_by(username=data.get("username")).first():
        return jsonify({"success": False, "message": "Username taken"})
    user = User(username=data.get("username"), password=generate_password_hash(data.get("password")))
    db.session.add(user)
    db.session.commit()
    session["user_id"] = user.id
    session["username"] = user.username
    return jsonify({"success": True})

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/delete_history", methods=["POST"])
def delete_history():
    if "user_id" not in session: return jsonify({"success": False})
    item = ImageHistory.query.get(request.json.get("id"))
    if item and item.user_id == session["user_id"]:
        try: os.remove(os.path.join(app.config["UPLOAD_FOLDER"], item.filename))
        except: pass
        db.session.delete(item)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False})

if __name__ == "__main__":
    app.run(debug=True)