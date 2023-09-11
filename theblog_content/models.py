# external imports


from werkzeug.security import generate_password_hash 
from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin, LoginManager 
from datetime import datetime
import uuid 
from flask_marshmallow import Marshmallow
from sqlalchemy import ForeignKey
from flask_ckeditor import CKEditor





# instantiate DB
db = SQLAlchemy()

# instantiate login_manager
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


# Blog post model
class Posts(db.Model):
    postid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
    author_id = db.Column(db.String, db.ForeignKey('users.user_id'), nullable=False)

# Back ref relationship
    author = db.relationship('Users', backref='poster')

# Users of blog
class Users(db.Model, UserMixin):
    user_id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(10), default="blogger")
    about_you = db.Column(db.String(200))
  
   


    def __init__(self, username, email, password, first_name="", last_name=""):
        self.user_id = self.set_id() # creates a unique id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = self.set_password(password) # hash pw for security
    
   

    def set_id(self):
        return str(uuid.uuid4())
    
    def get_id(self):
        return str(self.user_id)

    def set_password(self, password):
        return generate_password_hash(password)
    


        return image

    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f" <USER: {self.username}"





    