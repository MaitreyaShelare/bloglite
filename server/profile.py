#IMPORTS
from flask import Blueprint,request,jsonify
from models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, create_access_token,create_refresh_token,get_jwt_identity
import base64
import os
from __init__ import db
profile = Blueprint('profile', __name__)

# For Profile Component
@profile.route('/api/profile/<int:user_id>', methods=['GET'])
def getUserProfile(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        user_schema = UserSchema()
        result = user_schema.dump(user)
        return jsonify(result)
    else:
        return jsonify(error="User not found"), 404
    
# For Change Profile Picture
@profile.route('/api/profile/dp/<int:user_id>', methods=['POST'])
def getUserDp(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        photo = request.files["image"].read()
        photo_b64 = base64.b64encode(photo).decode('utf-8')
        photo_mimetype = request.files["image"].mimetype

        user.dp = photo_b64
        user.dp_mimetype = photo_mimetype
        db.session.commit()
    
        return jsonify(message="Profile Picture Updated",dp=photo_b64,dp_mimetype=photo_mimetype), 201
    # return jsonify(message="Profile Picture Updated"), 201
    else:
        return jsonify(error="Error in Updating Profile Picture"), 404    
    
# To change Name
@profile.route('/api/profile/name/<int:user_id>', methods=['POST'])
@jwt_required()
def changeName(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        # name = request.json["name"]
        name = request.form["name"]
        user.name = name
        db.session.commit()
        return jsonify(message="Name Updated"), 201
    else:
        return jsonify(error="Error in Updating Name"), 404    

# For Profile View, returns only a user's blog IDs
@profile.route('api/profile/blogs/<int:user_id>', methods=['GET'])
@jwt_required()

def get_user_blogs(user_id):
    blogs = Blog.query.filter_by(user_id=user_id).order_by(Blog.timestamp.desc()).all()
    blog_ids = [blog.id for blog in blogs]
    return jsonify(blog_ids) 

# For Search View, returns only a user IDs
@profile.route('api/profile/search', methods=['POST'])
@jwt_required()

def get_user_ids():
    name = request.json["name"]
    print(name)
    users = User.query.filter(User.name.ilike('%'+name+'%')).all()
    user_ids = [user.id for user in users]
    return jsonify(user_ids), 201
    # return jsonify(message="serched"), 201

# Follow a user
@profile.route('api/profile/follow/<int:current_user_id>/<int:user_id>', methods=['POST'])
@jwt_required()

def follow_user(current_user_id,user_id):
    current_user = User.query.filter_by(id=current_user_id).first()
    user = User.query.filter_by(id=user_id).first()
    # print(user.id)
    if user is not None:
        current_user.follow(user)
        return jsonify({'message': 'You are now following {}.'.format(user.name)}), 201
    else:
        return jsonify(error="User not found"), 404
    
# Unfollow a user
@profile.route('api/profile/unfollow/<int:current_user_id>/<int:user_id>', methods=['POST'])
@jwt_required()

def unfollow_user(current_user_id,user_id):
    current_user = User.query.filter_by(id=current_user_id).first()
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        current_user.unfollow(user)
        return jsonify({'message': 'You are no longer following {}.'.format(user.name)}), 201
    else:
        return jsonify(error="User not found"), 404
    
# Get a user's followers
@profile.route('api/profile/followers/<int:user_id>', methods=['GET'])
@jwt_required()

def get_followers(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        followers_ids = [follower.id for follower in user.followers_users.all()]
        return jsonify(followers_ids), 201
    
    else:
        return jsonify(error="Invalid User"), 404
    
# Get a user's following
@profile.route('api/profile/following/<int:user_id>', methods=['GET'])
@jwt_required()

def get_following(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        following_ids = [user.id for user in user.followed_users.all()]
        return jsonify(following_ids), 201
    else:
        return jsonify(error="User not found"), 404
    
# Get a user's followers count
@profile.route('api/profile/followers/count/<int:user_id>', methods=['GET'])
@jwt_required()

def get_followers_count(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        followers = user.followers
        return jsonify(count=len(followers))
    else:
        return jsonify(error="User not found"), 404
    
# Get a user's following count
@profile.route('api/profile/following/count/<int:user_id>', methods=['GET'])
@jwt_required()

def get_following_count(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        following = user.following
        return jsonify(count=len(following))
    else:
        return jsonify(error="User not found"), 404
    
# Get a user's blogs count
@profile.route('api/profile/blogs/count/<int:user_id>', methods=['GET'])
@jwt_required()

def get_blogs_count(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        blogs = user.blogs
        return jsonify(count=len(blogs))
    else:
        return jsonify(error="User not found"), 404
    
# Get a user's likes count
@profile.route('api/profile/likes/count/<int:user_id>', methods=['GET'])
@jwt_required()

def get_likes_count(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        likes = user.likes
        return jsonify(count=len(likes))
    else:
        return jsonify(error="User not found"), 404
    
# Get a user's comments count
@profile.route('api/profile/comments/count/<int:user_id>', methods=['GET'])
@jwt_required()

def get_comments_count(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        comments = user.comments
        return jsonify(count=len(comments))
    else:
        return jsonify(error="User not found"), 404
    

#######################################################################################################
# @auth.route('api/signup', methods=['POST'])
# def signup():
#     name = request.json["name"]
#     email = request.json["email"]
#     password = request.json["password"]
#     dp = open('bloglite/src/assets/user.png', 'rb').read()
#     ext = os.path.splitext('bloglite/src/assets/user.png')[1][1:]
#     dp_b64 = base64.b64encode(dp).decode('utf-8')
#     dp_mimetype = f'image/{ext}'
    
#     user = User.query.filter_by(email=email).first()
#     if user:
#         return jsonify(message="User Already Exists"), 409
#     else:
#             new_user = User(email=email, name=name, dp=dp_b64, dp_mimetype=dp_mimetype, password=generate_password_hash(password, method='sha256'))
#             access_token = create_access_token(identity=email)
#             refresh_token = create_refresh_token(identity=email)
#             db.session.add(new_user)
#             db.session.commit()
#             return jsonify(access_token=access_token, refresh_token=refresh_token), 201


# @auth.route('api/login', methods=['POST'])
# def login():
#     email = request.json["email"]
#     password = request.json["password"]
    
#     user = User.query.filter_by(email=email).first()
#     if user:
#         if check_password_hash(user.password, password): 
#             access_token = create_access_token(identity=email)
#             refresh_token = create_refresh_token(identity=email)
#             return jsonify(access_token=access_token, refresh_token=refresh_token), 201
#     return jsonify(message="Invalid Email or Password"), 403

# @auth.route("api/refresh", methods=["POST"])
# @jwt_required(refresh=True)
# def refresh():
#     identity = get_jwt_identity()
#     access_token = create_access_token(identity=identity)
#     return jsonify(access_token=access_token),201    
