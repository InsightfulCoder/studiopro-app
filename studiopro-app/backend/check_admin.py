from app import app, db
from models import User

def check_admin():
    with app.app_context():
        try:
            # Try to query the User table
            user = User.query.filter_by(username='admin').first()
            if user:
                print(f"Admin found! Username: {user.username}, Password: {user.password}")
            else:
                print("Admin user NOT found. Seeding now...")
                new_admin = User(username='admin', password='password123')
                db.session.add(new_admin)
                db.session.commit()
                print("Admin user seeded successfully.")
        except Exception as e:
            print(f"Error checking/seeding admin: {e}")
            print("Attempting to create all tables...")
            db.create_all()
            print("Tables created. Re-seeding...")
            new_admin = User(username='admin', password='password123')
            db.session.add(new_admin)
            db.session.commit()
            print("Admin user seeded successfully.")

if __name__ == "__main__":
    check_admin()
