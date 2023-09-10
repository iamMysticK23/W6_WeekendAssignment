

# External imports
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user


# internal imports
from theblog_content.forms import PostForm, SearchForm, LoginForm, RegisterForm, UpdateForm
from theblog_content.models import Users, Posts, db

# Blueprint object
site = Blueprint('site', __name__, template_folder='site_templates')



# testing the initial setup

@site.route('/')
def index():
    return render_template('index.html')




@site.route('/user')
def user():
    return render_template('user.html')




# create post page
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
            



# pass info to navbar
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







