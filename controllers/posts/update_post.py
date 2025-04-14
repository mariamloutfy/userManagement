
from flask import request, jsonify
import psycopg2
from config.database import connect_db

def update_post(post_id):
    try:
        data = request.json
        title = data.get("title")
        description = data.get("description")
        if not title and not description:
            return jsonify({"error": "Nothing to update"}), 400

        updates = []
        values = []
        if title:
            updates.append("title = %s")
            values.append(title)
        if description:
            updates.append("description = %s")
            values.append(description)
        values.append(post_id)

        conn = connect_db()
        cur = conn.cursor()
        query = f"UPDATE posts SET {', '.join(updates)} WHERE id = %s"
        cur.execute(query, tuple(values))
        conn.commit()

        if cur.rowcount == 0:
            return jsonify({"error": "Post not found"}), 404
        return jsonify({"message": "Post updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
