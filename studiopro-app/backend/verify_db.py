import psycopg2

def verify_tables():
    try:
        conn = psycopg2.connect(
            user='postgres', 
            password='Pass@123', 
            host='localhost', 
            port='5432', 
            database='waste_db1'
        )
        cur = conn.cursor()
        
        # List tables
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = cur.fetchall()
        print(f"Tables: {tables}")
        
        # Check 'bin' table columns
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'bin'")
        columns = cur.fetchall()
        print(f"Columns in 'bin': {columns}")
        
        # Check if Bin 20 exists
        cur.execute("SELECT * FROM bin WHERE id = 20")
        bin20 = cur.fetchone()
        print(f"Bin 20 data: {bin20}")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_tables()
