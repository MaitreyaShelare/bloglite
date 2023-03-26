#IMPORTS
from flask import Blueprint,request,jsonify
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, create_access_token,create_refresh_token,get_jwt_identity
import base64
import os
from __init__ import db
auth = Blueprint('auth', __name__)

@auth.route('api/signup', methods=['POST'])
def signup():
    name = request.json["name"]
    email = request.json["email"]
    password = request.json["password"]
    dp = open('bloglite/src/assets/user.png', 'rb').read()
    ext = os.path.splitext('bloglite/src/assets/user.png')[1][1:]
    dp_b64 = base64.b64encode(dp).decode('utf-8')
    dp_mimetype = f'image/{ext}'
    
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(message="User Already Exists"), 409
    else:
            new_user = User(email=email, name=name, dp=dp_b64, dp_mimetype=dp_mimetype, password=generate_password_hash(password, method='sha256'))
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)
            db.session.add(new_user)
            db.session.commit()
            return jsonify(access_token=access_token, refresh_token=refresh_token, id=new_user.id), 201


@auth.route('api/login', methods=['POST'])
def login():
    email = request.json["email"]
    password = request.json["password"]
    
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password): 
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)
            return jsonify(access_token=access_token, refresh_token=refresh_token, id=user.id), 201
    return jsonify(message="Invalid Email or Password"), 403

# @auth.route("api/refresh", methods=["POST"])
# @jwt_required(refresh=True)
# def refresh():
#     identity = get_jwt_identity()
#     access_token = create_access_token(identity=identity)
#     return jsonify(access_token=access_token),201    

@auth.route("api/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token),201   
