
from flask import request, jsonify
import psycopg2
from config.database import connect_db


def delete_post(post_id):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM posts WHERE id = %s", (post_id,))
        conn.commit()

        if cur.rowcount == 0:
            return jsonify({"error": "Post not found"}), 404
        return jsonify({"message": "Post deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
