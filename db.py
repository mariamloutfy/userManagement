import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST

def connect_db():
    return psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
