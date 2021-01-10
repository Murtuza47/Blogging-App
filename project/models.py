from project import db, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as tSerializer

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(200), default="default.png")
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User <{self.username}>"

    def generate_token(self):
        s = tSerializer(app.config['SECRET_KEY'], 1800)
        return s.dumps({"user_id": self.id}).decode('utf-8')

    @staticmethod
    def get_token_and_verify(token):
        s = tSerializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)
        except:
            return None
        return User.query.get(user_id)




class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.DATETIME(), default=datetime.utcnow)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post <{self.title}>"

