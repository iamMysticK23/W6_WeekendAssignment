# Application configuration
import os
from dotenv import load_dotenv # loading environment variables



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
