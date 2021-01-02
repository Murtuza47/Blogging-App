from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRETKEY'


@app.route("/")
def index():
    return render_template("base.html")


@app.route("/post")
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
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("post"))
    return render_template("registrationForm.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
