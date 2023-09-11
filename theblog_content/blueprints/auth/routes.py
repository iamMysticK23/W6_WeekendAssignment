# external imports

from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user


# internal imports

from theblog_content.forms import SearchForm, LoginForm, RegisterForm, UpdateForm
from theblog_content.models import Users, db

# intiantate auth blueprint 
auth = Blueprint('auth', __name__, template_folder='auth_templates')


# New user sign up
@auth.route('/register',methods=['GET', 'POST'])
def register():
    

    # instantiate form
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

        # add the user object to database and commit the changes
        db.session.add(user)
        db.session.commit()

        flash (f" {username} has been registered", category='success')
        return redirect('/login') 

    return render_template('register.html', form=registerform)  



# User login
@auth.route('/login', methods = ['GET', 'POST'])
def login():

    loginform = LoginForm()

    if request.method == 'POST' and loginform.validate_on_submit():
        username = loginform.username.data
        password = loginform.password.data
        print(username, password)

        user = Users.query.filter(Users.username == username).first()
        print(user)

        if user and check_password_hash(user.password, password): 
            login_user(user) 

            # Check for admin in "role" column of database
            if user.role == 'admin':
                flash(f" Successfully logged in admin {username}", category='success')
                return redirect('/admin')
            
            else:
            
                flash(f" Successfully logged in user {username}", category='success')
                return redirect('/posts')
     
        else:
            flash(f" Invalid username and/or password. Please try again", category='warning')
            return redirect('/login')
        
    return render_template('login.html', form=loginform)



# Admin route

@auth.route('/admin')
@login_required
def admin():

    users = Users.query.all()

    user_stats = len(users)

    form = SearchForm()
    
    return render_template('admin.html', users=users, user_stats=user_stats, form=form)



# Delete user route

@auth.route('/user/delete')
@login_required
def delete():

    user = current_user
    print(user)

    db.session.delete(user)
    db.session.commit()


    flash (f" {user.first_name}'s profile has been deleted", category='success')

    return redirect('/')


# Logout route

@auth.route('/logout') 
def logout():
    logout_user() 
    return redirect('/')





