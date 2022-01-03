from sqlalchemy.ext.hybrid import hybrid_property
from application import bcrypt

from application import db
from . import ma
from marshmallow import fields, validates, ValidationError

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    _password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, string):
        self._password = bcrypt.generate_password_hash(string)

    def check_password(self,string):
        return bcrypt.check_password_hash(self._password,string)

class UsersSchema(ma.Schema):
    id = fields.Int()
    email = fields.Email(required=True)
    password = fields.Str(load_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)

    @validates("email")
    def validate_email(self, value):
        user = Users.query.filter_by(email=value).first()
        if user is not None:
            raise ValidationError("This email already exists")
        return value

    class Meta:
        ordered = True