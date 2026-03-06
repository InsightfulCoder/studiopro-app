from datetime import datetime
import random
import math
from flask import request, jsonify

from models import Bin, Truck, FillLog, ActiveRoute, update_truck_route, db
from logic.optimizer import optimize_route, get_predicted_bins, cluster_bins, get_priority_bins


# Global state for route staleness
is_route_stale = False
last_optimization_time = datetime.utcnow()
is_truck_moving = False

# Real on-road bin coordinates for Amravati city
# These are snapped to actual road locations
AMRAVATI_BIN_COORDS = {
    1:  (20.9335, 77.7668),  # Morshi Road near Irwin Square
    2:  (20.9349, 77.7721),  # Shivaji Putla Chowk
    3:  (20.9374, 77.7761),  # Rajkamal Chowk, NH-6
    4:  (20.9388, 77.7708),  # Jaistambh Chowk area
    5:  (20.9402, 77.7762),  # Bhatkuli Road junction
    6:  (20.9413, 77.7768),  # Akola Road (State Highway)
    7:  (20.9316, 77.7741),  # Bapuji Nagar Road
    8:  (20.9362, 77.7800),  # Rajapeth Road
    9:  (20.9404, 77.7724),  # Mofussil Bus Stand Road
    10: (20.9440, 77.7752),  # Tapadia Stadium approach
    11: (20.9298, 77.7780),  # Shende Plot Chowk
    12: (20.9270, 77.7760),  # Gorakshan Road
    13: (20.9285, 77.7809),  # Near Amravati Railway Station
    14: (20.9310, 77.7830),  # Station Road
    15: (20.9355, 77.7848),  # Badnera Road
    16: (20.9388, 77.7840),  # Nandgaonpeth Road
    17: (20.9450, 77.7800),  # Chikhaldara Road junction
    18: (20.9460, 77.7725),  # Chandrashekhar Nagar Road
    19: (20.9475, 77.7680),  # Kapas Naka
    20: (20.9330, 77.7700),  # Varud Road (IOT Bin)
}


