from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app():
    """
    initialize app with confirgurations
    """

    app = Flask(__name__)
    
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flashcard-tracker:flashcard@localhost:8889/flashcard-tracker'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.secret_key = 'c3c61aba99efb<1ce484af{=k.'
    
    return app