import re
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


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
            return jsonify({"error": "Username, email, password, and phone are required!"}), 400
        if not is_valid_email(email):
            return jsonify({"error": "Invalid email format!"}), 400
        new_user = {
            "username": username,
            "email": email,
            "phone": phone
        }
        print("Hello", new_user["username"]) # Log user creation to terminal
        return jsonify({"message": f"User {new_user['username']} created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500
if __name__ == "__main__":
    app.run(debug=True)
