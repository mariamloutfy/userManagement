from flask import request, jsonify
from config.database import connect_db
from datetime import datetime
def create_post():
    try:
        data = request.json
        title = data.get("title")
        description = data.get("description")
        created_by = data.get("created_by")
        if not title or not description or not created_by:
            return jsonify({"error": "Missing required fields"}), 400
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO posts (title, description, created_by, created_at) 
            VALUES (%s, %s, %s, %s) RETURNING id
        """, (title, description, created_by, datetime.utcnow()))
        post_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Post created", "post_id": post_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
