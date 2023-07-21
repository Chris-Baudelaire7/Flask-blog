from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from apps import db
from apps.posts.forms import PostForm
from apps.models import Post


posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=["POST", "GET"])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Post created and posted", "success")
        return redirect(url_for('main.home'))
    return render_template("create_post.html", title="new-post", form=form, legend="Create post")


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title="Post details", post=post)


@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash("Attention, you aren't the author of this post, you can not edit it", "warning")
        return redirect(url_for("posts.post", post_id=post.id))
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post updated successfully", "success")
        return redirect(url_for("posts.post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title="Update post", form=form, legend="Update post")


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id) 
    if post.author != current_user:
        flash("Attention, you aren't the author of this post, you can not delete it", "info")
        return redirect(url_for("posts.post", post_id=post.id))
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted successfully", "success")
    return redirect(url_for("main.home"))