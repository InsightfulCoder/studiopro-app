import os
import datetime
import io
import base64
import requests
import numpy as np
import cv2
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import cloudinary
import cloudinary.uploader

app = Flask(__name__)
app.secret_key = "studiopro_pro_secret_key"

# --- 1. CONFIGURATION ---

# 🧠 BRAIN: Hugging Face (Model: OpenJourney - High Quality & Ungated)
HUGGINGFACE_API_KEY = "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"

# ☁️ STORAGE: Cloudinary
# ⚠️ PASTE YOUR CLOUDINARY KEYS HERE ⚠️
cloudinary.config(
    cloud_name = "dhococ8e5",
    api_key = "457977599793717",    
    api_secret = "uPtdj1lgu-HvQ2vnmHCgDk1QHu0" 
)

# 🗄️ DATABASE: Neon
db_url = "postgresql://neondb_owner:npg_JXnas5ev8AgG@ep-crimson-wind-aillfxxy-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# --- 2. AI FUNCTIONS ---

def apply_local_backup(img_bytes, style):
    """Fallback: Runs if AI is down. Uses OpenCV filters."""
    # Decode image
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if style == 'pencil':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        inv = 255 - gray
        blur = cv2.GaussianBlur(inv, (21, 21), 0)
        sketch = cv2.divide(gray, 255 - blur, scale=256.0)
        result = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)
    elif style == 'cyberpunk':
        # Blue/Purple tint
        img_float = img.astype(np.float32) / 255.0
        b, g, r = cv2.split(img_float)
        b = np.clip(b * 1.3, 0, 1)
        g = np.clip(g * 0.8, 0, 1)
        result = (cv2.merge([b, g, r]) * 255).astype(np.uint8)
    else:
        # Cartoon
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(img, 9, 250, 250)
        result = cv2.bitwise_and(color, color, mask=edges)

    success, buffer = cv2.imencode('.png', result)
    return buffer.tobytes()

def query_huggingface(file_stream, prompt, style):
    # Model: OpenJourney (Midjourney style, usually ungated)
    API_URL = "https://router.huggingface.co/models/prompthero/openjourney"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    
    # Read file safely
    file_stream.seek(0)
    original_bytes = file_stream.read()
    b64_img = base64.b64encode(original_bytes).decode('utf-8')
    
    # Note: OpenJourney is primarily Text-to-Image. 
    # For Image-to-Image via API, we use a trick or fallback to the backup if strictly needed.
    # But let's try to send it as input.
    
    payload = {
        "inputs": b64_img,
        "parameters": {
            "prompt": "mdjrny-v4 style " + prompt, # Trigger word for this model
            "strength": 0.65,
            "guidance_scale": 7.5
        }
    }
    
    try:
        print("Attempting AI generation...")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=25)
        
        # If AI works, return AI image
        if response.status_code == 200:
            return response.content
            
        print(f"AI Failed ({response.status_code}). Switching to Backup.")
        # If AI fails (404, 503, 500), Fallback to Local
        return apply_local_backup(original_bytes, style)
        
    except Exception as e:
        print(f"Connection Error: {e}. Switching to Backup.")
        # If connection fails, Fallback to Local
        return apply_local_backup(original_bytes, style)

# --- 3. DATABASE MODELS ---
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    history = db.relationship('ImageHistory', backref='owner', lazy=True)

class ImageHistory(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    style = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

with app.app_context():
    db.create_all()

# --- 4. ROUTES ---
@app.route("/")
def index():
    history = []
    if "user_id" in session:
        history = ImageHistory.query.filter_by(user_id=session["user_id"]).order_by(ImageHistory.timestamp.desc()).all()
    return render_template("index.html", logged_in="user_id" in session, username=session.get("username"), history=history)

@app.route("/process", methods=["POST"])
def process():
    if "user_id" not in session:
        return jsonify({"auth_required": True, "message": "Please login to generate assets."})

    file = request.files.get("file")
    style = request.form.get("style", "cartoon")
    
    if not file: return jsonify({"error": "No file uploaded"}), 400

    try:
        # Define AI Prompts
        prompt_text = "cartoon illustration, vibrant"
        if style == 'cyberpunk': prompt_text = "cyberpunk city, neon lights, futuristic, highly detailed"
        elif style == 'anime': prompt_text = "studio ghibli anime style, masterpiece"
        elif style == 'pencil': prompt_text = "pencil sketch, architectural drawing, black and white"
        elif style == 'hdr': prompt_text = "hdr photography, realistic, 8k resolution"

        # 1. GENERATE (AI with Local Backup)
        final_image_bytes = query_huggingface(file, prompt_text, style)

        # 2. Upload to Cloudinary
        upload_res = cloudinary.uploader.upload(io.BytesIO(final_image_bytes), resource_type="image")
        permanent_url = upload_res['secure_url']

        # 3. Save to Database
        new_entry = ImageHistory(
            user_id=session["user_id"],
            image_url=permanent_url,
            style=style
        )
        db.session.add(new_entry)
        db.session.commit()

        return jsonify({
            "image": permanent_url,
            "id": new_entry.id,
            "style": style
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    if User.query.filter_by(username=data.get("username")).first():
        return jsonify({"success": False, "message": "Username taken"})
    new_user = User(username=data.get("username"), password=generate_password_hash(data.get("password")))
    db.session.add(new_user)
    db.session.commit()
    session["user_id"] = new_user.id
    session["username"] = new_user.username
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

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/delete_history", methods=["POST"])
def delete_history():
    if "user_id" not in session: return jsonify({"success": False})
    data = request.json
    item = ImageHistory.query.get(data.get("id"))
    if item and item.user_id == session["user_id"]:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False})
    
@app.route("/mock_payment", methods=["POST"])
def mock_payment():
    return jsonify({"success": True}) 

if __name__ == "__main__":
    app.run(debug=True)
