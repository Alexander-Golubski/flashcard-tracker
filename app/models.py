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
    password_hash = db.Column(db.String(120))
    #cards = db.relationship("Card", backref="owner") 
    
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
        return '<ID: {} {} {}>'.format(self.id, self.first_name, self.last_name)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
