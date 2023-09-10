# external imports

from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

# internal imports
from theblog_content.forms import RegisterForm, LoginForm, UpdateForm
from theblog_content.models import Users,Posts, db

# intiantate our auth blueprint 
auth = Blueprint('auth', __name__, template_folder='auth_templates')


# New user sign up
@auth.route('/register',methods=['GET', 'POST'])
def register():
    

    # we need to instantiate our form
    registerform = RegisterForm()

    if request.method == 'POST' and registerform.validate_on_submit():
        # grab the input data from the form and save it to variables
        first_name = registerform.first_name.data
        last_name = registerform.last_name.data
        username = registerform.username.data
        email = registerform.email.data
        password = registerform.password.data
        print(email, password)
        
    # check the database for same username and/or email
    # Query the database

        if Users.query.filter(Users.username == username).first(): # if this comes back as something, the username already exists
            flash(' Username already exists. Please Try Again.', category='warning')
            return redirect('/register')
    
        if Users.query.filter(Users.email == email).first():
            flash(' Email already exists. Please Try Again.', category='warning')
            return redirect('/register')
    
        # instantiate a user object and commit to the db
        user = Users(username, email,password, first_name=first_name, last_name=last_name)

        # add the user object to our database and commit the changes
        db.session.add(user)
        db.session.commit()

        flash (f" {username} has been registered", category='success')
        return redirect('/login') #  add login here

    return render_template('register.html', form=registerform)  


# Log in
@auth.route('/login', methods = ['GET', 'POST'])
def login():

    loginform = LoginForm()

    if request.method == 'POST' and loginform.validate_on_submit():
        username = loginform.username.data
        password = loginform.password.data
        print(username, password)

        user = Users.query.filter(Users.username == username).first()
        print(user)

        if user and check_password_hash(user.password, password): # if there is a user that matches the email and the passwords match
            login_user(user) # this we have access to because of the UserMixin we inherited
            if user.role == 'admin':
                flash(f" Successfully logged in admin {username}", category='success')
                return redirect('/')
            else:
            # using the user_loader() function we made so now that will be the current_user of the site
                flash(f" Successfully logged in user {username}", category='success')
                return redirect('/')
     
        
        else:
            flash(f" Invalid username and/or password. Please try again", category='warning')
            return redirect('/login')
        
    return render_template('login.html', form=loginform)



@auth.route('/admin')
def admin():

    users = Users.query.all()

    user_stats = len(users)
    return render_template('admin.html', users=users, user_stats=user_stats)


@auth.route('/update', methods = ['GET', 'POST']) 
@login_required
def update():

    # instantiate our form
    updateform = UpdateForm()
    user = current_user
    print(user)

    if request.method == 'POST' and updateform.validate_on_submit():
        # grab the input data from the form and save it to variables

        try:
            user.first_name = updateform.first_name.data
            user.last_name = updateform.last_name.data
            user.email = updateform.email.data
            user.about_you = updateform.about_you.data


            # Commit changes to the database
            db.session.commit()

            flash (f" {user.first_name} 's profile has been updated", category='success')
        except:
            flash(" We were unable to process your request. Please try again", category='warning')
            return redirect('/update')


    return render_template('update.html', form=updateform, user=user)


@auth.route('/user/delete')
@login_required
def delete():

    user = current_user
    print(user)

    db.session.delete(user)
    db.session.commit()


    flash (f" {user.first_name}'s profile has been deleted", category='success')

    return redirect('/')


@auth.route('/logout') 
def logout():
    logout_user() # whatever user is the current_user will be logged out
    return redirect('/')





