from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, RadioField, TextAreaField, FileField
from wtforms.validators import DataRequired, EqualTo


class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    about_author = TextAreaField("About Author")
    password = PasswordField("Password", validators=[DataRequired(),
                                                     EqualTo("password_confirm", message="Passwords Must Match!")])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    profile_pic = FileField("Profile Picture")
    submit = SubmitField("Submit")


class EditUserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    is_admin = RadioField("Is Admin", choices=[(True, "True"), (False, "False")],default=True, coerce=bool)
    can_post = RadioField("Can Post", choices=[(True, "True"), (False, "False")],default=True, coerce=bool)
    submit = SubmitField("Save")


# Create a Form Class
class NameForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Password Form
class PasswordForm(FlaskForm):
    email = EmailField("What' Your Email.", validators=[DataRequired()])
    password = PasswordField("What's Your Password.", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Login Form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create Post Form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = CKEditorField("Content", validators=[DataRequired()])
    # author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Search Form
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")
