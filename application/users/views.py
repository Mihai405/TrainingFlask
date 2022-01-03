from flask_restful import Resource
from .models import Users, UsersSchema
from application import db
from flask import request, session, abort
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)

class UsersList(Resource):

    def get(self):
        users=Users.query.all()
        return users_schema.dump(users)

    def post(self):
        try:
            user_schema.load(request.json)
        except ValidationError as err:
            abort(
                400,
                err.messages
            )

        new_user = Users(
            email = request.json["email"],
            password = request.json["password"],
            first_name = request.json["first_name"],
            last_name = request.json["last_name"],
        )

        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                "Error adding in db"
            )
        return user_schema.dump(new_user)

class AuthUser(Resource):
    def post(self):
        email = request.json["email"]
        password = request.json["password"]
        user = Users.query.filter_by(email=email).first()
        if user is None:
            abort(
                400,
                "Invalid email"
            )
        if not user.check_password(password):
            abort(
                400,
                "Invalid password"
            )
        session['user_id']=user.id
        return user_schema.dump(user)
    def delete(self):
        try:
            session.pop("user_id")
        except KeyError:
            abort(
                401,
                "Unauthenticated"
            )
        return "Log Out"