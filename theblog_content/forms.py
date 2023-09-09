# Form creation

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email

# create login form
class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email() ])
    password = PasswordField('Password', validators = [DataRequired() ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# create register form
class RegisterForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    username = StringField('Username', validators= [DataRequired() ])
    email = StringField('Email', validators = [DataRequired(), Email() ])
    password = PasswordField('Password', validators = [DataRequired()])
    verify_password = PasswordField('Confirm Password', validators=[ DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# create name form
# this may be deleted
class NameForm(FlaskForm):
    name = StringField("What's Your Name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

