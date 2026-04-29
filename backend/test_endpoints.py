import requests
import time

def test_endpoint(url, method='GET', data=None):
    start = time.time()
    try:
        if method == 'GET':
            res = requests.get(url, timeout=10)
        else:
            res = requests.post(url, json=data, timeout=10)
        end = time.time()
        print(f"{method} {url} -> Status: {res.status_code}, Time: {end-start:.2f}s")
        return res
    except Exception as e:
        print(f"{method} {url} -> Error: {e}")
        return None

def run_tests():
    base_url = "http://127.0.0.1:8000"
    print(f"Testing endpoints at {base_url}...")
    
    test_endpoint(f"{base_url}/bins")
    test_endpoint(f"{base_url}/analytics/fill-rates")
    test_endpoint(f"{base_url}/bins/seed", method='POST')
    test_endpoint(f"{base_url}/sensor-data", method='POST', data={"bin_id": 20, "fill_level": 50})
    test_endpoint(f"{base_url}/check-route-update")

if __name__ == "__main__":
    run_tests()
