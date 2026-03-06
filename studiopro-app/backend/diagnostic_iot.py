import requests
import json

url = "http://localhost:8000/sensor-data"
payload = {"bin_id": 20, "fill_level": 74}
try:
    print(f"Sending POST to {url} with {payload}")
    # Using the local IP to match ESP32 environment exactly
    url_ip = "http://10.197.167.249:8000/sensor-data"
    resp = requests.post(url_ip, json=payload, timeout=5)
    print(f"Status Code: {resp.status_code}")
    print(f"Response Body: {resp.text}")
except Exception as e:
    print(f"Error: {e}")
