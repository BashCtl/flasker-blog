from flask import redirect, render_template, flash, url_for
from flask_login import login_user
from src.models.user_model import User
from src import bcrypt
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