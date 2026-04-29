import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_clustering():
    print("--- Testing Spatial Clustering ---")
    
    # 0. Reset all existing bins to low fill to isolate the test
    print("Resetting all bins to 10%...")
    all_bins = requests.get(f"{BASE_URL}/bins").json()
    for b in all_bins:
        requests.post(f"{BASE_URL}/sensor-data", json={"bin_id": b['id'], "fill_level": 10})
    
    # 1. Setup Bins in two distinct groups
    # Group A (West side)
    west_bins = [
        {"bin_id": 101, "lat": 20.9300, "lng": 77.7700, "fill_level": 90},
        {"bin_id": 102, "lat": 20.9310, "lng": 77.7710, "fill_level": 90},
    ]
    # Group B (East side)
    east_bins = [
        {"bin_id": 201, "lat": 20.9400, "lng": 77.7900, "fill_level": 90},
        {"bin_id": 202, "lat": 20.9410, "lng": 77.7910, "fill_level": 90},
    ]
    
    for b in west_bins + east_bins:
        requests.post(f"{BASE_URL}/sensor-data", json=b)
    
    # 2. Trigger Optimization
    print("Triggering optimization...")
    res = requests.get(f"{BASE_URL}/optimize-route")
    data = res.json()
    
    routes = data.get('routes', {})
    print(f"Number of routes generated: {len(routes)}")
    
    for truck_id, route in routes.items():
        # Get bin IDs in this route (skipping depot)
        bin_ids = [p['id'] for p in route if p.get('id')]
        print(f"Truck {truck_id} route IDs: {bin_ids}")
        
        # Verify that bins in the same route are in the same cluster
        # e.g., if 101 is in the route, 102 should also be there, but not 201/202
        if '101' in bin_ids:
            assert '102' in bin_ids, f"Truck {truck_id} split west cluster!"
            assert '201' not in bin_ids, f"Truck {truck_id} overlapped with east cluster!"
            print(f"Verified: Truck {truck_id} correctly handled the West Cluster.")
        elif '201' in bin_ids:
            assert '202' in bin_ids, f"Truck {truck_id} split east cluster!"
            assert '101' not in bin_ids, f"Truck {truck_id} overlapped with west cluster!"
            print(f"Verified: Truck {truck_id} correctly handled the East Cluster.")

    print("\n--- All Clustering Tests Passed! ---")

if __name__ == "__main__":
    test_clustering()
