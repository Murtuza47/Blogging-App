from project import app, bcrypt, db, login_manager
from flask import render_template, flash, redirect, url_for, request
from project.forms import RegistrationForm, LoginForm, UpdateForm
from project.models import User
from flask_login import login_user, logout_user, login_required, current_user
from helper_function.image_loader import image_loader

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


@app.route("/")
@app.route("/post")
@login_required
def post():
    posts = [
        {
            "author": "Ali",
            "date_posted": "22 June",
            "content": "This is my first blog",
            "title": "First Blog"
        }
    ]
    return render_template("posts.html", posts=posts)


@app.route("/registration", methods=["GET", "POST"])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("login"))
    return render_template("registrationForm.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Welcome")
            return redirect(url_for("post"))
    return render_template("loginForm.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("login"))



@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.image_file.data:
            image_file = image_loader(form.image_file.data)
            current_user.image_file = image_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Profile has been updated!")
        return redirect("account")
    elif request.method =="GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template('account.html', form=form, image=image)
