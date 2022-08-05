from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


# create the application object
app = Flask(__name__)
app.config['SECRET_KEY'] = 'db2839ce189ba56681f9deb0c6bbcc3e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
login_manager = LoginManager()
 #Added this line fixed the issue.
login_manager.init_app(app)
login_manager.login_view = 'users.login'

from apion import routes