import os
import datetime
import io
import base64
import requests
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import cloudinary
import cloudinary.uploader

app = Flask(__name__)
app.secret_key = "studiopro_pro_secret_key"

# --- 1. CONFIGURATION ---

# 🧠 BRAIN: Hugging Face (Real AI)
# I have already inserted your key below!
HUGGINGFACE_API_KEY = "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"

# ☁️ STORAGE: Cloudinary
# ⚠️ YOU MUST PASTE YOUR CLOUDINARY KEYS HERE ⚠️
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

# --- 2. AI FUNCTION (HUGGING FACE) ---
def query_huggingface(file_stream, prompt):
    # UPDATED URL: Using 'router' instead of 'api-inference'
    API_URL = "https://router.huggingface.co/models/timbrooks/instruct-pix2pix"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    
    # Read file and convert to Base64 (required for this API)
    file_stream.seek(0)
    b64_img = base64.b64encode(file_stream.read()).decode('utf-8')
    
    payload = {
        "inputs": b64_img,
        "parameters": {
            "prompt": prompt,
            "image_guidance_scale": 1.5,
            "num_inference_steps": 20
        }
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    # Cold Start Handler
    if response.status_code == 503:
        raise Exception("AI is warming up... please wait 30 seconds and try again!")
        
    if response.status_code != 200:
        raise Exception(f"HuggingFace Error: {response.text}")

    return response.content

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
        prompt_text = "make it look like a cartoon"
        if style == 'cyberpunk': prompt_text = "make it look like a cyberpunk city, neon lights"
        elif style == 'anime': prompt_text = "make it look like a studio ghibli anime"
        elif style == 'pencil': prompt_text = "make it look like a pencil sketch"
        elif style == 'hdr': prompt_text = "make it look like high definition photography, realistic"

        # 1. Send to Hugging Face
        ai_image_bytes = query_huggingface(file, prompt_text)

        # 2. Upload to Cloudinary
        upload_res = cloudinary.uploader.upload(io.BytesIO(ai_image_bytes), resource_type="image")
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
