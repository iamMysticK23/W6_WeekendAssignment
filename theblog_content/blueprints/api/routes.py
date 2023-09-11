# external imports

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity 

# internal imports
from theblog_content.models import Posts,PostSchema, db, post_schema, posts_schema

# instantiate blueprint

api = Blueprint('api', __name__, url_prefix ='/api') 

@api.route('/token', methods = ['GET', 'POST'])
def token():

    data = request.json

    if data:
        client_id = data['client_id'] # looking for the key of client_id on the dictionary passed 
        access_token = create_access_token(identity=client_id)
        return {
            'status' : 200,
            'access_token': access_token

        }
    
    else:
        return {
            'status': 400,
            'message': 'Missing Client ID. Try again.'

        }



# API endpoint to get all blog posts
# this is the only one I find to be useful for the API since people are more than likely only interested in the content of a post
@api.route('/posts', methods=['GET'])
@jwt_required()
def get_posts():
    posts = Posts.query.order_by(Posts.date_posted).all()
    post_schema = PostSchema(many=True)
    result = post_schema.dump(posts)
    return jsonify({'posts': result})



# API endpoint to create a new blog post
# this doesn't really work and I wouldn't want the functionality of someone being able to create a post without being on the site
@api.route('posts/create/<int:postid>', methods=['POST'])
@jwt_required()
def create_post():

    data = request.json
    post_schema = PostSchema()
    new_post = post_schema.load(data)
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Blog post created successfully'})

# API endpoint to update a blog post
# this doesn't really work and I wouldn't want the functionality of someone being able to edit a post without being on the site
@api.route('/posts/update/<int:postid>', methods=['PUT'])
@jwt_required()
def update_post(postid):
    data = request.json
    post_schema = PostSchema()
    post = Posts.query.get_or_404(postid)

    try:
        post = post_schema.load(data, instance=post)
        db.session.commit()
        return jsonify({'message': 'Blog post updated successfully'})
    except Exception as e:
        # Log the error for debugging
        print(e)
        db.session.rollback()  # Rollback changes in case of error
        return jsonify({'error': 'Failed to update the blog post'}), 500  # Return an error response


# API endpoint to delete a blog post
# This did work when I tested it. 
@api.route('posts/delete/<int:postid>', methods=['DELETE'])
@jwt_required()
def delete_post(postid):
    post = Posts.query.get_or_404(postid)


    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Blog post deleted successfully'})


