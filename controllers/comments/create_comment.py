from flask import request, jsonify
from config.database import connect_db
from datetime import datetime

def create_comment():
    try:
        data = request.json
        comment = data.get("comment")
        created_by = data.get("created_by")
        post_id = data.get("post_id")

        if not comment or not created_by or not post_id:
            return jsonify({"error": "Missing required fields"}), 400

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO comments (comment, created_by, post_id, created_at) 
            VALUES (%s, %s, %s, %s) RETURNING id
        """, (comment, created_by, post_id, datetime.utcnow()))
        comment_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Comment added", "comment_id": comment_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
