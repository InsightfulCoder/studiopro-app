from flask import Flask
from flask_cors import CORS
import os
from models import db

app = Flask(__name__, static_folder='../frontend/public', static_url_path='')
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Pass%40123@localhost:5432/waste_db1"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db.init_app(app)

# Import and register routes
from api_routes import register_routes
register_routes(app, db)

if __name__ == '__main__':
    print("Starting RouteX Backend Server...")
    # host='0.0.0.0' is REQUIRED for the ESP32 to connect
    app.run(host='0.0.0.0', port=8000, debug=False)
