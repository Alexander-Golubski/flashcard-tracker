"""Contains all flask forms"""

# Third party imports
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
# Local application imports
from .models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
                                             Email(),
                                             Length(max=35)])
    first_name = StringField('First Name', validators=[DataRequired(),
                                                       Length(max=45)])
    last_name = StringField('Last Name', validators=[DataRequired(),
                                                     Length(max=45)])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=8, max=45),
                                                     EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8, max=45)])
    submit = SubmitField('Log in')


class CreateDeckForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=5, max=45)])
    submit = SubmitField('Create')


class AddCardForm(FlaskForm):
    front = TextAreaField('Front',
                          validators=[DataRequired(), Length(max=1200)])
    back = TextAreaField('Back', validators=[DataRequired(), Length(max=1200)])
    submit = SubmitField('Add card')


class CreateCohortForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=35)])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=5, max=45),
                                         EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Create')


class JoinCohortForm(FlaskForm):
    email = StringField('Instructor email', validators=[DataRequired(),
                                                        Email(),
                                                        Length(max=35)])
    submit = SubmitField('Submit')


class JoinCohortPWForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=5, max=45)])
    submit = SubmitField('Submit')
