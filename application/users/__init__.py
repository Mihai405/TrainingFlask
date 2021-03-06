from flask import Blueprint
from flask_restx import Api
from flask_marshmallow import Marshmallow

#Create the blueprint object
users = Blueprint('users', __name__)
ma = Marshmallow(users)
api = Api(users)

#add routes to the blueprint
from .views import UsersList, AuthUser
api.add_resource(UsersList,"/users/")
api.add_resource(AuthUser,"/auth/")
