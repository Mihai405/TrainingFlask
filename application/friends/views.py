from flask_restx import Resource, fields
from flask import request, session, abort
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from .models import Friends , FriendsSchema, UpdateFriendSchema
from application.users.models import Users
from application import db, cache
from . import api

friend_schema = FriendsSchema()
friends_schema = FriendsSchema(many=True)

user_fields = api.model('User', {
    "id" : fields.Integer()
})

friend_fields = api.model('Friend',{
    "first_name" : fields.String(required=True),
    "last_name" : fields.String(required=True),
    "number" : fields.String(required=True),
    "user" : fields.Nested(user_fields)
})

friend_create_fields = api.model('FriendCreate',{
    "first_name" : fields.String(required=True),
    "last_name" : fields.String(required=True),
    "number" : fields.String(required=True),
})

class FriendsList(Resource):

    @api.doc(responses={401: 'Unauthorized'})
    @api.marshal_with(friend_fields, as_list=True)
    @cache.cached(timeout=500)
    def get(self):
        try:
            session["user_id"]
        except KeyError:
            abort(
                401,
                "Unauthenticated"
            )
        friends=Friends.query.filter_by(user_id=session["user_id"]).all()
        return friends_schema.dump(friends)

    @api.doc(responses={200: ('Success', friend_fields), 401: 'Unauthorized', 400:'Bad Request'},
             body=friend_create_fields)
    def post(self):
        try:
            session["user_id"]
        except KeyError:
            abort(
                401,
                "Unauthenticated"
            )
        try:
            friend_schema.load(request.json)
        except ValidationError as err:
            abort(
                400,
                err.messages
            )

        new_friend = Friends(
            first_name = request.json["first_name"],
            last_name = request.json["last_name"],
            number = request.json["number"],
            user=Users.query.get(session["user_id"])
        )
        try:
            db.session.add(new_friend)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                "Error adding in db"
            )
        cache.clear()
        return friend_schema.dump(new_friend)


update_friend_schema = UpdateFriendSchema()

friend_update_fields = api.model('FriendUpdate',{
    "first_name" : fields.String(),
    "last_name" : fields.String(),
    "number" : fields.String(),
})

class FriendUpdate(Resource):

    @api.doc(responses={200: ('Success', friend_fields), 401: 'Unauthorized', 400:'Bad Request'})
    @cache.cached(timeout=500)
    def get(self, friend_id):
        try:
            session["user_id"]
        except KeyError:
            abort(
                401,
                "Unauthenticated"
            )

        friend = Friends.query.filter(and_(Friends.id==friend_id, Friends.user_id==session["user_id"])).first()

        if friend is None:
            abort(
                404,
                "Friend not found"
            )
        return friend_schema.dump(friend)

    @api.doc(responses={200: ('Success', friend_fields), 401: 'Unauthorized', 400:'Bad Request'},
             body=friend_update_fields)
    def put(self, friend_id):
        try:
            session["user_id"]
        except KeyError:
            abort(
                401,
                "Unauthenticated"
            )

        friend = Friends.query.filter(and_(Friends.id == friend_id, Friends.user_id == session["user_id"])).first()

        if friend is None:
            abort(
                404,
                "Friend not found"
            )

        try:
            update_friend_schema.load(request.json)
        except ValidationError as err:
            abort(
                400,
                err.messages
            )

        if "first_name" in request.json:
            friend.first_name = request.json["first_name"]

        if "last_name" in request.json:
            friend.last_name = request.json["last_name"]

        if "number" in request.json:
            friend.number = request.json["number"]

        try:
            db.session.add(friend)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                "Error adding in db"
            )
        cache.clear()
        return friend_schema.dump(friend)

    @api.doc(responses={200: 'Success', 401: 'Unauthorized', 400:'Bad Request'})
    def delete(self, friend_id):
        try:
            session["user_id"]
        except KeyError:
            abort(
                401,
                "Unauthenticated"
            )

        friend = Friends.query.filter(and_(Friends.id == friend_id, Friends.user_id == session["user_id"])).first()

        if friend is None:
            abort(
                404,
                "Friend not found"
            )

        try:
            db.session.delete(friend)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                "Error adding in db"
            )
        cache.clear()
        return f"Deleted friend with friend id {friend_id}"