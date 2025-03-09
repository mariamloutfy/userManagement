import re
import psycopg2
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db.connection import connect_db

users_bp = Blueprint("users", __name__)

def is_valid_email(email):
    """Check if an email is valid using regex."""
    email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(email_regex, email) is not None

@users_bp.route('/create-user', methods=['POST'])
def create_user():
    """Create a new user with hashed password."""
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
        
        hashed_password = generate_password_hash(password)

        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, email, password, phone) VALUES (%s, %s, %s, %s) RETURNING id",
                (username, email, hashed_password, phone),
            )
            user_id = cur.fetchone()[0]
            conn.commit()
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
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@users_bp.route('/get-user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Fetch a user by ID."""
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT id, username, email, phone FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404
        user_data = {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "phone": user[3]
        }
        return jsonify(user_data), 200
    except psycopg2.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        cur.close()
        conn.close()

@users_bp.route('/login', methods=['POST'])
def login():
    """Authenticate a user."""
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required!"}), 400

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT id, username, password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()

        if not user or not check_password_hash(user[2], password):
            return jsonify({"error": "Invalid email or password! Learn to type properly!"}), 401

        return jsonify({"message": f"Welcome, {user[1]}!"}), 200
    except psycopg2.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        cur.close()
        conn.close()
