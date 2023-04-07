#IMPORTS
from flask import Blueprint,request,jsonify, make_response
import json
import redis
from models import *
from flask_jwt_extended import jwt_required, current_user
import base64
from __init__ import db
blog = Blueprint('blog', __name__)

from datetime import datetime

# Set up Redis connection
redis_conn = redis.Redis(host='localhost', port=6379, db=0)

# Set up cache expiration policy (e.g. expire cached data after 1 hour)
CACHE_EXPIRATION_TIME = 3600

# # For Each Blog Component
@blog.route('/api/blog/<int:blog_id>', methods=['GET'])
@jwt_required()
def getBlog(blog_id):
    # Generate a Redis key for the request
    redis_key = f"blog:{blog_id}".encode('utf-8')

    # Check if the request is already cached in Redis
    cached_data = redis_conn.get(redis_key)

    if cached_data:
        # If the request is cached, return the cached data as a response
        return jsonify(json.loads(cached_data))

    # If the request is not cached, retrieve the data from the database
    blog = Blog.query.filter_by(id=blog_id).first()

    if blog is not None:
        # Serialize the data using the schema
        blog_schema = BlogSchema()
        result = blog_schema.dump(blog)

        # Cache the serialized data in Redis
        redis_conn.setex(redis_key, CACHE_EXPIRATION_TIME, json.dumps(result))

        # Return the serialized data as a response
        return jsonify(result)
    else:
        # Return an error message as a response
        return jsonify(error="Blog not found"), 404
    
    
# For Each Comment Component
@blog.route('/api/blog/comment/<int:comment_id>', methods=['GET'])
@jwt_required()
def getComment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if comment is not None:
        comment_schema = CommentSchema()
        result = comment_schema.dump(comment)
        return jsonify(result)
    else:
        return jsonify(error="Comment not found"), 404

# For Home, returns only blog IDs
@blog.route('api/feed/<int:user_id>', methods=['GET'])
@jwt_required()

def get_feed(user_id):
    current_user = User.query.filter_by(id=user_id).first()
    if current_user is not None:
        followed_user_ids = [user.id for user in current_user.followed_users]
        followed_user_blogs = Blog.query.filter(Blog.user_id.in_(followed_user_ids)).filter_by(hidden=False).order_by(Blog.timestamp.desc()).all()
        blog_ids = [blog.id for blog in followed_user_blogs]
        return jsonify(blog_ids), 201 
    else:
        return jsonify(error="Invalid User"), 404   
    
# For Explore, returns only blog IDs
@blog.route('api/blogs', methods=['GET'])
@jwt_required()
def get_blogs():
    blogs = Blog.query.filter_by(hidden=False).order_by(Blog.timestamp.desc()).all()
    blog_ids = [blog.id for blog in blogs]
    return jsonify(blog_ids), 201    

# For Comments, returns only comment IDs
@blog.route('api/blog/comments/<int:blog_id>', methods=['GET'])
@jwt_required()
def get_comments(blog_id):
    comments = Comment.query.filter_by(blog_id=blog_id).order_by(Comment.timestamp.desc()).all()
    comment_ids = [comment.id for comment in comments]
    return jsonify(comment_ids), 201


# Create a Blog
@blog.route('api/blog', methods=['POST'])
@jwt_required()
def createBlog():
    if request.method == 'POST':
        text = request.form["text"]
        photo = request.files["image"].read()
        photo_b64 = base64.b64encode(photo).decode('utf-8')
        photo_mimetype = request.files["image"].mimetype
        new_blog = Blog(text=text, photo=photo_b64, photo_mimetype=photo_mimetype, user_id=current_user.id)
        db.session.add(new_blog)
        db.session.commit()
    return jsonify(message="Blog added sucessfully"), 201

# Update a Blog
@blog.route('api/blog/<int:blog_id>', methods=['PATCH'])
@jwt_required()
def updateBlog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    if blog is not None:
        if 'text' in request.form:
            blog.text = request.form['text']

        if 'image' in request.files:
            photo = request.files["image"].read()
            photo_b64 = base64.b64encode(photo).decode('utf-8')
            photo_mimetype = request.files["image"].mimetype
            blog.photo = photo_b64
            blog.photo_mimetype = photo_mimetype

        db.session.commit()

        # Delete cached data for this blog
        redis_key = f"blog:{blog_id}".encode('utf-8')
        redis_conn.delete(redis_key)

        return jsonify(message="Blog updated sucessfully"), 201
    else:
        return jsonify(error="Error in Blog Update"), 404
    
# Delete a Blog
@blog.route('api/blog/<int:blog_id>', methods=['DELETE'])
@jwt_required()
def deleteBlog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    if blog is not None:
        db.session.delete(blog)
        db.session.commit()

        # Delete cached data for this blog
        redis_key = f"blog:{blog_id}".encode('utf-8')
        redis_conn.delete(redis_key)
        
        return jsonify(message="Blog deleted sucessfully"), 201
    else:
        return jsonify(error="Error in Blog Delete"), 404
    
# Like a Blog
@blog.route('api/blog/like/<int:user_id>/<int:blog_id>', methods=['POST'])
@jwt_required()

def like_blog(user_id,blog_id):
    user = User.query.filter_by(id=user_id).first()
    blog = Blog.query.filter_by(id=blog_id).first()
    if user is not None:
        if blog is not None:
            user.like(blog)
        return jsonify(message="Blog Liked"), 201
    else:
        return jsonify(error="Error in Blog Like"), 404
    
# Unlike a Blog
@blog.route('api/blog/unlike/<int:user_id>/<int:blog_id>', methods=['POST'])
@jwt_required()

def unlike_blog(user_id,blog_id):
    user = User.query.filter_by(id=user_id).first()
    blog = Blog.query.filter_by(id=blog_id).first()
    if user is not None:
        if blog is not None:
            user.unlike(blog)
        return jsonify(message="Blog Unliked"), 201
    else:
        return jsonify(error="Error in Blog Unlike"), 404
    
# Toggle Blog Hide
@blog.route('api/blog/toggleHide/<int:blog_id>', methods=['PATCH'])
@jwt_required() 

def toggle_hide(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    if blog is not None:
        blog.hidden = not blog.hidden
        db.session.commit()
        return jsonify(message="Blog Hide Toggled", status=blog.hidden), 201
    else:
        return jsonify(error="Error in Blog Hide Toggle"), 404

# Add Comment
@blog.route('api/blog/comment/<int:user_id>/<int:blog_id>', methods=['POST']) 
@jwt_required()

def addComment(user_id,blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    if blog is not None:
        text = request.form["comment"]
        new_comment = Comment(text=text, blog_id=blog_id, user_id=user_id)
        db.session.add(new_comment)
        db.session.commit()
        return jsonify(message="Comment added sucessfully"), 201
    else:
        return jsonify(error="Error in Comment Add"), 404

    
# Delete Comment
@blog.route('api/blog/comment/<int:comment_id>', methods=['DELETE'])
@jwt_required()

def deleteComment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if comment is not None:
        db.session.delete(comment)
        db.session.commit()
        return jsonify(message="Comment deleted sucessfully"), 201
    else:
        return jsonify(error="Error in Comment Delete"), 404