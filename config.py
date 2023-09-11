# Application configuration
import os
from dotenv import load_dotenv # loading environment variables
from datetime import timedelta



basedir = os.path.abspath(os.path.dirname(__file__)) # base directory/root folder

load_dotenv(os.path.join(basedir, 'env')) # points to direction of environment variables in .env file


# many Config classes can be made with this
class Config():

    """
    Set Config variables for Flask app.
    Using Environment variables where available.
    Otherwise Config variables will be created.
    
    """

    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    FLASK_DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or "the blog weekend homework"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=365)        
