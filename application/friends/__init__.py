from flask import Blueprint
from flask_restx import Api
from flask_marshmallow import Marshmallow

#create blueprint object
friends = Blueprint('friends', __name__)
ma = Marshmallow(friends)
api = Api(friends)

#add routes to the blueprint
from .views import FriendsList, FriendUpdate
api.add_resource(FriendsList,'/friends/')
api.add_resource(FriendUpdate,'/friend/<int:friend_id>/')
