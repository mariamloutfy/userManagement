from flask import request, jsonify
import psycopg2
from config.database import connect_db
def create_department():
    try:
        data = request.json
        depname = data.get("depname")
        isActive = data.get("isActive")
        if not depname or isActive is None:  # Make sure both fields are provided
            return jsonify({"error": "Missing required fields"}), 400
        # Validate data types
        if not isinstance(depname, str) or not isinstance(isActive, (bool, int)):
            return jsonify({"error": "Invalid data types"}), 400
        conn = connect_db()
        cur = conn.cursor()
        # Double-check table name and column names
        cur.execute("INSERT INTO departments (DepartmentName, isActive) VALUES (%s, %s) RETURNING id", 
                    (depname, isActive))
        dep_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Department Created", "department_id": dep_id}), 201
    except psycopg2.Error as db_err:
        print("Database Error:", db_err)
        return jsonify({"error": "Database error", "details": str(db_err)}), 500
    except Exception as e:
        print("Error in create_department:", str(e))  # More specific message
        return jsonify({"error": "Server error", "details": str(e)}), 500
