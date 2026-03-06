from app import app, db
from models import Bin
from datetime import datetime
import time

def debug_iot():
    with app.app_context():
        bin20 = Bin.query.get(20)
        print(f"System Clock (UTC): {datetime.utcnow()}")
        print(f"System Clock (Local): {datetime.now()}")
        
        if bin20:
            print(f"Bin 20 Data:")
            print(f"  Fill Level: {bin20.fill_level}%")
            print(f"  Last Updated (DB): {bin20.last_updated}")
            
            if bin20.last_updated:
                # Try to calculate diff carefully
                # If last_updated is offset-naive, assume it's UTC for this check
                try:
                    diff = (datetime.utcnow() - bin20.last_updated).total_seconds()
                    print(f"  Seconds since last update (assuming DB is UTC): {diff}")
                except:
                    pass
        else:
            print("Bin 20 not found.")

if __name__ == "__main__":
    debug_iot()
