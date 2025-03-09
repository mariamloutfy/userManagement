from flask import Blueprint
from routes.users import users_bp  # Import your users blueprint

routes_bp = Blueprint("routes", __name__)

# Register the users blueprint
routes_bp.register_blueprint(users_bp, url_prefix="/users")
