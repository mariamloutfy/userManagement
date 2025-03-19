from flask import Blueprint
from controllers.users.create_user import create_user
from controllers.users.get_user import get_user
from controllers.users.list_users import get_users
from controllers.users.update_user import update_user
from controllers.users.delete_user import delete_user
from controllers.auth.login import login 

from controllers.departments.create_department import create_department
from controllers.departments.delete_department import delete_department
from controllers.departments.get_department import get_department
from controllers.departments.list_departments import get_departments
from controllers.departments.update_department import update_department


routes = Blueprint("routes", __name__)

# User routes
routes.route('/users', methods=['POST'])(create_user)
routes.route('/users/<int:user_id>', methods=['GET'])(get_user)
routes.route('/users', methods=['GET'])(get_users)
routes.route('/users/<int:user_id>', methods=['PUT'])(update_user)
routes.route('/users/<int:user_id>', methods=['DELETE'])(delete_user)

# Department routes
routes.route('/departments', methods=['POST'])(create_department) 
routes.route('/departments/<int:dep_id>', methods=['DELETE'])(delete_department)
routes.route('/departments/<int:dep_id>', methods=['GET'])(get_department)
routes.route('/departments', methods=['GET'])(get_departments)
routes.route('/departments/<int:dep_id>', methods=['PUT'])(update_department)
# Authentication routes
auth_routes = Blueprint("auth", __name__)

@auth_routes.route("/login", methods=["POST"])
def login_route():
    return login()
