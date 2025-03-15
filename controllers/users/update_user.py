from flask import request, jsonify
import psycopg2
from config.database import connect_db
from utils import is_valid_email
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
