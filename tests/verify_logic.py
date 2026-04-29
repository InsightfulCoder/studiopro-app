import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def verify_all():
    print("--- Verification Started ---")
    
    # 1. Reset Bin 1 for starting point
    print("Setting Bin 1 to 50%...")
    requests.post(f"{BASE_URL}/sensor-data", json={"bin_id": 1, "fill_level": 50})
    
    # 2. Start Truck Movement
    print("Setting Truck Status: MOVING...")
    requests.post(f"{BASE_URL}/truck/status", json={"moving": True})
    
    # 3. Try to update Bin 1 while moving
    print("Attempting to update Bin 1 while truck is moving (should be ignored)...")
    res = requests.post(f"{BASE_URL}/sensor-data", json={"bin_id": 1, "fill_level": 80})
    data = res.json()
    print(f"Update Result: {data['status']} - {data.get('message', '')}")
    
    # 4. Verify Bin 1 level (should still be 50)
    res = requests.get(f"{BASE_URL}/bins")
    bins = res.json()
    bin1 = next(b for b in bins if b['id'] == 1)
    print(f"Bin 1 Current Level: {bin1['fill']}% (Expected: 50%)")
    assert bin1['fill'] == 50
    
    # 5. Stop Truck Movement
    print("Setting Truck Status: IDLE...")
    requests.post(f"{BASE_URL}/truck/status", json={"moving": False})
    
    # 6. Update Bin 1 while idle
    print("Attempting to update Bin 1 while truck is idle (should succeed)...")
    requests.post(f"{BASE_URL}/sensor-data", json={"bin_id": 1, "fill_level": 90})
    res = requests.get(f"{BASE_URL}/bins")
    bin1 = next(b for b in res.json() if b['id'] == 1)
    print(f"Bin 1 Current Level: {bin1['fill']}% (Expected: 90%)")
    assert bin1['fill'] == 90
    
    # 7. Reset Bin 1 (simulating arrival)
    print("Simulating arrival at Bin 1 (Calling reset)...")
    requests.post(f"{BASE_URL}/bins/reset/1")
    res = requests.get(f"{BASE_URL}/bins")
    bin1 = next(b for b in res.json() if b['id'] == 1)
    print(f"Bin 1 Current Level: {bin1['fill']}% (Expected: 0%)")
    assert bin1['fill'] == 0
    
    print("--- Verification Successful! ---")

if __name__ == "__main__":
    verify_all()
