import requests
import random
import time

API_URL = "http://localhost:8000/sensor-data"

BIN_IDS = list(range(1, 20))

def simulate():
    print("Starting IoT Simulation (Bins 1-19)...")
    while True:
        for bin_id in BIN_IDS:
            fill_level = random.randint(10, 95)
            payload = {
                "bin_id": bin_id,
                "fill_level": fill_level
            }
            try:
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    print(f"Update: Bin {bin_id} -> {fill_level}%")
                else:
                    print(f"Failed: Bin {bin_id} ({response.status_code})")
            except Exception as e:
                print(f"Error connecting to backend: {e}")
        
        print("Waiting 10 seconds for next update...")
        time.sleep(10)

if __name__ == "__main__":
    simulate()
