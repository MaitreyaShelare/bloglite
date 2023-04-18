from flask_restful import Api
from auth import Signup, Login, Refresh


def register_resources(app):
    api = Api(app)
    api.add_resource(Signup, "/api/signup")
    api.add_resource(Login, "/api/login")
    api.add_resource(Refresh, "/api/refresh")