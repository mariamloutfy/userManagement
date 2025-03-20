from flask import request, jsonify
import psycopg2
from config.database import connect_db
from utils import is_valid_email
def get_user(user_id):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT id, username, email, phone,department_id  FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404
        user_data = {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "phone": user[3],
            "department_id": user[4]
        }
        return jsonify(user_data), 200
    except psycopg2.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        cur.close()
        conn.close()
