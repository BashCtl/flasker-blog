from flask import Blueprint, flash, redirect, render_template, url_for, abort, request, current_app
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.utils import secure_filename
import uuid
import os

from src import db, bcrypt
from src.models.user_model import User
from src.forms.webforms import UserForm, LoginForm, NameForm, SearchForm

users = Blueprint("users", __name__)

UPLOAD_FOLDER = "static/images"


@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            # check password hash
            if bcrypt.check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Successful.", category="success")
                return redirect(url_for("users.dashboard"))
            else:
                flash("Wrong Password - Try Again!", category="warning")
        else:
            flash("That User Doesn't Exist! Try Again!", category="warning")
    return render_template("login.html", form=form)


@users.route("/users/", methods=["GET", "POST"])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                        favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
            flash("User added successfully!", category="success")
        name = form.name.data
        form.username.data = ""
        form.name.data = ""
        form.email.data = ""
        form.favorite_color.data = ""
        form.password.data = ""

    users = User.query.order_by(User.created_at)
    return render_template("add_user.html", form=form, name=name, users=users)


@users.route("/users/<int:user_id>", methods=["GET", "POST"])
@login_required
def update_user(user_id):
    form = UserForm()
    user_to_update = User.query.get_or_404(user_id)
    if request.method == "POST":
        user_to_update.name = request.form["name"]
        user_to_update.username = request.form["username"]
        user_to_update.email = request.form["email"]
        user_to_update.favorite_color = request.form["favorite_color"]
        try:
            db.session.commit()
            flash("User Updated Successfully!", category="success")
            return render_template("update.html", form=form, user_to_update=user_to_update)
        except:
            flash("Error. Something went wrong during update!", category="success")
            return render_template("update.html", form=form, user_to_update=user_to_update)
    else:
        # form.name.data = user_to_update.name
        # form.email.data = user_to_update.email
        return render_template("update.html", form=form, user_to_update=user_to_update)


@users.route("/delete/<int:user_id>")
@login_required
def delete_user(user_id):
    name = None
    form = UserForm()
    user_to_delete = User.query.get_or_404(user_id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!!", category="success")
        users = User.query.order_by(User.created_at)
        return render_template("add_user.html", form=form, name=name, users=users)
    except:
        flash("There was a problem deleting user, try again.", category="warning")
    users = User.query.order_by(User.created_at)
    return render_template("add_user.html", form=form, name=name, users=users)


@users.route("/admin")
@login_required
def admin():
    if current_user.is_admin:
        return render_template("admin.html")
    return render_template("403.html")


@users.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = UserForm()
    user_id = current_user.id
    user_to_update = User.query.get_or_404(user_id)
    if request.method == "POST":
        user_to_update.name = request.form["name"]
        user_to_update.username = request.form["username"]
        user_to_update.email = request.form["email"]
        user_to_update.favorite_color = request.form["favorite_color"]
        user_to_update.about_author = request.form["about_author"]

        if request.files["profile_pic"]:
            user_to_update.profile_pic = request.files["profile_pic"]
            # Grab Image Name
            pic_filename = secure_filename(user_to_update.profile_pic.filename)
            pic_name = f"{str(uuid.uuid1())}_{pic_filename}"
            # Save That Image
            saver = request.files["profile_pic"]
            saver.save(os.path.join(current_app.config["UPLOAD_FOLDER"], pic_name))
            user_to_update.profile_pic = pic_name
        try:
            db.session.commit()

            flash("User Updated Successfully!", category="success")
            return render_template("dashboard.html", form=form, user_to_update=user_to_update)
        except:
            flash("Error. Something went wrong during update!", category="success")
            return render_template("dashboard.html", form=form, user_to_update=user_to_update)
    else:
        # form.name.data = user_to_update.name
        # form.email.data = user_to_update.email
        return render_template("dashboard.html", form=form, user_to_update=user_to_update)


# Logout Page
@users.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out!", category="success")
    return redirect(url_for("users.login"))


@users.route("/user/<name>")
def user(name):
    return render_template("user.html", user_name=name)


@users.route("/name", methods=["GET", "POST"])
def name_page():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        flash("Form Submitted Successfully.", category="success")
    return render_template("name.html", name=name, form=form)
