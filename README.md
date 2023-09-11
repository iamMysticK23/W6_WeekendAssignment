:Week 6 Weekend Project
:Create full featured CRUD RESTful API

------:Creator: Kenai Epps

I came up with a blog style site for this. Here is more information about it:

The blog is called The Blog Spot.
CRUD Requirements were met as follows:

C- Users can be created by a person registering
    - Users are initally set up under the role of "blogger". There is another role called "admin" that simulates what an administrator would see running a blog.
        I wanted to do more with this, but I was able to set it up to where you can see all the users in individual cards and a running count of current people registered
    - I made a testing account for the instructor grading: 
    
    - username- codingtemple | password- test4

R - Users can log into the site, create/update/delete blog posts, update/delete their own user profile
    -Users can only delete their own blog posts. I wanted to set it up to where admins could delete everybody's post but it is something I can probably revisit in the future

U - Users can update their posts and profiles. I wanted to have a feature that people could use to pull in pictures from the google image API but spent too much time trying to figure 
    out how to have a user upload their own profile picture
    from their computer instead. That was a fail so I omitted it from the final site. I ended up just using placeholder images from Lorem Picsum so most of the pics on the
    site will change upon refresh.

D - Users can delete their profile/posts from the database.

:::Extra - The search bar/button actually work! It searches for words that are in a blog post (the actual content) and returns the results. If there's nothing found, the search
page will say that.

The database models i used were Users and Posts. The relationship is that one user can have many posts so I created an "author"
backref since that was the relationship between a user and post. a user is an author. 
I set the site up to where only a registered user can become an author, but anyone(registered or not) can read posts.

