#IMPORTS
from flask import Blueprint,request,jsonify
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token,create_refresh_token
from __init__ import db
auth = Blueprint('auth', __name__)

@auth.route('api/signup', methods=['POST'])
def signup():
    name = request.json["name"]
    email = request.json["email"]
    password = request.json["password"]
    
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(message="User Already Exists"), 409
    else:
            new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
            access_token = create_access_token(identity=email)
            db.session.add(new_user)
            db.session.commit()
            return jsonify(message="User added sucessfully", access_token=access_token), 201


@auth.route('api/login', methods=['POST'])
def login():
    email = request.json["email"]
    password = request.json["password"]
    
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password): 
            access_token = create_access_token(identity=email)
            return jsonify(message="Login Succeeded!", access_token=access_token), 201
    return jsonify(message="Invalid Email or Password"), 401
