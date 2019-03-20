"""
Contains all views, including:
/register, /login, /logout, /dashboard, /create-deck, /deck, /add-card
"""

# Third party imports
from flask import Flask, redirect, render_template, session, flash, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
# Local application imports
from . import app, db
from .forms import LoginForm, RegistrationForm, CreateDeckForm, AddCardForm, CreateCohortForm, JoinCohortForm, JoinCohortPWForm
from .models import User, Deck, InsCard, StuCard, Cohort, load_user


# Authentication route controllers


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
        flash('Welcome to teach_SR! You may now login.')

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

    return redirect(url_for('login'))


# Dashboard route controller


@app.route('/dashboard')
@login_required
def dashboard():
    """
    Displays the dashboard view
    From the dashboard, user can access:
    Review Flashcards, Cohorts, Decks, and Monitoring
    """
    user = current_user
    decks = Deck.query.filter_by(owner_id=current_user.id).all()
    cohorts = user.cohorts

    return render_template('dashboard.html', decks=decks, user=user,
                           cohorts=cohorts)


# Deck route controllers


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

        return redirect('/deck/{}'.format(deck.id))

    return render_template('create-deck.html', form=form, title='create deck')


@app.route('/deck/<int:deck_id>', methods=['GET', 'POST'])
@login_required
def deck_view(deck_id):
    """
    Displays view of deck
    From here, users can:
    Add, edit, assign, and delete cards from decks and access settings
    """

    # Get currently selected deck
    deck = Deck.query.get_or_404(deck_id)
    # Display list of InsCards in deck using model's backref attribute
    cards = deck.ins_cards
    # Get list of the user's owned cohorts for dropdown menu
    cohorts = current_user.cohorts

    # Route to assign cards to cohort
    if request.method == 'POST' and request.form['submit'] == 'Add to cohort':
        # Get checkbox'd cards
        sel_card_ids = request.form.getlist('sel_cards')
        # Create list of card objects
        sel_cards = []
        for card_id in sel_card_ids:
            sel_cards.append(InsCard.query.get(card_id))
        # Get selected cohort
        sel_cohort_id = request.form.get('sel_cohort_id')
        sel_cohort = Cohort.query.get(sel_cohort_id)
        # Add cards to selected cohort
        for card in sel_cards:
            card.cohorts.append(sel_cohort)
        db.session.commit()
        flash('Card(s) successfully added')

        return redirect('/deck/{}'.format(deck_id))

    # TODO: give error if no card is checked
    # Route to delete cards
    if request.method == 'POST' and request.form['submit'] == 'Delete cards':
        # Get checkbox'd cards
        sel_card_ids = request.form.getlist('sel_cards')
        # Create list of card objects
        sel_cards = []
        for card_id in sel_card_ids:
            sel_cards.append(InsCard.query.get(card_id))
        # Delete cards from deck
        for card in sel_cards:
            deck.cards.remove(card)
        db.session.commit()
        flash('Card(s) successfully deleted')

        return redirect('/deck/{}'.format(deck_id))

    return render_template('deck.html', deck=deck, cards=cards,
                           cohorts=cohorts)


@app.route('/deck/add-card/<int:deck_id>', methods=['GET', 'POST'])
@login_required
def add_card(deck_id):
    """
    Allows user to add a new card to the current deck
    """
    form = AddCardForm()
    deck = Deck.query.filter_by(id=deck_id).first()
    if form.validate_on_submit():
        # create card
        card = InsCard(front=form.front.data,
                       back=form.back.data,
                       deck=deck,
                       owner=current_user)
        # add card to the database
        db.session.add(card)
        db.session.commit()
        flash('Card successfully created')

        return redirect('/deck/{}'.format(deck_id))

    return render_template('add-card.html', form=form)


# Cohort route controllers


