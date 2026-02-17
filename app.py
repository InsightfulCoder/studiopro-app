import os
import datetime
import io
import base64
import requests
import numpy as np
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import cloudinary
import cloudinary.uploader

app = Flask(__name__)
app.secret_key = "studiopro_pro_secret_key"

# --- CONFIGURATION (SECURE) ---
# This line is the secret bridge. It pulls the key from Render's Safe Box.
# Because the actual key is not written here, GitGuardian will not flag it.
HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")

# ⚠️ CLOUDINARY KEYS ⚠️
cloudinary.config(
    cloud_name = "dhococ8e5",
    api_key = "457977599793717",    
    api_secret = "uPtdj1lgu-HvQ2vnmHCgDk1QHu0" 
)

db_url = "postgresql://neondb_owner:npg_JXnas5ev8AgG@ep-crimson-wind-aillfxxy-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"
if db_url.startswith("postgres://"): db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

# --- MODELS ---
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

# --- AI LOGIC (ROUTER FIX + SDXL) ---
def process_ai(file, style):
    if not HUGGINGFACE_API_KEY:
        raise Exception("❌ API Key missing in Render Environment.")

    # CORRECT URL: Includes the /hf-inference/ path required by the new Router
    API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    
    # High-quality technical prompts
    quality_boost = "(masterpiece:1.3), (highly detailed:1.2), cinematic lighting, 8k resolution, sharp focus"
    negative_prompt = "blurry, low quality, distorted, extra fingers, mutated hands, bad anatomy, text, grainy"
    
    prompt_map = {
        'cartoon': f"Pixar style 3D render, vibrant, cute character, {quality_boost}", 
        'pencil': f"hyper-realistic pencil sketch, fine graphite lines, {quality_boost}", 
        'anime': f"Studio Ghibli style, high quality anime art, {quality_boost}", 
        'cyberpunk': f"neon futuristic city, photorealistic, volumetric lighting, {quality_boost}"
    }
    
    file.seek(0)
    b64_img = base64.b64encode(file.read()).decode('utf-8')
    
    payload = {
        "inputs": prompt_map.get(style, f"digital art, {quality_boost}"),
        "parameters": {
            "negative_prompt": negative_prompt,
            "image": b64_img,
            "strength": 0.55,
            "guidance_scale": 11.0
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            return response.content
        elif response.status_code == 503:
            raise Exception("⏳ AI is warming up. Please click Generate again in 20 seconds.")
        else:
            raise Exception(f"❌ AI Error ({response.status_code}): {response.text}")
            
    except Exception as e:
        raise Exception(f"⚠️ Connection Error: {str(e)}")

# --- ROUTES ---
@app.route('/')
def index():
    history = []
    if current_user.is_authenticated:
        history = ImageHistory.query.filter_by(user_id=current_user.id).order_by(ImageHistory.timestamp.desc()).limit(20).all()
    return render_template('index.html', user=current_user if current_user.is_authenticated else None, history=history)

@app.route('/process', methods=['POST'])
def process():
    if not current_user.is_authenticated:
        if 'guest_count' not in session: session['guest_count'] = 0   
        if session['guest_count'] >= 3:
            return jsonify({"auth_required": True, "error": "Free Limit Reached (3/3). Please Login!"})
        current_wallet = f"Guest ({2 - session['guest_count']} left)"
        session['guest_count'] += 1
    else:
        if current_user.wallet < 10: return jsonify({"error": "Insufficient Funds! Add Coins."})
        current_wallet = current_user.wallet - 10

    try:
        file = request.files.get('file')
        style = request.form.get('style')
        
        img_bytes = process_ai(file, style)
        upload = cloudinary.uploader.upload(io.BytesIO(img_bytes), resource_type="image")
        
        if current_user.is_authenticated:
            current_user.wallet -= 10
            new_entry = ImageHistory(user_id=current_user.id, image_url=upload['secure_url'], style=style)
            db.session.add(new_entry)
            db.session.commit()
            current_wallet = current_user.wallet

        return jsonify({"image": upload['secure_url'], "wallet": current_wallet, "message": "Success"})

    except Exception as e:
        return jsonify({"error": str(e)})

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
        db.drop_all(); db.create_all()
        return "DB Reset Success"
    except Exception as e: return str(e)

if __name__ == '__main__':
    with app.app_context(): db.create_all()
    app.run(debug=True)
