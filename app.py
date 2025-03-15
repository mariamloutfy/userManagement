from flask import Flask
from flask_cors import CORS
from routes import routes, auth_routes  

app = Flask(__name__)
CORS(app)  # Allow all origins

app.register_blueprint(routes)
app.register_blueprint(auth_routes)

if __name__ == "__main__":
    app.run(debug=True)
