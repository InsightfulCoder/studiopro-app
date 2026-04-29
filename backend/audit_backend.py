import requests
import time
import random

BASE_URL = "http://127.0.0.1:8000"

def run_audit():
    print("🚀 Starting Backend Performance Audit...")
    print("Step 1: Simulating 200 sequential sensor updates (Burst Mode)")
    
    start_burst = time.time()
    for i in range(200):
        # Rotate through 20 bins
        bin_id = (i % 20) + 1
        payload = {
            "bin_id": bin_id,
            "fill_level": random.randint(10, 95)
        }
        try:
            requests.post(f"{BASE_URL}/sensor-data", json=payload)
        except Exception as e:
            print(f"Update failed at round {i}: {e}")
            break
            
    end_burst = time.time()
    burst_duration = end_burst - start_burst
    print(f"✅ Burst complete: 200 updates in {burst_duration:.2f} seconds.")

    print("\nStep 2: Benchmarking /optimize-route under cumulative load...")
    
    # Measure optimization time
    start_opt = time.time()
    try:
        response = requests.get(f"{BASE_URL}/optimize-route")
        end_opt = time.time()
        
        opt_latency = (end_opt - start_opt) * 1000 # ms
        print(f"🏁 Execution Time: {opt_latency:.2f} ms")
        
        if response.status_code == 200:
            print("Status: Success")
        else:
            print(f"Status: Error ({response.status_code})")

        # Threshold advice
        if opt_latency > 200:
            print("\n⚠️ WARNING: Performance threshold exceeded (>200ms).")
            print("💡 RECOMMENDATION: Add a non-clustered index on the 'bin' table's 'fill_level' column.")
            print("   SQL: CREATE INDEX idx_bin_fill ON bin(fill_level);")
            print("   This will speed up filtering for target bins during optimization.")
        else:
            print("\n🚀 PERFORMANCE IS OPTIMAL: System responding within sub-200ms requirement.")

    except Exception as e:
        print(f"Optimization call failed: {e}")

if __name__ == "__main__":
    try:
        # Check if server is up
        requests.get(BASE_URL)
        run_audit()
    except requests.exceptions.ConnectionError:
        print(f"❌ Error: Could not connect to server at {BASE_URL}. Ensure backend is running.")
