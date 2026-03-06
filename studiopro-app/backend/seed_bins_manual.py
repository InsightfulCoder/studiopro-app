import psycopg2
from datetime import datetime
import random

def check_and_seed():
    try:
        conn = psycopg2.connect(
            user='postgres', 
            password='Pass@123', 
            host='localhost', 
            port='5432', 
            database='waste_db1'
        )
        cur = conn.cursor()
        
        # Check if Bin table exists and has data
        cur.execute("SELECT count(*) FROM bin")
        count = cur.fetchone()[0]
        print(f"Current bin count: {count}")
        
        if count == 0:
            print("Seeding bins...")
            AMRAVATI_BIN_COORDS = {
                1:  (20.9335, 77.7668),
                2:  (20.9349, 77.7721),
                3:  (20.9374, 77.7761),
                4:  (20.9388, 77.7708),
                5:  (20.9402, 77.7762),
                6:  (20.9413, 77.7768),
                7:  (20.9316, 77.7741),
                8:  (20.9362, 77.7800),
                9:  (20.9404, 77.7724),
                10: (20.9440, 77.7752),
                11: (20.9298, 77.7780),
                12: (20.9270, 77.7760),
                13: (20.9285, 77.7809),
                14: (20.9310, 77.7830),
                15: (20.9355, 77.7848),
                16: (20.9388, 77.7840),
                17: (20.9450, 77.7800),
                18: (20.9460, 77.7725),
                19: (20.9475, 77.7680),
                20: (20.9330, 77.7700),
            }
            
            for bin_id, (lat, lng) in AMRAVATI_BIN_COORDS.items():
                fill = random.randint(10, 85)
                cur.execute(
                    "INSERT INTO bin (id, latitude, longitude, fill_level, last_updated, last_collected_at) VALUES (%s, %s, %s, %s, %s, %s)",
                    (bin_id, lat, lng, fill, datetime.now(), datetime.now())
                )
            conn.commit()
            print("Successfully seeded 20 bins.")
        else:
            cur.execute("SELECT id, fill_level FROM bin")
            bins = cur.fetchall()
            print("Existing bins:")
            for b in bins:
                print(f"  Bin {b[0]}: {b[1]}%")
                
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_and_seed()
