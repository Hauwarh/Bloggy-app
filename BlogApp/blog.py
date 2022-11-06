from flask import Blueprint, render_template, request, flash, url_for, redirect
from . import db
from .datamodel import User
from .datamodel import Post
from .datamodel import Message
from flask_login import login_required, current_user





blog = Blueprint("blog", __name__)


@blog.route("/")
def home():
    posts = Post.query.all()
    return render_template("home.html",user=current_user, posts=posts)

@blog.route("/create-post",  methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get("title")
        author = request.form.get("author")
        content = request.form.get("content")

        if not title:
            flash("Title cannot be empty", category='error')
        if not author:
            flash("Author cannot be empty", category='error')
        if not content:
            flash("Content cannot be empty", category='error')
        else: 
            new_post = Post(title=title, author=author, content=content, created_by=current_user.id)
            db.session.add(new_post) 
            db.session.commit() 
            flash("Post created!", category="success") 
            return redirect(url_for('blog.home'))
        

    return render_template("create_post.html", user=current_user.username)   


@blog.route("/delete-post/<id>")
@login_required
def delete_post(id):
    # new_post = Post.query.filter_by(id=id).first()
    new_post = Post.query.get(id)
    id = current_user.id
   
    if not new_post: 
        flash("Post does not exist.", category='error')
    elif current_user.id != id:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(new_post)
        db.session.commit()
        flash('Post deleted.', category='success')
    posts = Post.query.order_by(Post.date_created)
    return redirect(url_for('blog.home', posts=posts))

@blog.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('blog.home'))

    posts = Post.query.filter_by(created_by=user.id).all()
    return render_template("posts.html", user=current_user, posts=posts, username=username)

@blog.route("/about")
def about():
    return render_template("about.html", user=current_user)

@blog.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        title = request.form.get('title')
        message = request.form.get('message')

        new_message = Message(name=name, email=email, title=title, message=message)
        db.session.add(new_message) 
        db.session.commit() 
        flash("Thanks for reaching out! We will get back to you.", category="success") 
        return redirect(url_for('blog.home'))
    return render_template("contact.html", user=current_user)

@blog.route('/edit/<int:id>/', methods=['GET', 'POST'])
@login_required
def edit(id):
    post_edit = Post.query.get(id)

    if current_user.id == post_edit.id:
        if request.method == 'POST':
            post_edit.title = request.form.get('title')
            post_edit.author= request.form.get('author')
            post_edit.content = request.form.get('content')
            
            db.session.add(post_edit)
            db.session.commit()

            flash("Post updated.")
            return redirect(url_for('blog.posts', id=post_edit.id))
        return render_template('edit.html', user=current_user, posts=posts)

