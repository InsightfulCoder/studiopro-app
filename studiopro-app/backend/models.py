from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Bin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    fill_level = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    last_collected_at = db.Column(db.DateTime, default=datetime.utcnow)


class Truck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    current_load = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='available') # available, busy, maintenance

class ActiveRoute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    truck_id = db.Column(db.Integer, db.ForeignKey('truck.id'), nullable=False)
    bin_id = db.Column(db.Integer, nullable=True) # Optional, null for depot
    point_index = db.Column(db.Integer, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)


class FillLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bin_id = db.Column(db.Integer, db.ForeignKey('bin.id'), nullable=False)
    fill_level = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


def update_truck_route(truck_id, coordinates):
    """
    Clears the ActiveRoute for a specific truck and inserts a new list of coordinates.
    coordinates: List of dictionaries [{'lat': ..., 'lng': ...}]
    """
    try:
        # Clear existing route for this truck
        ActiveRoute.query.filter_by(truck_id=truck_id).delete()
        
        # Batch insert new coordinates
        for index, coord in enumerate(coordinates):
            new_point = ActiveRoute(
                truck_id=truck_id,
                bin_id=coord.get('id'), # Use .get() as depot might not have ID
                point_index=index,
                lat=coord['lat'],
                lng=coord['lng']
            )
            db.session.add(new_point)

        
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error updating route for truck {truck_id}: {e}")
        return False