from flask import flash, render_template, redirect, url_for
from flask_login import login_required, current_user
from src.models.post_model import Post
from src.forms.webforms import PostForm, SearchForm
from src import db


class PostService:

    @staticmethod
    def create_post(form):
        if form.validate_on_submit():
            post = Post(title=form.title.data, content=form.content.data,
                        user_id=current_user.id, slug=form.slug.data)
            db.session.add(post)
            db.session.commit()
            flash("Blog Post Submitted Successfully!", category="success")
            return redirect(url_for("posts.create_post"))
        return render_template("create_post.html", form=form)

    @staticmethod
    def render_all_posts():
        posts = Post.query.order_by(Post.created_at)
        return render_template("posts.html", posts=posts)

    @staticmethod
    def view_post_by_id(post_id):
        post = Post.query.get_or_404(post_id)
        return render_template("post.html", post=post)

    @staticmethod
    def edit_post(post_id):
        post = Post.query.get_or_404(post_id)
        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.slug = form.slug.data
            post.content = form.content.data
            db.session.add(post)
            db.session.commit()
            flash("Post Has Been Updated!", category="success")
            return redirect(url_for("posts.get_post", post_id=post_id))
        if current_user.id == post.user.id:
            form.content.data = post.content
            return render_template("edit_post.html", form=form, post=post)
        else:
            return render_template("403.html")

    @staticmethod
    def delete_post(post_id):
        post_to_delete = Post.query.get_or_404(post_id)
        if current_user.id == post_to_delete.user.id or current_user.is_admin:
            try:
                db.session.delete(post_to_delete)
                db.session.commit()
                flash("Blog Post Was Deleted!", category="success")
                return redirect(url_for("posts.show_posts"))
            except:
                flash("There was a problem deleting post.", category="warning")
        posts = Post.query.order_by(Post.created_at)
        return render_template("posts.html", posts=posts)

    @staticmethod
    def search_post():
        global searched
        form = SearchForm()
        posts = Post.query
        if form.validate_on_submit():
            searched = form.searched.data
            posts = posts.filter(Post.content.like(f"%{searched}%"))
            posts = posts.order_by(Post.title).all()
        return render_template("search.html", form=form, searched=searched, posts=posts)
