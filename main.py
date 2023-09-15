from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("SECRET_KEY")


# Create a Form Class
class NameForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


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
