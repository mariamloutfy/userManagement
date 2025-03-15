from flask import request, jsonify
import psycopg2
from config.database import connect_db
from utils import is_valid_email
def get_users():
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT id, username, email, phone FROM users")
        users = cur.fetchall()
        if not users:
            return jsonify({"message": "No users found"}), 404
        user_list = [
            {"id": user[0], "username": user[1], "email": user[2], "phone": user[3]}
            for user in users
        ]
        return jsonify(user_list), 200
    except psycopg2.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        cur.close()
        conn.close()