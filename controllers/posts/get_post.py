from flask import request, jsonify
import psycopg2
from config.database import connect_db

def get_post(post_id):
    try:
        conn = connect_db()
        cur = conn.cursor()

        # Get post and author
        cur.execute("""
            SELECT p.id, p.title, p.description, p.created_at, u.username
            FROM posts p
            JOIN users u ON p.created_by = u.id
            WHERE p.id = %s
        """, (post_id,))
        post = cur.fetchone()
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

        # Get comments
        cur.execute("""
            SELECT c.comment, c.created_at, u.username
            FROM comments c
            JOIN users u ON c.created_by = u.id
            WHERE c.post_id = %s
            ORDER BY c.created_at ASC
        """, (post_id,))
        comments = cur.fetchall()
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
