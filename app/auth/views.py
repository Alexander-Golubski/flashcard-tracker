# Third party imports
from flask import Flask, redirect, render_template, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, logout_user
# Local application imports
from forms import LoginForm, RegistrationForm
from models.user import User

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('app/templates/dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Welcome to Flashcard Tracker! You may now login.')

        return redirect(url_for('app.login'))

    return render_template('templates/register.html', form=form, title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(
                form.password.data):
            login_user(user)

            return redirect(url_for('home.dashboard'))

        else:
            flash('Invalid email or password.')

    return render_template('templates/login.html', form=form, title='Login')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully been logged out.')

    return redirect(url_for('profile-auth.login'))