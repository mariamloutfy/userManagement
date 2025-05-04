from flask import request, jsonify
import psycopg2

from utils import is_valid_email
from core.database.fetch_one import fetch_one 

def get_user(user_id):
    try:
        query = """
            SELECT u.id, u.username, u.email, u.phone, u.gender, d.departmentname 
            FROM users u 
            LEFT JOIN departments d ON u.department_id = d.id
            WHERE u.id = %s
        """
        user = fetch_one(query, (user_id,))
        
        if not user:
            return jsonify({"error": "User not found"}), 404

        user_data = {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "phone": user[3],
            "gender": user[4],
            "department": user[5]
        }

        return jsonify(user_data), 200
    except psycopg2.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
