from project import app, bcrypt, db, login_manager, mail
from flask import render_template, flash, redirect, url_for, request, abort
from project.forms import RegistrationForm, LoginForm, UpdateForm, PostForm, RequestPasswordFrom, ResetPasswordForm
from project.models import User, Post
from flask_login import login_user, logout_user, login_required, current_user
from helper_function.image_loader import image_loader
from flask_mail import Message


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


@app.route("/")
@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page=5)
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post'))
    return render_template("posts.html", posts=posts, form=form)


@app.route("/post/edit/<int:id>", methods=["GET", "POST"])
def edit_post(id):
    post = Post.query.get_or_404(int(id))
    if post.author.email != current_user.email:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for("post"))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("edit_post.html", form=form)


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
            next = request.args.get('next')
            if next is None and next[0] == '/':
                return redirect(url_for('post'))
            return redirect(next)
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
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template('account.html', form=form, image=image)


@app.route("/post-detail/<int:id>")
def post_detail(id):
    post = Post.query.get_or_404(int(id))
    return render_template("post_detail.html", post=post)


@app.route("/post-delete/<int:id>")
def post_delete(id):
    post = Post.query.get_or_404(int(id))
    if post.author.email != current_user.email:
        abort(403)
    if post:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted")
        return redirect(url_for('post'))
    return render_template("post_detail.html", post=post)


@app.route('/author/<string:username>', methods=['GET', 'POST'])
@login_required
def user_posts(username):
    form = PostForm()
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    if user.email != current_user.email:
        abort(403)
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('user_posts', username=current_user.username))
    post = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_post.html', posts=post, user=user, form=form)


@app.route("/request-reset-password", methods=['GET', 'POST'])
def request_new_pass():
    if current_user.is_authenticated:
        return redirect(url_for("post"))
    form = RequestPasswordFrom()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data)
        send_mail(user)
        flash('A Password Reset Url has been sent to your email')
        return redirect(url_for('reset_new_pass'))
    return render_template('request_new_pass.html', form=form)


def send_mail(user):
    token = user.generate_token()
    msg = Message('Password Reset Request', sender='a.murtuza007@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password please click the following link 
{url_for('reset_new_pass', token=token, )}
If you dont make this request kindly plaese dont click this link. No changes will be made
    '''
    mail.send(msg)

@app.route("/reset-password/<token>", methods=['GET', 'POST'])
def reset_new_pass(token):
    if current_user.is_authenticated:
        return redirect(url_for("post"))
    user = User.get_token_and_verify(token)
    if user is None:
        flash("Invaild token or token has been expired")
        redirect(url_for('request_new_pass'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = password
        db.session.commit()
        flash('Password has been updated, and now you can login')
        return redirect(url_for('login'))
    return render_template('reset_new_pass.html', form=form)
