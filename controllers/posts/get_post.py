from flask import request, jsonify
import psycopg2
from core.database.fetch_one import fetch_one
from core.database.fetch_all import fetch_all

def get_post(post_id):
    try:
        # Fetch post and author
        post_query = """
            SELECT p.id, p.title, p.description, p.created_at, u.username
            FROM posts p
            JOIN users u ON p.created_by = u.id
            WHERE p.id = %s
        """
        post = fetch_one(post_query, (post_id,))
        if not post:
            return jsonify({"error": "Post not found"}), 404

        post_data = {
            "id": post[0],
            "title": post[1],
            "description": post[2],
            "created_at": post[3],
            "author": post[4],
            "comments": []
        }

        # Fetch comments
        comment_query = """
            SELECT c.comment, c.created_at, u.username
            FROM comments c
            JOIN users u ON c.created_by = u.id
            WHERE c.post_id = %s
            ORDER BY c.created_at ASC
        """
        comments = fetch_all(comment_query, (post_id,))
        post_data["comments"] = [
            {
                "comment": c[0],
                "created_at": c[1],
                "author": c[2]
            } for c in comments
        ]

        return jsonify(post_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
