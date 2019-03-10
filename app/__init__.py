from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://teach_sr:flashcard@localhost:8889/teach_sr'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'c3c61aba99efb<1ce484af{=k.'

db = SQLAlchemy()
db.init_app(app)

bootstrap = Bootstrap(app)

login_manager = LoginManager(app)

from . import views