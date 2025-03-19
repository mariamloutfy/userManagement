from flask import request, jsonify
import psycopg2
from config.database import connect_db

def update_department(dep_id):
    conn = None
    cur = None
    try:
        data = request.json
        depname = data.get("depname")
        isActive = data.get("isActive")
        if not depname and not isActive:
            return jsonify({"error": "At least one field (depname, isActive) is required!"}), 400
        conn = connect_db()
        cur = conn.cursor()
        update_fields = []
        update_values = []
        if depname:
            update_fields.append("depname = %s")
            update_values.append(depname)
        if isActive:
            update_fields.append("isActive = %s")
            update_values.append(isActive)
        update_values.append(dep_id)
        query = f"UPDATE departments SET {', '.join(update_fields)} WHERE id = %s"
        cur.execute(query, tuple(update_values))
        conn.commit()
        if cur.rowcount == 0:
            return jsonify({"error": "Department not found"}), 404
        return jsonify({"message": "Department updated successfully!"}), 200
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
