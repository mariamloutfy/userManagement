from flask import request, jsonify
from config.database import connect_db
from datetime import datetime
from core.database.fetch_all import fetch_all

def get_comments():
    try:
        query = """
            SELECT c.id, c.comment, c.created_at, u.username, c.post_id
            FROM comments c
            JOIN users u ON c.created_by = u.id
            ORDER BY c.created_at DESC
        """
        comments = fetch_all(query)

        comment_list = [
            {
                "id": row[0],
                "comment": row[1],
                "created_at": row[2],
                "author": row[3],
                "post_id": row[4]
            } for row in comments
        ]
        return jsonify(comment_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
