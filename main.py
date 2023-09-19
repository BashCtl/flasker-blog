from flask import Flask, render_template, flash, request, redirect
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
from os import getenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
# Add Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = getenv("SECRET_KEY")

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Create Model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email})"


# Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    submit = SubmitField("Submit")


# Create a Form Class
class NameForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Update Database Record
@app.route("/users/<int:user_id>", methods=["GET", "POST"])
def update_user(user_id):
    form = UserForm()
    user_to_update = User.query.get_or_404(user_id)
    if request.method == "POST":
        user_to_update.name = request.form["name"]
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


@app.route("/users/", methods=["GET", "POST"])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data)
            db.session.add(user)
            db.session.commit()
            flash("User added successfully!", category="success")
        name = form.name.data
        form.name.data = ""
        form.email.data = ""
        form.favorite_color.data = ""

    users = User.query.order_by(User.created_at)
    return render_template("add_user.html", form=form, name=name, users=users)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/user/<name>")
def user(name):
    return render_template("user.html", user_name=name)


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Internal Server Error
@app.errorhandler(500)
def page_internal_server_error(e):
    return render_template("500.html"), 500


# Create Name Page
@app.route("/name", methods=["GET", "POST"])
def name_page():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        flash("Form Submitted Successfully.", category="success")
    return render_template("name.html", name=name, form=form)


if __name__ == "__main__":
    app.run(host="localhost", debug=True)
