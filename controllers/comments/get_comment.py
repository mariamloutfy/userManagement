
from flask import request, jsonify
from config.database import connect_db
from datetime import datetime
from core.database.fetch_one import fetch_one

def get_comment(comment_id):
    try:
        query = """
            SELECT c.id, c.comment, c.created_at, u.username, c.post_id
            FROM comments c
            JOIN users u ON c.created_by = u.id
            WHERE c.id = %s
        """
        row = fetch_one(query, (comment_id,))
        if not row:
            return jsonify({"error": "Comment not found"}), 404

        comment_data = {
            "id": row[0],
            "comment": row[1],
            "created_at": row[2],
            "author": row[3],
            "post_id": row[4]
        }
        return jsonify(comment_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
