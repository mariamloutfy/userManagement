from flask import request, jsonify
import psycopg2
from config.database import connect_db

def get_posts():
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                p.id, p.title, p.description, p.created_at, u.username,
                COUNT(c.id) AS comment_count
            FROM posts p
            JOIN users u ON p.created_by = u.id
            LEFT JOIN comments c ON p.id = c.post_id
            GROUP BY p.id, u.username
            ORDER BY p.created_at DESC
        """)
        posts = cur.fetchall()
        post_list = [
            {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "created_at": row[3],
                "author": row[4],
                "total_comments": row[5]
            } for row in posts
        ]
        return jsonify(post_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
