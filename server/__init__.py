#IMPORTS
from flask import Flask
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from os import path
# from celeryTasks import celery

db = SQLAlchemy()
ma = Marshmallow()
DB_NAME = "bloglite.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '18102001'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authorization'
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)
    app.config["JWT_SECRET_KEY"] = "jwtkey"
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    
    db.init_app(app)
    ma.init_app(app)
    
    CORS(app)
    
    jwt = JWTManager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(email=identity).one_or_none()
    
    # app.app_context().push()

    # celery = Celery(
    #     app.name,
    #     broker=app.config['CELERY_BROKER_URL'],
    #     backend=app.config['CELERY_RESULT_BACKEND']
    # )

    # celery.conf.task_routes = {
    #     'app.celeryTasks.*': {'queue': 'default'}
    # }

    # app.celery = celery
    # celery.conf.update(app.config)
    
    from auth import auth
    from blog import blog
    from profile import profile

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(blog, url_prefix='/')
    app.register_blueprint(profile, url_prefix='/')

    from models import User, Blog, Like, Comment

    create_database(app)
    return app


def create_database(app):
    if not path.exists('backend/instance' + DB_NAME):
        with app.app_context():
            db.create_all()
            # print('Created Database!')
