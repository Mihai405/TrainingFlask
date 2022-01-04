from flask_restful import Resource
from flask import request, session, abort
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from .models import Friends , FriendsSchema, UpdateFriendSchema
from application.users.models import Users
from application import db, cache

friend_schema = FriendsSchema()
friends_schema = FriendsSchema(many=True)

class FriendsList(Resource):
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

class FriendUpdate(Resource):
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