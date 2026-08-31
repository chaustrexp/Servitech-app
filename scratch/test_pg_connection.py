import psycopg2
import sys

passwords = ["1234", "E1093595859", "bayona117", "postgres", "admin", "root", ""]

for pwd in passwords:
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password=pwd,
            host="localhost",
            port=5432,
            client_encoding="utf-8"
        )
        print(f"SUCCESS: Connected to 'postgres' db with password: '{pwd}'")
        
        # Check if servitech db exists
        cur = conn.cursor()
        cur.execute("SELECT datname FROM pg_database WHERE datname = 'servitech';")
        db_exists = cur.fetchone()
        print(f"servitech database exists? {bool(db_exists)}")
        conn.close()
        break
    except Exception as e:
        # decode raw bytes or string representation
        print(f"Failed with password '{pwd}': {e!r}")
