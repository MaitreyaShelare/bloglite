#IMPORTS
from flask import Blueprint,request,jsonify,json
from models import *
from flask_jwt_extended import jwt_required, current_user
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


@blog.route('api/blog', methods=['POST'])
@jwt_required()
def createBlog():
    if request.method == 'POST':
        # text = request.json["text"]
        # photo = request.json["photo"]
        text = request.form["text"]
        photo = request.files["image"].read()
        # photo_json = json.dumps(photo)
        print(photo,text)
        new_blog = Blog(text=text, photo=photo, user_id=current_user.id)
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