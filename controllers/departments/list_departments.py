from flask import jsonify
import psycopg2
from core.database.fetch_all import fetch_all

def get_departments():
    try:
        query = """
            SELECT d.id, d.departmentname, d.isactive, COUNT(u.id) 
            FROM departments d 
            LEFT JOIN users u ON d.id = u.department_id
            GROUP BY d.id, d.departmentname, d.isactive
        """
        departments = fetch_all(query)

        if not departments:
            return jsonify({"message": "No departments found"}), 404

        department_list = [
            {
                "id": dep[0],
                "depname": dep[1],
                "isActive": dep[2],
                "userCount": dep[3]
            }
            for dep in departments
        ]

        return jsonify(department_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
