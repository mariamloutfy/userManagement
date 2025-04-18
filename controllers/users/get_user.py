from flask import request, jsonify
import psycopg2
from config.database import connect_db
from utils import is_valid_email

def get_user(user_id):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT u.id, u.username, u.email, u.phone,u.gender, d.departmentname 
            FROM users u 
            LEFT JOIN departments d ON u.department_id = d.id
            WHERE u.id = %s
        """, (user_id,))
        
        user = cur.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404
        user_data = {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "phone": user[3],
            "gender":user[4],
            "department": user[5]  # Returns department name instead of ID
        }

        return jsonify(user_data), 200
    except psycopg2.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        cur.close()
        conn.close()
