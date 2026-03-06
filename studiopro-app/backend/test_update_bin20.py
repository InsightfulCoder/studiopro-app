from app import app, db
from models import Bin

def update():
    with app.app_context():
        bin_id = 20
        fill = 99
        bin_item = Bin.query.get(bin_id)
        if bin_item:
            bin_item.fill_level = fill
            db.session.commit()
            print(f"Updated Bin {bin_id} to {fill}%")
        else:
            print("Bin 20 not found")

if __name__ == "__main__":
    update()
