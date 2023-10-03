from flask import redirect, render_template, flash, url_for
from flask_login import login_user
from sqlalchemy import or_
from src.models.user_model import User
from src import bcrypt, db


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
