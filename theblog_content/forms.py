# Form creation

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, validators
from wtforms.validators import DataRequired, EqualTo, Email
from wtforms.widgets import TextArea

# create login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators= [DataRequired() ])
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

# create update form


class UpdateForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    image = StringField("Image URL")
    about_you = TextAreaField("Short bio about you", validators=[validators.Length(max=500)],
        render_kw={"rows": 4, "cols": 50})
    submit = SubmitField('Submit Changes')

# post form
class PostForm(FlaskForm):
    title = StringField("Title",validators=[DataRequired()] )
    content =StringField("Content",validators=[DataRequired()], widget=TextArea())
    author =StringField("Author",validators=[DataRequired()])
    slug =StringField("Slug",validators=[DataRequired()])
    submit = SubmitField("Submit")

