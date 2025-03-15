from flask import request, jsonify
import bcrypt
from config.database import connect_db

def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        conn = connect_db()
        cur = conn.cursor()

        cur.execute("SELECT id, password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        conn.close()

        if not user:
            return jsonify({"error": "User not found"}), 404

        user_id, hashed_password = user

        if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
            return jsonify({"message": f"Welcome, user {user_id}!"})
        else:
            return jsonify({"error": "Invalid password"}), 401

    except Exception as e:
        print("🔥 ERROR:", e)  # Debugging print
        return jsonify({"error": "Internal server error"}), 500