@app.route('/cohort/<int:cohort_id>', methods=['GET', 'POST'])
@login_required
def cohort_view(cohort_id):
    """
    Displays view of cohort
    """

    sel_cohort = Cohort.query.get_or_404(cohort_id)
    cards = sel_cohort.ins_cards
    students = sel_cohort.students

    # TODO: allow these only for cohort owner
    if request.method == 'POST':

        # Route to remove students from cohort
        if request.form['submit'] == 'Remove student(s) from cohort':
            # Get checkbox'd students
            sel_stu_ids = request.form.getlist('sel_students')
            # Create list of user objects
            sel_students = []
            for stu_id in sel_stu_ids:
                sel_students.append(User.query.get(stu_id))
            # Remove students from cohort
            for student in sel_students:
                student.joined_cohorts.remove(sel_cohort)
            db.session.commit()
            flash('Student(s) successfully removed')

            return redirect('/cohort/{}'.format(cohort_id))

        # TODO: Add functionality to remove StuCards from students
        # TODO: give error if no card is checked
        # Route to remove cards from cohort
        if request.form['submit'] == 'Remove card(s) from cohort':
            # Get checkbox'd cards
            sel_card_ids = request.form.getlist('sel_cards')
            # Create list of card objects
            sel_cards = []
            for card_id in sel_card_ids:
                sel_cards.append(InsCard.query.get(card_id))
            # Remove cards contained in list
            for card in sel_cards:
                card.cohorts.remove(sel_cohort)
            db.session.commit()
            flash('Card(s) successfully removed.')

            return redirect('/cohort/{}'.format(cohort_id))

    return render_template('cohort.html', sel_cohort=sel_cohort,
                           students=students, cards=cards)


@app.route('/create-cohort', methods=['GET', 'POST'])
@login_required
def create_cohort():
    """
    Allows user to create a cohort
    """
    form = CreateCohortForm()
    if form.validate_on_submit():
        # create cohort
        cohort = Cohort(name=form.name.data,
                        password_hash=form.password.data,
                        owner=current_user)
        # add cohort to the database
        db.session.add(cohort)
        db.session.commit()
        flash('Cohort successfully created')

        return redirect(url_for('dashboard'))

    return render_template('create-cohort.html', form=form)


@app.route('/join-cohort', methods=['GET', 'POST'])
@login_required
def join_cohort():
    """
    Allows user to join a cohort, including their own
    """
    form = JoinCohortForm()
    if form.validate_on_submit():
        # Get instructor based on submitted email
        instructor = User.query.filter_by(email=form.email.data).first()

        return redirect('join-cohort/{}'.format(instructor.id))

    return render_template('join-cohort.html', form=form)


@app.route('/join-cohort/<int:instructor_id>')
@login_required
def join_cohort_inst(instructor_id):
    """
    Shows user a list of cohorts owned by instructor
    """
    instructor = User.query.filter_by(id=instructor_id).first()
    cohorts = instructor.cohorts

    return render_template('instructor-cohorts.html',
                           cohorts=cohorts, instructor=instructor)


@app.route('/join-cohort-pw/<int:cohort_id>', methods=['GET', 'POST'])
@login_required
def join_cohort_pw(cohort_id):
    """
    Prompts user to enter password before joining the cohort
    """
    form = JoinCohortPWForm()
    if form.validate_on_submit():
        # Get selected cohort based on id from URL
        sel_cohort = Cohort.query.filter_by(id=cohort_id).first()
        if sel_cohort.password_hash == form.password.data:
            # Add user to the cohort through the backref "students"
            sel_cohort.students.append(current_user)
            db.session.commit()
            flash('You have joined the cohort!')

            return redirect('/dashboard')
        else:
            flash('Invalid password')

            return render_template('join-cohort-pw.html', form=form)

    return render_template('join-cohort-pw.html', form=form)


@app.route('/review/<int:cohort_id>/<int:user_id>', methods=['GET', 'POST'])
@login_required
def review(cohort_id, user_id):
    """
    Allows user to see a certain cohort's cards
    From here the user can review due cards or free review
    """

    return render_template('cohort-stu-view.html', cohort_id=cohort_id,
                           user_id=user_id)


@app.route('/free-review/<int:cohort_id>/<int:user_id>', methods=['GET', 'POST'])
@login_required
def free_review(cohort_id, user_id):
    """
    Allows user to review all cards in cohort outside of the SR schedule
    """
    cohort = Cohort.query.get(cohort_id)
    total_cards = total_cards(cohort)

    return render_template('free-review-landing.html', cohort_id=cohort_id,
                           user_id=user_id)


# Redirects


@app.route('/deck/dashboard')
@login_required
def deck_dashboard():

    return redirect('/dashboard')


@app.route('/cohort/dashboard')
@login_required
def cohort_dashboard():

    return redirect('/dashboard')


@app.route('/join-cohort/dashboard')
@login_required
def join_cohort_dashboard():

    return redirect('/dashboard')


@app.route('/deck/add-card/dashboard')
@login_required
def add_card_dashboard():

    return redirect('/dashboard')
