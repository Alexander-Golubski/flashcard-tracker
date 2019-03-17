"""
Contains all views, including:
/register, /login, /logout, /dashboard, /create-deck, /deck, /add-card
"""

# Third party imports
from flask import Flask, redirect, render_template, session, flash, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, logout_user, current_user
# Local application imports
from . import app, db
from .forms import LoginForm, RegistrationForm, CreateDeckForm, AddCardForm, CreateClassForm
from .models import User, Deck, Card, Class, load_user


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Route handler for registration
    Add user to the database
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        # create user
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password_hash=form.password.data)
        # add user to the database
        db.session.add(user)
        db.session.commit()
        flash('Welcome to Flashcard Tracker! You may now login.')

        return redirect(url_for('login'))

    return render_template('register.html', form=form, title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route handler for logging in
    Validates user login information
    """
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        # if user is not None and user.verify_password(form.password.data):
        if user is not None and user.password_hash == form.password.data:
            login_user(user)

            return redirect(url_for('dashboard'))

        else:
            flash('Invalid email or password.')

    return render_template('login.html', form=form, title='login')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully been logged out.')

    return redirect(url_for('login.html'))


@app.route('/dashboard')
@login_required
def dashboard():
    """
    Displays the dashboard view
    From the dashboard, user can access:
    Review Flashcards, Decks, and Monitoring
    """
    user = current_user
    decks = Deck.query.filter_by(owner_id=current_user.id).all()

    return render_template('dashboard.html', decks=decks, user=user)


@app.route('/create-deck', methods=['GET', 'POST'])
@login_required
def create_deck():
    """
    Creates decks and assigns them to current user_id (inner join)
    """
    form = CreateDeckForm()
    if form.validate_on_submit():
        # create deck
        deck = Deck(name=form.name.data, owner=current_user)
        # add deck to the database
        db.session.add(deck)
        db.session.commit()
        flash('Deck successfully created')

        return redirect(url_for('dashboard'))

    return render_template('create-deck.html', form=form, title='create deck')


@app.route('/deck', methods=['GET', 'POST'])
@login_required
def deck():
    """
    Displays view of deck
    From here, users can:
    Add, edit, assign, and delete cards from decks and access settings
    """

    # Get currently selected deck
    deck_id = request.args.get('id')
    deck = Deck.query.filter_by(id=deck_id).first()
    # Display list of cards in deck using model's backref attribute
    cards = deck.cards
    # Get list of the user's owned classes for dropdown menu
    classes = current_user.classes

    if request.method == 'POST':
        # Get checkbox'd cards
        sel_cards = request.form.getlist('sel_cards')
        # Get selected class
        sel_class = request.form.get('sel_class')
        # Add cards to selected class
        for card in sel_cards:
            card.classes.append(sel_class)
            db.session.commit()
            flash('Cards successfully added')
        return redirect(url_for('dashboard'))

    return render_template('deck.html', deck=deck, cards=cards, classes=classes)


@app.route('/add-card', methods=['GET', 'POST'])
@login_required
def add_card():
    """
    Allows user to add a new card to the current deck
    """
    form = AddCardForm()
    deck_id = request.args.get('id')
    deck = Deck.query.filter_by(id=deck_id).first()
    if form.validate_on_submit():
        # create card
        card = Card(front=form.front.data,
                    back=form.back.data,
                    deck=deck,
                    owner=current_user)
        # add card to the database
        db.session.add(card)
        db.session.commit()
        flash('Card successfully created')

        return redirect('/deck?id={}'.format(deck_id))

    return render_template('add-card.html', form=form)


@app.route('/create-class', methods=['GET', 'POST'])
@login_required
def create_class():
    """
    Allows user to create a class
    """
    form = CreateClassForm()
    if form.validate_on_submit():
        # create class
        cohort = Class(name=form.name.data,
                       password_hash=form.password.data,
                       owner=current_user)
        # add class to the database
        db.session.add(cohort)
        db.session.commit()
        flash('Class successfully created')

        return redirect(url_for('dashboard'))

    return render_template('create-class.html', form=form)
