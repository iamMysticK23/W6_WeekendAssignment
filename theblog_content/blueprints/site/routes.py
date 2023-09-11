

# External imports
import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user


# internal imports
from theblog_content.forms import PostForm, SearchForm, UpdateForm
from theblog_content.models import Users, Posts, db



# Blueprint object
site = Blueprint('site', __name__, template_folder='site_templates')




# homepage route

@site.route('/')
def index():
    return render_template('index.html')




# individual user page

@site.route('/user', methods=['GET', 'POST'])
@login_required

def user():

    # Instantiate the form for updating a user profile

    user = Users.query.get(current_user.user_id)
    updateform = UpdateForm(first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        about_you=user.about_you)

    if request.method == 'POST' and updateform.validate_on_submit():
        try:
            # Update the user's information
            user.first_name = updateform.first_name.data
            user.last_name = updateform.last_name.data
            user.email = updateform.email.data
            user.about_you = updateform.about_you.data

            # Commit changes to the database
            db.session.commit()

            flash(f" {user.first_name}'s profile has been updated", category='success')
            return redirect(url_for('site.user'))  # Redirect back to the user page
        except Exception as e:
            flash("We were unable to process your request. Please try again", category='warning')
            print(e)  # Print the error for debugging
            return redirect(url_for('site.user'))

    return render_template('user.html', updateform=updateform)




# post route

@site.route('/add-post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Posts(title= form.title.data, content=form.content.data, author_id=current_user.user_id, slug = form.slug.data)

        # Clear the form
        form.title.data =''
        form.content.data =''
        form.slug.data = ''

        # Add post data to database
        db.session.add(post)
        db.session.commit()

        # Return the message
        flash (f" Blog post submitted successfully!", category='success')
        return redirect(url_for('site.post', postid=post.postid))

        # redirect to webpage
    return render_template("add_post.html", form=form)


# edit a blog post

@site.route('/posts/edit/<int:postid>', methods=['GET', 'POST'])
@login_required
def edit_post(postid):
    post = Posts.query.get_or_404(postid)
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.slug = form.slug.data
        post.content = form.content.data


        # update database
        db.session.add(post)
        db.session.commit()

        flash (f" Blog post updated successfully!", category='success')
        return redirect(url_for('site.post', postid=post.postid))
    
    # only allow correct user to go to the edit page
    if current_user.user_id == post.author_id:
    
        form.title.data = post.title
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template('edit_post.html', form=form)
    else:
        flash (f" Not authorized to edit this post.", category='warning')
        posts = Posts.query.order_by(Posts.date_posted)

        return render_template("posts.html", posts=posts)




# show only one blog post
@site.route('/posts/<int:postid>')
def post(postid):
    post = Posts.query.get_or_404(postid)
    return render_template('post.html', post=post)



# show blog posts
@site.route('/posts')
def posts():


    posts = Posts.query.order_by(Posts.date_posted)

    return render_template("posts.html", posts=posts)


# delete posts
@site.route('/posts/delete/<int:postid>')
@login_required
def delete_post(postid):
    post_to_delete = Posts.query.get_or_404(postid)
    id = current_user.user_id
    if id == post_to_delete.author_id:


        try:
            db.session.delete(post_to_delete)
            db.session.commit()

        # return success message
            flash (f" Blog post deleted.", category='success')
        
        # get all posts
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html", posts=posts)

        except:
            # return error message

            flash (f" Problem deleting post. Try again.", category='warning')
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html", posts=posts)
    else:
        flash (f" Not authorized to delete this post.", category='warning')
        
        # get all posts
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)
            


# pass info to navbar for search bar
@site.context_processor
def base():
    form = SearchForm()
    return dict(form=form)



# search bar feature

@site.route('/search', methods=["POST"])
def search():
    form = SearchForm()


    posts = Posts.query

    if form.validate_on_submit():

        # get data from submitted form
        post.searched = form.searched.data

        # query db
        posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
        posts = posts.order_by(Posts.title).all()

        return render_template("search.html", form=form, searched= post.searched, posts=posts)








