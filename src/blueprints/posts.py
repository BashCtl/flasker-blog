from flask import Blueprint, render_template
from flask_login import login_required, current_user

from src.forms.webforms import PostForm
from src.services.post_service import PostService

posts = Blueprint("posts", __name__)


@posts.route("/add-post", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()
    if current_user.can_post:
        return PostService.create_post(form)
    return render_template("403.html")


@posts.route("/posts")
def show_posts():
    return PostService.render_all_posts()


@posts.route("/posts/<int:post_id>")
def get_post(post_id):
    return PostService.view_post_by_id(post_id)


@posts.route("/posts/edit/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    return PostService.edit_post(post_id)


@posts.route("/posts/delete/<int:post_id>")
@login_required
def delete_post(post_id):
    return PostService.delete_post(post_id)


@posts.route("/search", methods=["POST"])
def search():
    return PostService.search_post()
