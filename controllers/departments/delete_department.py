from flask import request, jsonify
import psycopg2
from config.database import connect_db

def delete_department(dep_id):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM departments WHERE id = %s", (dep_id,))
        conn.commit()
        if cur.rowcount == 0:
            return jsonify({"error": "Department not found"}), 404
        return jsonify({"message": "Department deleted successfully!"}), 200
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
