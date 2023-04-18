#IMPORTS
from flask import Blueprint,request,Response,json,make_response,jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, create_access_token,create_refresh_token,get_jwt_identity
import base64
import os

from models import User
from __init__ import db
auth = Blueprint('auth', __name__)


class Signup(Resource):
    def post(self):
        name = request.json["name"]
        email = request.json["email"]
        password = request.json["password"]
        dp = open('bloglite/src/assets/user.png', 'rb').read()
        ext = os.path.splitext('bloglite/src/assets/user.png')[1][1:]
        dp_b64 = base64.b64encode(dp).decode('utf-8')
        dp_mimetype = f'image/{ext}'

        user = User.query.filter_by(email=email).first()
        if user:
            return Response(response=json.dumps({"message": "User Already Exists"}), status=409, mimetype='application/json')
        else:
            new_user = User(email=email, name=name, dp=dp_b64, dp_mimetype=dp_mimetype, password=generate_password_hash(password, method='sha256'))
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)
            db.session.add(new_user)
            db.session.commit()
            return Response(response=json.dumps({"access_token": access_token, "refresh_token": refresh_token, "id": new_user.id}), status=201, mimetype='application/json')


class Login(Resource):
    def post(self):
        email = request.json["email"]
        password = request.json["password"]
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password): 
                access_token = create_access_token(identity=email)
                refresh_token = create_refresh_token(identity=email)
                response_data = {"access_token": access_token, "refresh_token": refresh_token, "id": user.id}
                response = make_response(jsonify(response_data))
                response.status_code = 201
                return response
        response = make_response(jsonify({"message": "Invalid Email or Password"}))
        response.status_code = 403
        return response
    

class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        response = make_response(jsonify(access_token=access_token))
        response.status_code = 201
        return response
