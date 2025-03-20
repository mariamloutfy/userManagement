from flask import request, jsonify
import psycopg2
from config.database import connect_db

def get_department(dep_id):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT id, departmentname, isactive FROM departments WHERE id = %s", (dep_id,))
        department = cur.fetchone()
        if not department:
            return jsonify({"error": "Department not found"}), 404
        dep_data = {
            "id": department[0],
            "depname": department[1],
            "isActive": department[2]
        }
        return jsonify(dep_data), 200
    except psycopg2.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        cur.close()
        conn.close()
