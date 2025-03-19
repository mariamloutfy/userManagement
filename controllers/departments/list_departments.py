from flask import request, jsonify
import psycopg2
from config.database import connect_db

def get_departments():
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT id, depname, isActive FROM departments")
        departments = cur.fetchall()
        if not departments:
            return jsonify({"message": "No departments found"}), 404
        department_list = [
            {"id": department[0], "depname": department[1], "isActive": department[2]}
            for department in departments
        ]
        return jsonify(department_list), 200
    except psycopg2.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        cur.close()
        conn.close()