from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from run-app import flask_app, db, app

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from profile-auth import LoginForm, RegistrationForm
from run-app import db
from models import User


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        return redirect(url_for('auth.login'))

    return render_template('templates/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
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

    return render_template('templates/log-in.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully been logged out.')

    return redirect(url_for('auth.login'))