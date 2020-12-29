from flask import Flask, render_template

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(debug=True)
