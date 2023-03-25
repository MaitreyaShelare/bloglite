#IMPORTS
from flask import Blueprint,request,jsonify,json
from models import *
from flask_jwt_extended import jwt_required, current_user
import base64
from __init__ import db
blog = Blueprint('blog', __name__)

from datetime import datetime
# from pytz import timezone

# def get_server_time(self, obj):
#     # Calculate the server time using datetime and pytz
#     tz = pytz.timezone('Asia/Kolkata')  # Indian Standard Time
#     server_time = datetime.datetime.now(tz)
#     return server_time
# # get the current datetime in UTC
# utc_now = datetime.utcnow()
# print(utc_now)

# # convert UTC datetime to IST timezone
# ist_now = utc_now.astimezone(timezone('Asia/Kolkata'))
# ist_now_str = ist_now.strftime('%Y-%m-%d %H:%M:%S %Z%z')
# print(ist_now)

# @list.route('api/lists', methods=['GET'])
# @jwt_required()
# def getAllLists():
#     list_all = List.query.filter_by(user_id=current_user.id).all()
#     list_schema = ListSchema(many=True)
#     output = list_schema.dump(list_all)
#     # print(output)
#     return jsonify(output), 201

# @blog.route('api/blog/<int:id>', methods=['GET'])
# @jwt_required()
# def getBlog(id):
#     blog = Blog.query.get(id)
#     blog_schema = BlogSchema(many=True)
#     output = blog_schema.dump(blog)
#     # print(output)
#     return jsonify(output), 201

# For Each Blog Component
@blog.route('/api/blog/<int:blog_id>', methods=['GET'])
@jwt_required()
def getBlog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    if blog is not None:
        blog_schema = BlogSchema()
        result = blog_schema.dump(blog)
        return jsonify(result)
    else:
        return jsonify(error="Blog not found"), 404

# For Explore, returns only blog IDs
@blog.route('api/blogs', methods=['GET'])
@jwt_required()
# def getAllBlogs():
#     blog_all = Blog.query.all()
#     blog_schema = BlogSchema(many=True)
#     output = blog_schema.dump(blog_all)
#     return jsonify(output), 201
def get_blogs():
    blogs = Blog.query.order_by(Blog.timestamp.desc()).all()
    blog_ids = [blog.id for blog in blogs]
    return jsonify(blog_ids), 201    
# @blog.route('api/blog/<int:blog_id>', methods=['GET'])
# @jwt_required()
# def getBlog(blog_id):
#     blog = Blog.query.get(blog_id)
#     if not blog:
#         return jsonify(message="Blog not found"), 404
#     blog_data = {
#         "text": blog.text,
#         "image": blog.photo.decode('utf-8') # decode the binary image data
#     }
#     return jsonify(blog_data), 201

# def getBlog(blog_id):
#     blog = Blog.query.filter_by(id=blog_id).first()
#     if blog is not None:
#         blog_schema = BlogSchema()
#         result = blog_schema.dump(blog)
#         return jsonify(result)
#     else:
#         return jsonify(error="Blog not found"), 404

# For Home View Feed, returns only blog IDs
@blog.route('api/feed/<int:user_id>', methods=['GET'])
@jwt_required()

def get_feed(user_id):
    current_user = User.query.filter_by(id=user_id).first()
    if current_user is not None:
        followed_user_ids = [user.id for user in current_user.followed_users]
        followed_user_blogs = Blog.query.filter(Blog.user_id.in_(followed_user_ids)).order_by(Blog.timestamp.desc()).all()
        blog_ids = [blog.id for blog in followed_user_blogs]
        return jsonify(blog_ids), 201 
    else:
        return jsonify(error="Invalid User"), 404   


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

# @list.route('api/list/<int:id>', methods=['DELETE'])
# @jwt_required()
# def deleteList(id):
#     list = List.query.filter_by(id=id).first() 
#     if list: 
#         if list.user_id == current_user.id:
#             db.session.delete(list)
#             db.session.commit()
#     return jsonify(message="List deleted sucessfully"), 201