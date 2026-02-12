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
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import cloudinary
import cloudinary.uploader

app = Flask(__name__)
app.secret_key = "studiopro_pro_secret_key"

# --- 1. SECURE CONFIGURATION ---
# This looks for the key inside Render's "Environment" tab
HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")

# ⚠️ YOUR CLOUDINARY KEYS (Preserved from your code) ⚠️
cloudinary.config(
    cloud_name = "dhococ8e5",
    api_key = "457977599793717",    
    api_secret = "uPtdj1lgu-HvQ2vnmHCgDk1QHu0" 
)

# Database Config
db_url = "postgresql://neondb_owner:npg_JXnas5ev8AgG@ep-crimson-wind-aillfxxy-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"
if db_url.startswith("postgres://"): db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

# --- DATABASE MODELS ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    wallet = db.Column(db.Integer, default=0)
    history = db.relationship('ImageHistory', backref='owner', lazy=True)

class ImageHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    image_url = db.Column(db.String(500))
    style = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Integer)
    status = db.Column(db.String(50))
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- AI PROCESSING ---
def local_filter(img_bytes, style):
    # Runs if AI fails
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Safety check if image is invalid
    if img is None: return b''

    h, w = img.shape[:2]
    if w > 800: img = cv2.resize(img, (800, int(h * (800/w))))

    if style == 'pencil':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        inv = 255 - gray
        blur = cv2.GaussianBlur(inv, (21, 21), 0)
        sketch = cv2.divide(gray, 255 - blur, scale=256.0)
        res = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)
    else:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        s = cv2.add(s, 50) 
        res = cv2.cvtColor(cv2.merge((h, s, v)), cv2.COLOR_HSV2BGR)

    success, buffer = cv2.imencode('.png', res)
    return buffer.tobytes()

def process_ai(file, style):
    # FIX: Read file ONCE safely
    file.seek(0)
    file_bytes = file.read()

    # 1. Check if Key exists
    if not HUGGINGFACE_API_KEY:
        print("❌ API Key missing. Using Backup.")
        return local_filter(file_bytes, style)

    # 2. Prepare AI Request
    prompt_map = {
        'cartoon': "cartoon style, vector art, flat color, high quality", 
        'pencil': "pencil sketch, graphite, monochrome, detailed", 
        'anime': "anime style, studio ghibli, vibrant, masterpiece, 8k", 
        'cyberpunk': "cyberpunk city, neon lights, futuristic, 8k"
    }
    
    API_URL = "https://router.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    
    b64_img = base64.b64encode(file_bytes).decode('utf-8')
    
    payload = {
        "inputs": b64_img,
        "parameters": {
            "prompt": prompt_map.get(style, "illustration"),
            "strength": 0.75, 
            "guidance_scale": 7.5
        }
    }
    
    try:
        # 3. Call AI
        response = requests.post(API_URL, headers=headers, json=payload, timeout=25)
        
        if response.status_code == 200:
            return response.content
        else:
            print(f"AI Error: {response.text}")
            
    except Exception as e:
        print(f"Connection Error: {e}")
        
    # 4. Fallback (Uses the safe file_bytes we read earlier)
    return local_filter(file_bytes, style)

# --- ROUTES ---
@app.route('/')
def index():
    if current_user.is_authenticated:
        history = ImageHistory.query.filter_by(user_id=current_user.id).order_by(ImageHistory.timestamp.desc()).all()
        return render_template('index.html', user=current_user, history=history)
    return render_template('index.html', user=None)

@app.route('/process', methods=['POST'])
def process():
    # Guest Logic
    if not current_user.is_authenticated:
        if 'guest_count' not in session: session['guest_count'] = 0   
        if session['guest_count'] >= 3:
            return jsonify({"auth_required": True, "error": "Free Limit Reached (3/3). Please Login!"})
        
        session['guest_count'] += 1
        current_wallet = f"Guest ({3 - session['guest_count']} left)"
    else:
        if current_user.wallet < 10: return jsonify({"error": "Insufficient Funds! Add Coins."})
        current_wallet = current_user.wallet - 10

    file = request.files.get('file')
    style = request.form.get('style')
    
    # Process
    img_bytes = process_ai(file, style)
    
    # Upload
    upload = cloudinary.uploader.upload(io.BytesIO(img_bytes), resource_type="image")
    
    # Save & Charge
    if current_user.is_authenticated:
        current_user.wallet -= 10
        new_entry = ImageHistory(user_id=current_user.id, image_url=upload['secure_url'], style=style)
        db.session.add(new_entry)
        db.session.commit()
        current_wallet = current_user.wallet

    return jsonify({"image": upload['secure_url'], "wallet": current_wallet, "message": "Success"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get('username')).first()
    if user and check_password_hash(user.password, data.get('password')):
        login_user(user)
        session.pop('guest_count', None)
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Invalid credentials"})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({"success": False, "message": "Username taken"})
    is_admin = (data.get('username').lower() == 'admin')
    user = User(username=data.get('username'), password=generate_password_hash(data.get('password')), is_admin=is_admin, wallet=0)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    session.pop('guest_count', None)
    return jsonify({"success": True})

@app.route('/pay', methods=['POST'])
@login_required
def pay():
    amount = int(request.json.get('amount'))
    current_user.wallet += amount
    trans = Transaction(user_id=current_user.id, amount=amount, status="Success")
    db.session.add(trans)
    db.session.commit()
    return jsonify({"success": True, "new_balance": current_user.wallet})

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/admin_data')
@login_required
def admin_data():
    if not current_user.is_admin: return jsonify({"error": "Unauthorized"})
    users = User.query.all()
    txs = Transaction.query.order_by(Transaction.date.desc()).all()
    user_list = [{"username": u.username, "wallet": u.wallet, "role": "Admin" if u.is_admin else "User"} for u in users]
    tx_list = [{"user": t.user_id, "amount": t.amount, "date": t.date.strftime("%Y-%m-%d")} for t in txs]
    return jsonify({"users": user_list, "transactions": tx_list})

@app.route('/reset_db_force')
def reset_db():
    try:
        db.drop_all()
        db.create_all()
        return "DB Reset Success"
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
