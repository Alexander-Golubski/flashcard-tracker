from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flashcard-tracker:flashcard@localhost:8889/flashcard-tracker'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'c3c61aba99efb<1ce484af{=k.'

db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run()