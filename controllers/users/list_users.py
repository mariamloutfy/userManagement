from flask import jsonify
import psycopg2
from config.database import connect_db

def get_users():
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT u.id, u.username, u.email, u.phone,u.gender, d.departmentname 
            FROM users u
            LEFT JOIN departments d ON u.department_id = d.id
        """)
        users = cur.fetchall()
        
        if not users:
            return jsonify({"message": "No users found"}), 404

        user_list = [
            {
                "id": user[0], 
                "username": user[1], 
                "email": user[2], 
                "phone": user[3], 
                "gender": user[4] ,
                "department":user[5] if user[5] else "No Department"
            }
            for user in users
        ]

        return jsonify(user_list), 200
    except psycopg2.Error as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        cur.close()
        conn.close()
