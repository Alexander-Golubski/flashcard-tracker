from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
    
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flashcard-tracker:flashcard@localhost:3306/flashcard-tracker'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'c3c61aba99efb<1ce484af{=k.'

db = SQLAlchemy(app)

login_manager = LoginManager()

from . import views