#external imports

from flask import Flask, Blueprint, render_template
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_ckeditor import CKEditor
from flask_wtf.csrf import CSRFProtect

# internal imports

from config import Config
from .models import login_manager, db
from .blueprints.site.routes import site
from .blueprints.auth.routes import auth
from .blueprints.api.routes import api

# intantiate  Flask

app = Flask(__name__)

# CSRF protect
csrf = CSRFProtect(app)



# created a rich text editor
ckeditor = CKEditor(app)

app.config.from_object(Config)
jwt = JWTManager(app) 

# page protection
login_manager.init_app(app)
login_manager.login_view = 'auth.sign_in'
login_manager.login_message = "You must log in to continue."
login_manager.login_message_category = "warning"


# blueprints
app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)



# database init
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)


# page not found
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

