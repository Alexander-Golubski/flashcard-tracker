"""
Contains all database models.

One to many relationships:
Deck to InsCard (one deck can have many cards)
User(owner) to InsCard (each card, cohort, and deck has one user who owns it)
User(owner) to StuCard
User(owner) to Cohort
User(owner) to Deck

Many to many relationships:
User to Cohort (one user can join many cohorts, one cohort can have many users)
Cohort to InsCard
"""

# Third party imports
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# Local application imports
from . import db, login_manager


# flask_login


@login_manager.user_loader
def load_user(user_id):
    """
    This callback is used to reload the user object from the user ID stored
    in the session. It is required by flask_login.
    """
    return User.query.get(int(user_id))

# Association tables


UserCohorts = db.Table('UserCohorts',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('cohort_id', db.Integer, db.ForeignKey('cohort.id'))
)

CardCohorts = db.Table('CardCohorts',
    db.Column('ins_card_id', db.Integer, db.ForeignKey('ins_card.id')),
    db.Column('cohort_id', db.Integer, db.ForeignKey('cohort.id'))
)

# Class models


class User(UserMixin, db.Model):
    """ Creates User table """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(40), unique=True)
    password_hash = db.Column(db.String(128))
    # A user can own multiple decks, cards, and cohorts (one to many)
    decks = db.relationship('Deck', backref='owner')
    ins_cards = db.relationship('InsCard', backref='owner')
    stu_cards = db.relationship('StuCard', backref='owner')
    cohorts = db.relationship('Cohort', backref='owner')
    # Many to many: users to cohorts
    user_cohorts = db.relationship('Cohort',
                                   secondary=UserCohorts,
                                   backref=db.backref('students'))

    def __init__(self, first_name, last_name, email, password_hash):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password_hash

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<ID: {}, {}, {}>'.format(self.id,
                                         self.last_name,
                                         self.first_name)


class Deck(db.Model):
    """ Creates Deck table """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    # Every deck is owned by one user
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # A deck can have multiple InsCards (one to many)
    ins_cards = db.relationship('InsCard', backref='deck')

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner

    def list_cards(self, an_owner_id):
        cards = InsCard.query.filter_by(owner_id=an_owner_id).all()
        return cards

    def __repr__(self):
        owner_name = self.owner.first_name + " " + self.owner.last_name
        return '<ID: {}, Name: {}, Owner: {}>'.format(self.id,
                                                      self.name,
                                                      owner_name)


class InsCard(db.Model):
    """
    Stands for "Instructor Card." Creates InsCard table.

    Instructors create these cards, then assign them to a cohort. When an
    InsCard is assigned to a cohort, a StuCard object is created for each
    student in the cohort.
    """
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(1200))
    back = db.Column(db.String(1200))
    # Every InsCard is owned by one user
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Every InsCard belongs to one deck
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'))
    # Many to many: InsCards to Cohorts
    card_cohorts = db.relationship('Cohort',
                                   secondary=CardCohorts,
                                   backref=db.backref('ins_cards'))

    def __init__(self, front, back, deck, owner):
        self.front = front
        self.back = back
        self.deck = deck
        self.owner = owner

    def create_stu_card(self, cohort_id, owner_id):
        stu_card = StuCard(self.front, self.back, cohort_id, owner_id)
        return stu_card

    def __repr__(self):
        owner_name = self.owner.first_name + " " + self.owner.last_name
        return '<ID: {}, Front: {}, Back: {}, Deck: {}>'.format(self.id,
                                                                self.front,
                                                                self.back,
                                                                self.deck,
                                                                owner_name)


class StuCard(db.Model):
    """
    Stands for "Student Card." Creates StuCard table.

    Extends the Card class. Is basically a copy of the InsCard it is based on.
    The difference is that it will have review data (e.g. date of last review)
    tied to a specific user.
    """
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(1200))
    back = db.Column(db.String(1200))
    # Every StuCard is owned by one user
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 0=new, 1=learning, 2=reviewed, 3=due
    review = db.Column(db.Integer)
    # When this card is due
    due = db.Column(db.Integer)
    # One to many: every StuCard belongs to one Cohort
    cohort_id = db.Column(db.Integer, db.ForeignKey('cohort.id'))

    def __init__(self, front, back, cohort_id, owner_id):
        self.front = front
        self.back = back
        self.cohort_id = cohort_id
        self.owner_id = owner_id

    def __repr__(self):
        owner_name = self.owner.first_name + " " + self.owner.last_name
        return '<ID: {}, F: {}, B: {}, C: {}, Due: {}>'.format(self.id,
                                                               self.front,
                                                               self.back,
                                                               self.cohort,
                                                               self.due,
                                                               owner_name)


class Cohort(db.Model):
    """ Creates Cohort table """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    password_hash = db.Column(db.String(128))
    # Every Cohort is owned by one user
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # A Cohort can have multiple StuCards (one to many)
    cards = db.relationship('StuCard', backref='cohort')
    # Many to many: Cohorts to InsCards
    card_cohorts = db.relationship('InsCard',
                                   secondary=CardCohorts,
                                   backref=db.backref('cohorts'))
    # Many to many: Cohorts to Users
    user_cohorts = db.relationship('User',
                                   secondary=UserCohorts,
                                   backref=db.backref('joined_cohorts'))

    def __init__(self, name, password_hash, owner):
        self.name = name
        self.password_hash = password_hash
        self.owner = owner

    def total_cards(self, student_id):
        """
        return number (int) of total cards in a cohort for a specific
        student
        """
        qo_card_list = StuCard.query.filter_by(cohort_id=self.id).filter_by(owner_id=student_id).all()
        return len(qo_card_list)

    def list_cards(self, student_id):
        """
        Returns a list of StuCard objects in a cohort for a specific student
        """
        qo_card_list = StuCard.query.filter_by(cohort_id=self.id).filter_by(owner_id=student_id).all()
        card_list = []
        for card in qo_card_list:
            card_list.append(StuCard.query.get(card.id))
        return card_list

    def __repr__(self):
        owner_name = self.owner.first_name + " " + self.owner.last_name
        return '<ID: {}, Name: {}, Owner: {}>'.format(self.id,
                                                      self.name,
                                                      owner_name)
