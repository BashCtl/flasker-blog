from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import login_required
from src.forms.webforms import PostForm
from src.models.post_model import Post
from src import db

posts = Blueprint("posts", __name__)


@posts.route("/add-post", methods=["GET", "POST"])
@login_required
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


@posts.route("/posts")
def show_posts():
    posts = Post.query.order_by(Post.created_at)
    return render_template("posts.html", posts=posts)


@posts.route("/posts/<int:post_id>")
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post)

@posts.route("/posts/edit/<int:post_id>", methods=["GET", "POST"])
@login_required
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
        return redirect(url_for("posts.get_post", post_id=post_id))
    form.content.data = post.content
    return render_template("edit_post.html", form=form, post=post)

@posts.route("/posts/delete/<int:post_id>")
def delete_post(post_id):
    post_to_delete = Post.query.get_or_404(post_id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Blog Post Was Deleted!", category="success")
        posts = Post.query.order_by(Post.created_at)
        return render_template("posts.html", posts=posts)
    except:
        flash("There was a problem deleting post.", category="warning")
        posts = Post.query.order_by(Post.created_at)
        return render_template("posts.html", posts=posts)

@posts.route("/")
def index():
    return render_template("index.html")