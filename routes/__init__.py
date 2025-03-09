from flask import Blueprint
from .users import users_bp

# Create a Blueprint to group all routes
routes_bp = Blueprint("routes", __name__)

# Register user routes
routes_bp.register_blueprint(users_bp)
