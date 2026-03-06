import requests
import time
import json

BASE_URL = "http://127.0.0.1:8000"


def test_full_cycle():
    print("Starting Integration Test: Full Cycle Simulation (20 Bins)")
    
    # 1. Update 20 bins to initial state (Green/Yellow)
    for i in range(1, 21):
        payload = {"bin_id": i, "fill_level": 30 + (i % 20)}
        response = requests.post(f"{BASE_URL}/sensor-data", json=payload)
        assert response.status_code == 200, f"Failed to update bin {i}"
    
    print("Step 1: 20 Bins updated successfully.")

    # 2. Set 5 specific bins to 'Red' (>70%)
    red_bin_ids = [2, 5, 10, 15, 19]
    for bid in red_bin_ids:
        payload = {"bin_id": bid, "fill_level": 85}
        requests.post(f"{BASE_URL}/sensor-data", json=payload)
    
    print(f"Step 2: Bins {red_bin_ids} set to RED.")

    # 3. Benchmark /optimize-route
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/optimize-route")
    end_time = time.time()
    
    latency_ms = (end_time - start_time) * 1000
    print(f"Step 3: /optimize-route took {latency_ms:.2f}ms.")
    
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    assert 'routes' in data
    assert len(data['routes']) > 0
    
    # Assert performance requirement (< 200ms)
    assert latency_ms < 200, f"Performance bottleneck detected: {latency_ms:.2f}ms > 200ms"
    print("Performance Check Passed!")

def test_empty_route():
    print("\nStarting Integration Test: Empty Route Case")
    
    # Set all bins to Green (<70% and no priority/prediction)
    # We'll just reset them to 10%
    for i in range(1, 21):
        requests.post(f"{BASE_URL}/sensor-data", json={"bin_id": i, "fill_level": 10})
    
    # Reset last_collected_at manually via API isn't easy here, 
    # but since we just reset fill, priority should drop.
    
    response = requests.get(f"{BASE_URL}/optimize-route")
    assert response.status_code == 200
    data = response.json()
    
    # If no bins need collection, it returns 'info' and empty routes
    assert data['status'] == 'info'
    assert 'No bins require collection' in data['message']
    print("Empty Route Graceful Handling Passed!")

if __name__ == "__main__":
    try:
        # Check if server is up
        requests.get(BASE_URL)
        test_full_cycle()
        test_empty_route()
        print("\nAll Backend Tests Passed Successfully!")
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to server at {BASE_URL}. Is app.py running?")
    except AssertionError as e:
        print(f"Test Failed: {e}")
