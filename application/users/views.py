from flask_restx import Resource, fields
from .models import Users, UsersSchema
from application import db, cache
from flask import request, session, abort
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from . import api

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)

user_fields = api.model('User',{
    "id" : fields.Integer(required=True),
    "email": fields.String(required=True),
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True)
})

user_create_fields = api.model('UserCreate',{
    "email": fields.String(required=True),
    "password": fields.String(required=True),
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True)
})

user_logIn_fields = api.model('UserLogIn',{
    "email": fields.String(required=True),
    "password": fields.String(required=True),
})

class UsersList(Resource):

    @api.doc(responses={400: 'Bad Request'})
    @api.marshal_with(user_fields, as_list=True)
    def get(self):
        users=Users.query.all()
        return users_schema.dump(users)

    @api.doc(responses={200: ('Success', user_fields), 400:'Bad Request', 401: 'Unauthorized'}, body=user_create_fields)
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
        cache.clear()
        return user_schema.dump(new_user)

class AuthUser(Resource):

    @api.doc(responses={200: ('Success', user_fields), 400: 'Bad Request'},body=user_logIn_fields)
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

    @api.doc(responses={200: ('Success', user_fields), 400: 'Bad Request'})
    def delete(self):
        try:
            session.pop("user_id")
        except KeyError:
            abort(
                401,
                "Unauthenticated"
            )
        cache.clear()
        return "Log Out"