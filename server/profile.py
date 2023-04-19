#IMPORTS
from flask import Blueprint,request,jsonify, Response
from models import *
from flask_jwt_extended import jwt_required
import pandas as pd
import base64
from __init__ import db
from blog import redis_conn
profile = Blueprint('profile', __name__)

from tasks import exportBlogs
# from tasks import long_task
# if __name__ == '__main__':
#     celery_app.worker_main()

# @profile.route('api/profile/export/<int:user_id>', methods=['GET'])
# @jwt_required()
# def run_task(user_id):
#     # print(user_id)
#     # task = long_task.apply_async(args=[10])
#     task = long_task.delay(10)
#     return jsonify({'task_id': task.id})

# For Importing Blogs
@profile.route('api/profile/import/<int:user_id>', methods=['POST'])
@jwt_required()

def import_blogs(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        file = request.files["file"]
        df = pd.read_csv(file)                 
        for index, row in df.iterrows():
            blog = Blog(
                user_id=row['user_id'],
                text=row['text'],
                photo=row['photo'],
                photo_mimetype=row['mimetype'],
            )
            db.session.add(blog)
            db.session.commit()
        return jsonify(success="Blogs imported successfully"), 200
    else:
        return jsonify(error="User not found"), 404


# For Exporting Blogs
@profile.route('api/profile/export/<int:user_id>', methods=['GET'])
@jwt_required()

def export_blogs(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        task = exportBlogs.delay(user_id)
        return jsonify({'task_id': task.id})

@profile.route('api/tasks/<string:task_id>')
@jwt_required()
def task_status(task_id):
    task = exportBlogs.AsyncResult(task_id)
    if task.state == 'SUCCESS':
        result = task.get()
        df = pd.DataFrame.from_dict(result)

        csv = df.to_csv(index=False, header=True)
        return Response(
            csv,
            mimetype="text/csv",
            headers={"Content-disposition":
                     "attachment; filename=blogs.csv"})
    else:
        return jsonify({'status': task.state})
    
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
        redis_conn.flushdb()

        return jsonify(message="Profile Picture Updated",dp=photo_b64,dp_mimetype=photo_mimetype), 201
    else:
        return jsonify(error="Error in Updating Profile Picture"), 404    
    
# To get DP
@profile.route('/api/profile/dp/<int:user_id>', methods=['GET']) 
@jwt_required()

def getDp(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        dp = user.dp
        dp_mimetype = user.dp_mimetype
        return jsonify(dp=dp, dp_mimetype=dp_mimetype), 201
    else:
        return jsonify(error="Error"), 404   
    
        
# To change Name
@profile.route('/api/profile/name/<int:user_id>', methods=['POST'])
@jwt_required()
def changeName(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        name = request.form["name"]
        user.name = name
        db.session.commit()
        redis_conn.flushdb()

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


# Follow a user
@profile.route('api/profile/follow/<int:current_user_id>/<int:user_id>', methods=['POST'])
@jwt_required()

def follow_user(current_user_id,user_id):
    current_user = User.query.filter_by(id=current_user_id).first()
    user = User.query.filter_by(id=user_id).first()
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
    
