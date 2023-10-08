from flask import Blueprint, render_template
from flask_login import login_required, current_user

from src.forms.webforms import UserForm, LoginForm, EditUserForm
from src.services.users_service import UserService

users = Blueprint("users", __name__)

UPLOAD_FOLDER = "static/images"


@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return UserService.user_login(form)


@users.route("/register/", methods=["GET", "POST"])
def add_user():
    form = UserForm()
    return UserService.registration(form)


@users.route("/users/<int:user_id>", methods=["GET", "POST"])
@login_required
def update_user(user_id):
    form = UserForm()
    return UserService.update_user(form, user_id)


@users.route("/delete/<int:user_id>")
@login_required
def delete_user(user_id):
    return UserService.delete_user(user_id)


@users.route("/admin")
@login_required
def admin():
    if current_user.is_admin:
        all_users = UserService.get_all_users()
        return render_template("admin.html", users=all_users)
    return render_template("403.html")


@users.route("/admin/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    if current_user.is_admin:
        return UserService.edit_by_admin(user_id)
    return render_template("403.html")


@users.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = UserForm()
    user_id = current_user.id
    return UserService.user_dashboard(form, user_id)


# Logout Page
@users.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    return UserService.user_logout()


@users.route("/")
def index():
    return render_template("index.html")
