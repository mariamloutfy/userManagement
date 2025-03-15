from flask import request, jsonify
import psycopg2
from config.database import connect_db
from utils import is_valid_email

@routes.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.json 
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        phone = data.get("phone")
        if not username or not email or not password or not phone:
            return jsonify({"error": "All fields are required!"}), 400
        if not is_valid_email(email):
            return jsonify({"error": "Invalid email format!"}), 400
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, email, password, phone) VALUES (%s, %s, %s, %s) RETURNING id",
                (username, email, password, phone),
            )
            user_id = cur.fetchone()[0]
            conn.commit()
            print(f"Hello {username}")
            return jsonify({"message": f"User {username} created successfully!", "user_id": user_id}), 201
        except psycopg2.Error as e:
            conn.rollback()
            if "duplicate key value" in str(e):
                return jsonify({"error": "Email already exists!"}), 400
            return jsonify({"error": "Database error", "details": str(e)}), 500
        finally:
            cur.close()
            conn.close()
    except Exception as e:
        print("🔥 ERROR:", str(e))
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

