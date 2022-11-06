from flask import Blueprint, render_template, redirect, url_for , request, flash
from . import db
from .datamodel import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():  
    if request.method == 'POST':
            email = request.form.get("email")
            password = request.form.get("password")

            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    flash("Logged in!", category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('blog.home'))
                else:
                        flash('Password is incorrect.', category='error')
            else:
                flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route("/signup", methods=['GET', 'POST'])
def sign_up():
    if request.method =='POST':     
        first_name= request.form.get("first_name")
        last_name= request.form.get("last_name")
        username= request.form.get("username")
        email= request.form.get("email")
        age= request.form.get("age")
        password= request.form.get("password")
        password1= request.form.get("password1")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif password != password1:
            flash('Password don\'t match!', category='error')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        elif len(password1) < 2:
            flash('Password is too short.', category='error')
        elif len(email) < 2:
            flash("Email is invalid.", category='error')
        else:
            new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, age=age, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!')
            return redirect(url_for('blog.home'))

    return render_template("signup.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("blog.home"))