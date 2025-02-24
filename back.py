import psycopg2
import re
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

DB_NAME = "userdb"
DB_USER = "myuser"
DB_PASSWORD = "mypassword"
DB_HOST = "localhost"

def connect_db():
    return psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

def is_valid_email(email):
    email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(email_regex, email) is not None

@app.route('/create-user', methods=['POST'])
def create_user():
    try:
        data = request.json 
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        phone = data.get("phone")

        if not username or not email or not password or not phone:
            return jsonify({"error": "All fields are required!"}), 400

        if not is_valid_email(email):
            return jsonify({"error": "Invalid email format!"}), 400



        conn = connect_db()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users (username, email, password, phone) VALUES (%s, %s, %s, %s) RETURNING id",
                (username, email, password, phone),
            )
            user_id = cur.fetchone()[0]
            conn.commit()

            # ✅ Print the username after successful creation
            print(f"Hello {username}")

            return jsonify({"message": f"User {username} created successfully!", "user_id": user_id}), 201
        except psycopg2.Error as e:
            conn.rollback()
            if "duplicate key value" in str(e):
                return jsonify({"error": "Email already exists!"}), 400
            return jsonify({"error": "Database error", "details": str(e)}), 500
        finally:
            cur.close()
            conn.close()

    except Exception as e:
        print("🔥 ERROR:", str(e))  # Add this
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)