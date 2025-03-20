from flask import request, jsonify
import psycopg2
from config.database import connect_db
from utils import is_valid_email
def assign_user_to_department(user_id):
    try:
        data = request.json
        department_id = data.get("department_id")
        if not department_id:
            return jsonify({"error": "Department ID is required!"}), 400
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            UPDATE users 
            SET department_id = %s 
            WHERE id = %s
        """, (department_id, user_id))
        conn.commit()
        if cur.rowcount == 0:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"message": "User assigned to department successfully!"}), 200
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()