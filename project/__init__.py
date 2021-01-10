from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRETKEY'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'a.murtuza007@gmail.com  '
app.config['MAIL_PASSWORD'] = 'california2218287'
app.config['MAIL_USE_TLS'] = True
mail = Mail(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = 'info'
db = SQLAlchemy(app)

from project import routes