def register_routes(app, db):
    with app.app_context():
        # db.create_all()
        # Seed initial trucks if none exist
        if Truck.query.count() == 0:
            trucks = [
                Truck(id=1, latitude=20.9374, longitude=77.7796, capacity=1000),
                Truck(id=2, latitude=20.9380, longitude=77.7800, capacity=1200)
            ]
            for t in trucks:
                db.session.add(t)
            
        # Seed admin user if none exist
        from models import User
        if User.query.filter_by(username='admin').count() == 0:
            admin = User(username='admin', password='password123')
            db.session.add(admin)
            
        db.session.commit()

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    @app.route('/bins/seed', methods=['POST'])
    def seed_bins():
        """Force-update all 20 bins to their correct on-road coordinates."""
        seeded = []
        for bin_id, (lat, lng) in AMRAVATI_BIN_COORDS.items():
            bin_item = Bin.query.get(bin_id)
            if bin_item:
                bin_item.latitude = lat
                bin_item.longitude = lng
            else:
                bin_item = Bin(id=bin_id, latitude=lat, longitude=lng, fill_level=random.randint(10, 85))
                db.session.add(bin_item)
            seeded.append(bin_id)
        db.session.commit()
        print(f"Seeded {len(seeded)} bins with real road coordinates.")
        return jsonify({'status': 'success', 'seeded_count': len(seeded), 'bin_ids': seeded})

    @app.route('/bins', methods=['GET'])
    def get_bins():
        bins = Bin.query.all()
        return jsonify([{'id': b.id, 'lat': b.latitude, 'lng': b.longitude, 'fill': b.fill_level} for b in bins])

    @app.route('/sensor-data', methods=['POST'])
    def update_sensor_data():
        data = request.json
        print(f"DEBUG: Received /sensor-data request from {request.remote_addr}. Data: {data}")
        
        if not data or 'bin_id' not in data or 'fill_level' not in data:
            return jsonify({'status': 'error', 'message': 'Missing data'}), 400
        
        bin_id = data.get('bin_id')
        fill_level = data.get('fill_level')

        global is_truck_moving
        # ALLOW updates for Bin 20 ALWAYS. For other bins, block if truck is moving.
        if is_truck_moving and bin_id != 20:
            return jsonify({'status': 'ignored', 'message': 'Truck is moving, updates frozen'}), 200
        
        bin_item = Bin.query.get(bin_id)
        if not bin_item:
            # Use seeded road coordinate if available, otherwise fallback
            coords = AMRAVATI_BIN_COORDS.get(bin_id)
            lat = coords[0] if coords else (20.9374 + random.uniform(-0.02, 0.02))
            lng = coords[1] if coords else (77.7796 + random.uniform(-0.02, 0.02))
            bin_item = Bin(
                id=bin_id,
                latitude=lat,
                longitude=lng,
                fill_level=fill_level
            )
            db.session.add(bin_item)
        else:
            bin_item.fill_level = fill_level
            bin_item.last_updated = db.func.now()
        
        log_entry = FillLog(bin_id=bin_id, fill_level=fill_level)
        db.session.add(log_entry)
        
        # Stale Path Check for emergency overflow
        global is_route_stale
        if fill_level > 95:
            # Check if this bin is NOT in any ActiveRoute
            in_active_route = ActiveRoute.query.filter_by(bin_id=bin_id).first()
            if not in_active_route:
                is_route_stale = True

        
        db.session.commit()

        if bin_id == 20:
            if fill_level == -1:
                status = "SENSOR ERROR"
            else:
                status = "CRITICAL" if fill_level > 75 else ("WARNING" if fill_level > 50 else "OK")
            
            print("")
            print("=" * 55)
            print(f"  IoT BIN 20 UPDATE RECEIVED")
            print("=" * 55)
            print(f"  Fill Level  : {fill_level if fill_level != -1 else 'ERR'} %")
            print(f"  Status      : {status}")
            print(f"  Location    : Varud Road, Amravati")
            print(f"  Timestamp   : {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
            print("=" * 55)
            print("")
        else:
            print(f"ok -> bin_id: {bin_id} updated with fill_level: {fill_level}%")

        return jsonify({'status': 'success', 'bin_id': bin_id, 'fill': fill_level})

    @app.route('/check-route-update', methods=['GET'])
    def check_route_update():
        global is_route_stale
        return jsonify({'is_stale': is_route_stale})


    @app.route('/analytics/fill-rates', methods=['GET'])
    def get_fill_rate_analytics():
        from collections import defaultdict
        
        bins = Bin.query.all()
        if not bins:
            return jsonify([])
            
        bin_ids = [b.id for b in bins]
        # Fetch last 5 logs for each bin to get a more stable average
        all_logs = FillLog.query.filter(FillLog.bin_id.in_(bin_ids)).order_by(FillLog.bin_id, FillLog.timestamp.desc()).all()
        
        logs_by_bin = defaultdict(list)
        for log in all_logs:
            if len(logs_by_bin[log.bin_id]) < 5:
                logs_by_bin[log.bin_id].append(log)
        
        analytics = []
        for b in bins:
            logs = logs_by_bin[b.id]
            prediction_hours = -1 # -1 means unknown or never
            
            if len(logs) >= 2:
                newest = logs[0]
                oldest = logs[-1]
                
                time_diff = (newest.timestamp - oldest.timestamp).total_seconds() / 3600.0
                fill_diff = newest.fill_level - oldest.fill_level
                
                if time_diff > 0 and fill_diff > 0:
                    fill_rate = fill_diff / time_diff # % per hour
                    remaining_capacity = 100 - b.fill_level
                    prediction_hours = round(remaining_capacity / fill_rate, 2)
                    
            analytics.append({
                'bin_id': b.id,
                'current_fill': b.fill_level,
                'predicted_full_in_hours': prediction_hours
            })
            
        return jsonify(analytics)


    @app.route('/optimize-route', methods=['GET'])
    def trigger_optimization():
        red_bins = Bin.query.filter(Bin.fill_level > 70).all()
        red_bins_data = [{'id': b.id, 'lat': b.latitude, 'lng': b.longitude} for b in red_bins]
        
        # Get Predicted bins (>60% current, predicted >80% in 2h)
        predicted_bins = get_predicted_bins()
        
        # Get Priority bins (Score > 80)
        priority_bins = get_priority_bins()
        
        # Merge red bins (>70%), predicted bins, and priority bins, removing duplicates
        all_bins_data = {b['id']: b for b in red_bins_data}
        for b in (predicted_bins + priority_bins):
            if b['id'] not in all_bins_data:
                all_bins_data[b['id']] = b
        
        final_bins_list = list(all_bins_data.values())

        depot = {'lat': 20.9374, 'lng': 77.7796}
        
        if not final_bins_list:
            return jsonify({'status': 'info', 'message': 'No bins require collection.', 'routes': {}})
        
        # Multi-truck logic
        available_trucks = Truck.query.filter_by(status='available').all()
        if not available_trucks:
            return jsonify({'status': 'error', 'message': 'No available trucks.'}), 400
        
        num_trucks = len(available_trucks)
        fleet_routes = optimize_route(final_bins_list, depot, num_trucks)
        
        # Persist routes and update timestamps
        final_fleet_routes = {}
        for i, (truck_internal_idx, route) in enumerate(fleet_routes.items()):
            if i >= len(available_trucks): break
            
            truck = available_trucks[i]
            update_truck_route(truck.id, route)
            final_fleet_routes[truck.id] = route
            
            # extract bin IDs from the route (excluding depot Points which have id=None)
            bin_ids = [int(p['id']) for p in route if p.get('id') and p['id'].isdigit()]
            
            if bin_ids:
                Bin.query.filter(Bin.id.in_(bin_ids)).update({Bin.last_collected_at: datetime.utcnow()}, synchronize_session=False)

        global is_route_stale, last_optimization_time

        is_route_stale = False
        last_optimization_time = datetime.utcnow()

        
        db.session.commit()
        return jsonify({'status': 'success', 'routes': fleet_routes})

    @app.route('/truck/status', methods=['POST'])
    def set_truck_status():
        global is_truck_moving
        data = request.json
        is_truck_moving = data.get('moving', False)
        print(f"Truck movement status set to: {is_truck_moving}")
        return jsonify({'status': 'success', 'is_truck_moving': is_truck_moving})

    @app.route('/bins/reset/<int:bin_id>', methods=['POST'])
    def reset_bin(bin_id):
        bin_item = Bin.query.get(bin_id)
        if bin_item:
            bin_item.fill_level = 0
            bin_item.last_collected_at = datetime.utcnow()
            db.session.commit()
            print(f"Bin {bin_id} reset to 0%")
            return jsonify({'status': 'success', 'bin_id': bin_id})
        return jsonify({'status': 'error', 'message': 'Bin not found'}), 404

    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        print(f"DEBUG: Login attempt - Data: {data}")
        
        if not data:
            return jsonify({'status': 'error', 'message': 'No data received'}), 400
            
        username = data.get('username')
        password = data.get('password')
        
        from models import User
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            print(f"DEBUG: Login successful for user: {username}")
            return jsonify({'status': 'success', 'message': 'Login successful', 'username': username})
        
        print(f"DEBUG: Login failed for user: {username}")
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401

    @app.route('/trucks', methods=['GET'])
    def get_trucks():
        trucks = Truck.query.all()
        result = []
        for t in trucks:
            # Find current route for this truck
            active_points = ActiveRoute.query.filter_by(truck_id=t.id).order_by(ActiveRoute.point_index).all()
            route_data = [{'lat': p.lat, 'lng': p.lng, 'bin_id': p.bin_id} for p in active_points]
            
            result.append({
                'id': t.id,
                'status': t.status,
                'latitude': t.latitude,
                'longitude': t.longitude,
                'capacity': t.capacity,
                'current_load': t.current_load,
                'route': route_data
            })
        return jsonify(result)

