from flask import request, jsonify
from config.database import connect_db
from datetime import datetime
def delete_comment(comment_id):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM comments WHERE id = %s", (comment_id,))
        conn.commit()

        if cur.rowcount == 0:
            return jsonify({"error": "Comment not found"}), 404
        return jsonify({"message": "Comment deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
