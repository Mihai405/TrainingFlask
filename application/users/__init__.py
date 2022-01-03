from flask import Blueprint
from flask_restful import Api
from flask_marshmallow import Marshmallow


users = Blueprint('users', __name__)
ma = Marshmallow(users)
api = Api(users)

from .views import UsersList, AuthUser
api.add_resource(UsersList,"/users")
api.add_resource(AuthUser,"/auth")
