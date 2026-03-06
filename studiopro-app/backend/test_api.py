import requests
import json

def test_bins_api():
    try:
        r = requests.get("http://127.0.0.1:8000/bins")
        print("BINS API RESPONSE:")
        print(json.dumps(r.json(), indent=2))
        
        r2 = requests.get("http://127.0.0.1:8000/analytics/fill-rates")
        print("\nANALYTICS API RESPONSE:")
        print(json.dumps(r2.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_bins_api()
