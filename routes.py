from flask import Blueprint
from controllers.users.create_user import create_user
from controllers.users.get_user import get_user
from controllers.users.list_users import get_users
from controllers.users.update_user import update_user
from controllers.users.delete_user import delete_user
from controllers.auth.login import login 

routes = Blueprint("routes", __name__)

routes.route('/users', methods=['POST'])(create_user)
routes.route('/users/<int:user_id>', methods=['GET'])(get_user)
routes.route('/users', methods=['GET'])(get_users)
routes.route('/users/<int:user_id>', methods=['PUT'])(update_user)
routes.route('/users/<int:user_id>', methods=['DELETE'])(delete_user)

# Authentication routes
auth_routes = Blueprint("auth", __name__)

@auth_routes.route("/login", methods=["POST"])
def login_route():
    return login()
