# Third party imports
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# Local application imports
from . import db, login_manager


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(40), unique=True)
    password_hash = db.Column(db.String(128))
    decks = db.relationship('Deck', backref='owner') 
    
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
        return '<ID: {}, {}, {}>'.format(self.id, self.last_name, self.first_name)

@login_manager.user_loader
def load_user(user_id):
    """
    This callback is used to reload the user object from the user ID stored
    in the session.
    """
    return User.query.get(int(user_id))

class Deck(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cards = db.relationship('Card', backref='deck')

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
    
    def __repr__(self):
        return '<ID: {}, Name: {}, Owner: {}>'.format(self.id, self.name, self.owner)

class Card(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(1200))
    back = db.Column(db.String(1200))
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'))

    def __init__(self, front, back, deck):
        self.front = front
        self.back = back
        self.deck = deck
    
    def __repr__(self):
        return '<ID: {}, Front: {}, Back: {}, Deck: {}>'.format(self.id, 
                                         self.front, self.back, self.deck)
