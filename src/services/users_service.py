import os
import uuid

from flask import redirect, render_template, flash, url_for, request, current_app
from flask_login import login_user, logout_user, current_user
from werkzeug.utils import secure_filename

from src import bcrypt, db
from src.models.user_model import User
from src.forms.webforms import EditUserForm, SearchForm


class UserService:

    @staticmethod
    def user_login(form):
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

    @staticmethod
    def registration(form):
        if form.validate_on_submit():
            user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
            if user is None:
                hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
                user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                            favorite_color=form.favorite_color.data, password_hash=hashed_pw)
                db.session.add(user)
                db.session.commit()
                flash("User added successfully!", category="success")
                return redirect(url_for("users.login"))
            else:
                flash("User already exists!", category="warning")
        return render_template("add_user.html", form=form)

    @staticmethod
    def update_user(form, user_id):
        user_to_update = User.query.get_or_404(user_id)
        if request.method == "POST":
            user_to_update.name = request.form["name"]
            user_to_update.username = request.form["username"]
            user_to_update.email = request.form["email"]
            user_to_update.favorite_color = request.form["favorite_color"]
            db.session.commit()
            flash("User Updated Successfully!", category="success")
            return redirect(url_for("users.dashboard"))
        else:
            return render_template("update.html", form=form, user_to_update=user_to_update)

    @staticmethod
    def delete_user(user_id):
        user_to_delete = User.query.get_or_404(user_id)
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User Deleted Successfully!!", category="success")
            if current_user.is_admin:
                return redirect(url_for("users.admin"))
            else:
                logout_user()
                return render_template("index.html")

    @staticmethod
    def user_dashboard(form, user_id):
        user_to_update = User.query.get_or_404(user_id)
        if request.method == "POST":
            UserService.__update_user_field(user_to_update)
            UserService.__update_user_picture(user_to_update)
            db.session.commit()
            flash("User Updated Successfully!", category="success")
            return render_template("dashboard.html", form=form, user_to_update=user_to_update)
        else:
            return render_template("dashboard.html", form=form, user_to_update=user_to_update)

    @staticmethod
    def user_logout():
        logout_user()
        flash("You Have Been Logged Out!", category="success")
        return redirect(url_for("users.login"))

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def edit_by_admin(user_id):
        form = EditUserForm()
        user = User.query.get_or_404(user_id)
        if request.method == "POST":
            user.name = form.name.data
            user.username = form.username.data
            user.email = form.email.data
            user.can_post = request.form["can_post"] == "True"
            user.is_admin = request.form["is_admin"] == "True"
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("users.admin"))
        form.name.data = user.name
        form.username.data = user.username
        form.email.data = user.email
        form.can_post.data = user.can_post
        form.is_admin.data = user.is_admin
        return render_template("edit_by_admin.html", form=form, user_id=user_id, user=user)

    @staticmethod
    def search_user():
        form = SearchForm()
        if form.validate_on_submit():
            username = form.searched.data
            user = User.query.filter_by(username=username).first()
            return render_template("admin.html", user=user, search_form=form)

    @staticmethod
    def __update_user_field(user_to_update):
        user_to_update.name = request.form["name"]
        user_to_update.username = request.form["username"]
        user_to_update.email = request.form["email"]
        user_to_update.favorite_color = request.form["favorite_color"]
        user_to_update.about_author = request.form["about_author"]

    @staticmethod
    def __update_user_picture(user_to_update):
        if request.files["profile_pic"]:
            user_to_update.profile_pic = request.files["profile_pic"]
            # Grab Image Name
            pic_filename = secure_filename(user_to_update.profile_pic.filename)
            pic_name = f"{str(uuid.uuid1())}_{pic_filename}"
            # Save That Image
            saver = request.files["profile_pic"]
            saver.save(os.path.join(current_app.config["UPLOAD_FOLDER"], pic_name))
            user_to_update.profile_pic = pic_name
