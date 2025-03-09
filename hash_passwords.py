import psycopg2
from werkzeug.security import generate_password_hash

DB_NAME = "userdb"
DB_USER = "myuser"
DB_PASSWORD = "mypassword"
DB_HOST = "localhost"

def connect_db():
    return psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

def hash_existing_passwords():
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute("SELECT id, password FROM users")
    users = cur.fetchall()
    for user_id, plain_password in users:
        hashed_password = generate_password_hash(plain_password, method='pbkdf2:sha256')

        cur.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_password, user_id))
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Passwords hashed successfully!")

if __name__ == "__main__":
    hash_existing_passwords()