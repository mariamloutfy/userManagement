from flask import Blueprint, request, jsonify
import psycopg2
from db import connect_db
from utils import is_valid_email

routes = Blueprint("routes", __name__)

@routes.route('/create-user', methods=['POST'])
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

@routes.route('/get-user/<int:user_id>', methods=['GET'])
def get_user(user_id):
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

@routes.route('/get-users', methods=['GET'])
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

@routes.route('/update-user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    conn = None
    cur = None
    try:
        data = request.json
        username = data.get("username")
        phone = data.get("phone")
        email = data.get("email")

        if not username and not phone and not email:
            return jsonify({"error": "At least one field (username, phone, or email) is required!"}), 400

        conn = connect_db()
        cur = conn.cursor()

        update_fields = []
        update_values = []

        if username:
            update_fields.append("username = %s")
            update_values.append(username)
        if phone:
            update_fields.append("phone = %s")
            update_values.append(phone)
        if email:
            update_fields.append("email = %s")
            update_values.append(email)

        update_values.append(user_id)
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"

        cur.execute(query, tuple(update_values))
        conn.commit()

        if cur.rowcount == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "User updated successfully!"}), 200

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@routes.route('/delete-user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        if cur.rowcount == 0:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"message": "User deleted successfully!"}), 200
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
