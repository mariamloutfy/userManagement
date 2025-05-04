import psycopg2
from config.database import connect_db
from datetime import datetime
from utils import is_valid_email

def fetch_one(query, params=None):
    conn = None
    cur = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(query, params)
        return cur.fetchone()
    except psycopg2.Error as e:
        raise e
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
