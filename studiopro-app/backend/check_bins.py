from app import app, db
from models import Bin

def check_bins():
    with app.app_context():
        bins = Bin.query.order_by(Bin.id).all()
        print(f"Total bins: {len(bins)}")
        for b in bins:
            print(f"ID: {b.id}, Fill: {b.fill_level}%")

if __name__ == "__main__":
    check_bins()
