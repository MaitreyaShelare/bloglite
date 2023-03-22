#IMPORTS
from flask import Blueprint,request,jsonify,json
from models import *
from flask_jwt_extended import jwt_required, current_user
import base64
from __init__ import db
blog = Blueprint('blog', __name__)


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

@blog.route('/api/blog/<int:blog_id>', methods=['GET'])
def getBlog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    if blog is not None:
        blog_schema = BlogSchema()
        result = blog_schema.dump(blog)
        return jsonify(result)
    else:
        return jsonify(error="Blog not found"), 404
    
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