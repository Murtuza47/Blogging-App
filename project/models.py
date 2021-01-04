from project import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(200), default="default.png")
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User <{self.username}>"


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.DATETIME(), default=datetime.utcnow)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post <{self.title}>"

