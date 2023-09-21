from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, SubmitField, EmailField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from dotenv import load_dotenv
from os import getenv
from datetime import datetime, date

load_dotenv()

app = Flask(__name__)
# Add Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = getenv("SECRET_KEY")

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Rest Json example
@app.route("/date")
def get_current_date():
    return {"Date": date.today()}


# Create Model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError("Password is not a readable.")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email})"


# Create a Blog Post model
class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    slug = db.Column(db.String(255))


# Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    password = PasswordField("Password", validators=[DataRequired(),
                                                     EqualTo("password_confirm", message="Passwords Must Match!")])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a Form Class
class NameForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Password Form
class PasswordForm(FlaskForm):
    email = EmailField("What' Your Email.", validators=[DataRequired()])
    password = PasswordField("What's Your Password.", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create Post Form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Post page
@app.route("/add-post", methods=["GET", "POST"])
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,
                    author=form.author.data, slug=form.slug.data)
        form.title.data = ""
        form.content.data = ""
        form.author.data = ""
        form.slug.data = ""

        db.session.add(post)
        db.session.commit()

        flash("Blog Post Submitted Successfully!", category="success")
    return render_template("create_post.html", form=form)


@app.route("/posts")
def show_posts():
    posts = Post.query.order_by(Post.created_at)
    return render_template("posts.html", posts=posts)


@app.route("/posts/<int:post_id>")
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post)


@app.route("/posts/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        flash("Post Has Been Updated!", category="success")
        return redirect(url_for("get_post", post_id=post_id))
    form.content.data = post.content
    return render_template("edit_post.html", form=form, post=post)


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
            hashed_pw = generate_password_hash(form.password.data, "sha256")
            user = User(name=form.name.data, email=form.email.data,
                        favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
            flash("User added successfully!", category="success")
        name = form.name.data
        form.name.data = ""
        form.email.data = ""
        form.favorite_color.data = ""
        form.password.data = ""

    users = User.query.order_by(User.created_at)
    return render_template("add_user.html", form=form, name=name, users=users)


@app.route("/delete/<int:user_id>")
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


# Create Password Test Page
@app.route("/test_pw", methods=["GET", "POST"])
def test_pw():
    email = None
    password = None
    user_check = None
    passed = None
    form = PasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        form.email.data = ""
        form.password.data = ""

        user_check = User.query.filter_by(email=email).first()
        # Check Hashed Password
        passed = check_password_hash(user_check.password_hash, password)

        flash("Form Submitted Successfully.", category="success")
    return render_template("test_pw.html", form=form, email=email,
                           password=password, user_check=user_check, passed=passed)


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
