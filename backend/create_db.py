import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_db():
    try:
        # Try to connect to 'postgres' database to create the new one
        con = psycopg2.connect(user='postgres', password='Pass@123', host='localhost', port='5432', database='postgres')
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        cur.execute("CREATE DATABASE waste_db1")
        cur.close()
        con.close()
        print("Database created successfully")
    except psycopg2.Error as e:
        if "already exists" in str(e):
            print("Database already exists")
        else:
            print(f"Error: {e}")

if __name__ == "__main__":
    create_db()
