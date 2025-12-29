import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    """Establish and return a connection to the Supabase PostgreSQL database."""
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL current environment variable is not set.")
    try:
        conn = psycopg.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise

def init_db(schema_path="schema.sql"):
    """Initialize the database by running the schema.sql script."""
    if not os.path.exists(schema_path):
        print(f"Schema file {schema_path} not found.")
        return

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            with open(schema_path, "r") as f:
                cur.execute(f.read())
        conn.commit()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    # Test connection
    try:
        c = get_connection()
        print("Successfully connected to Supabase!")
        c.close()
    except Exception:
        pass
