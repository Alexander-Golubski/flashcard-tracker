# Third party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
# Local application imports
from .key import key

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://teach_sr:flashcard@localhost:3306/teach_sr'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# key.py currently ignored by git
app.secret_key = key

db = SQLAlchemy(app)
db.init_app(app)

bootstrap = Bootstrap(app)

login_manager = LoginManager(app)

from . import views