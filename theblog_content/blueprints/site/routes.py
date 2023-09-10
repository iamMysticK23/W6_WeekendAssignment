

# External imports
from flask import Blueprint, render_template, request, flash, redirect


# internal imports
from theblog_content.forms import NameForm

# Blueprint object
site = Blueprint('site', __name__, template_folder='site_templates')



# testing the initial setup
# will need to comment the code below out
@site.route('/')
def index():
    return render_template('index.html')
# end commented out code

# testing out returning a user
# may need to comment the code below out
@site.route('/user')
def user():
    return render_template('user.html')
# end commented out code








# Test for name.html via form
# This may be deleted
@site.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()

    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data =''
        flash(f" Form submitted successfully! Thank you {name}.")

    return render_template('name.html', name=name, form=form)