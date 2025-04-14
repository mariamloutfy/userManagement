from flask import Blueprint
from controllers.users.create_user import create_user
from controllers.users.get_user import get_user
from controllers.users.list_users import get_users
from controllers.users.update_user import update_user
from controllers.users.delete_user import delete_user
from controllers.users.assign_department import assign_user_to_department
from controllers.auth.login import login 

from controllers.departments.create_department import create_department
from controllers.departments.delete_department import delete_department
from controllers.departments.get_department import get_department
from controllers.departments.list_departments import get_departments
from controllers.departments.update_department import update_department

from controllers.posts.create_posts import create_post
from controllers.posts.list_posts import get_posts
from controllers.posts.get_post import get_post
from controllers.posts.update_post import update_post
from controllers.posts.delete_post import delete_post

from controllers.comments.create_comment import create_comment
from controllers.comments.list_comments import get_comments
from controllers.comments.get_comment import get_comment
from controllers.comments.update_comment import update_comment
from controllers.comments.delete_comment import delete_comment


routes = Blueprint("routes", __name__)

# User routes
routes.route('/users', methods=['POST'])(create_user)
routes.route('/users/<int:user_id>', methods=['GET'])(get_user)
routes.route('/users', methods=['GET'])(get_users)
routes.route('/users/<int:user_id>', methods=['PUT'])(update_user)
routes.route('/users/<int:user_id>', methods=['DELETE'])(delete_user)
routes.route('/users/<int:user_id>/assign_department', methods=['PUT'])(assign_user_to_department)
# Department routes
routes.route('/departments', methods=['POST'])(create_department) 
routes.route('/departments/<int:dep_id>', methods=['DELETE'])(delete_department)
routes.route('/departments/<int:dep_id>', methods=['GET'])(get_department)
routes.route('/departments', methods=['GET'])(get_departments)
routes.route('/departments/<int:dep_id>', methods=['PUT'])(update_department)
# Post routes
routes.route('/posts', methods=['POST'])(create_post)
routes.route('/posts', methods=['GET'])(get_posts) 
routes.route('/posts/<int:post_id>', methods=['GET'])(get_post)  
routes.route('/posts/<int:post_id>', methods=['PUT'])(update_post)
routes.route('/posts/<int:post_id>', methods=['DELETE'])(delete_post)
# Comment routes
routes.route('/comments', methods=['POST'])(create_comment)
routes.route('/comments', methods=['GET'])(get_comments)
routes.route('/comments/<int:comment_id>', methods=['GET'])(get_comment)
routes.route('/comments/<int:comment_id>', methods=['PUT'])(update_comment)
routes.route('/comments/<int:comment_id>', methods=['DELETE'])(delete_comment)


# Authentication routes
auth_routes = Blueprint("auth", __name__)

@auth_routes.route("/login", methods=["POST"])
def login_route():
    return login()
