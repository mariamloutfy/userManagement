from flask import request, jsonify
from config.database import connect_db
from datetime import datetime
def update_comment(comment_id):
    try:
        data = request.json
        new_comment = data.get("comment")
        if not new_comment:
            return jsonify({"error": "No comment content provided"}), 400

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("UPDATE comments SET comment = %s WHERE id = %s", (new_comment, comment_id))
        conn.commit()

        if cur.rowcount == 0:
            return jsonify({"error": "Comment not found"}), 404
        return jsonify({"message": "Comment updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
