"""
Initializes app
Contains settings
"""

# Third party imports
import sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
# Local application imports
from .key import key, uri

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = sqlalchemy.create_engine(uri)

# key.py currently ignored by git
app.secret_key = key

db = SQLAlchemy(app)
db.init_app(app)

bootstrap = Bootstrap(app)

login_manager = LoginManager(app)

from . import views
