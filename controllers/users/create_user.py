from flask import request, jsonify
import psycopg2
from config.database import connect_db
from utils import is_valid_email
from werkzeug.security import generate_password_hash
from hash_passwords import hash_password

def create_user():
    try:
        data = request.json
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        phone = data.get("phone")
        department_id = data.get("department_id")
        if not username or not email or not password or not department_id:
            return jsonify({"error": "Missing required fields"}), 400
        hashed_password = hash_password(password)  # ✅ Secure password storage
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, email, password, phone,department_id) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                    (username, email, hashed_password, phone, department_id))
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "User created", "user_id": user_id}), 201
    except Exception as e:
        print("Error in create_user:", str(e))  # Debugging
        return jsonify({"error": "Server error", "details": str(e)}), 500