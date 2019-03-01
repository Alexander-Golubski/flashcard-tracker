from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

def flask_app():

    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flashcard-tracker:flashcard@localhost:8889/flashcard-tracker'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)
    app.secret_key = 'y337kGcys&zP3B'

    app.run()

if __name__ == '__main__':
    flask_app()