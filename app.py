import os
import datetime
import uuid
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import cloudinary
import cloudinary.uploader

app = Flask(__name__)
app.secret_key = "studiopro_pro_secret_key"

# --- 1. CONFIGURATION ---

# Brain (DeepAI)
DEEPAI_API_KEY = "377e9ecf-6443-4f51-b191-f7d3f8b442e7"

# Storage (Cloudinary)
cloudinary.config(
    cloud_name = "dhococ8e5",
    api_key = "457977599793717",    # <--- PASTE YOUR REAL API KEY HERE
    api_secret = "uPtdj1lgu-HvQ2vnmHCgDk1QHu0" # <--- PASTE YOUR REAL API SECRET HERE
)

# Database (Neon PostgreSQL)
db_url = "postgresql://neondb_owner:npg_JXnas5ev8AgG@ep-crimson-wind-aillfxxy-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# --- 2. DATABASE MODELS ---
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

# --- 3. ROUTES ---
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
        prompt_text = "cartoon style, clean lines, vibrant"
        if style == 'cyberpunk': prompt_text = "cyberpunk style, neon lights, futuristic city, high contrast"
        elif style == 'anime': prompt_text = "anime style, studio ghibli, vibrant, detailed"
        elif style == 'pencil': prompt_text = "pencil sketch, black and white drawing, architectural"
        elif style == 'hdr': prompt_text = "HDR photography, highly detailed, realistic, 8k"

        # Send to DeepAI
        r = requests.post(
            "https://api.deepai.org/api/image-editor",
            files={'image': file.stream}, 
            data={'text': prompt_text},
            headers={'api-key': DEEPAI_API_KEY}
        )
        result_json = r.json()
        
        if 'output_url' in result_json:
            ai_image_url = result_json['output_url']
            
            # Upload to Cloudinary
            upload_res = cloudinary.uploader.upload(ai_image_url)
            permanent_url = upload_res['secure_url']

            # Save to Database
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
        else:
            return jsonify({"error": "AI Error"}), 500

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

