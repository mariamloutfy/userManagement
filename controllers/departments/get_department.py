from flask import jsonify
import psycopg2
from config.database import connect_db

def get_department(dep_id):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT d.id, d.departmentname, d.isactive, COUNT(u.id) 
            FROM departments d 
            LEFT JOIN users u ON d.id = u.department_id
            WHERE d.id = %s
            GROUP BY d.id, d.departmentname, d.isactive
        """, (dep_id,))
        
        department = cur.fetchone()
        if not department:
            return jsonify({"error": "Department not found"}), 404

        dep_data = {
            "id": department[0],
            "depname": department[1],
            "isActive": department[2],
            "userCount": department[3]  # Adding user count
        }

        return jsonify(dep_data), 200
    except psycopg2.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        cur.close()
        conn.close()
