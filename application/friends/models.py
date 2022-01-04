from application import db
from . import ma
from marshmallow import fields, ValidationError, validates

from application.users.models import UsersSchema

class Friends(db.Model):
    __tablename__ = "friends"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    number = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    user = db.relationship('Users',
        backref=db.backref('friends', lazy=True))

class FriendsSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    number = fields.Str(required=True)
    user = fields.Nested(UsersSchema(only=("id",)),dump_only=True)

    @validates("number")
    def validate_number(self, value):
        if len(value) != 10:
            raise ValidationError("The phone number should contain 10 digits")
        if value[0] != '0':
            raise ValidationError("The phone number should start with 0")
        if value.isdigit() == False:
            raise ValidationError("The phone number should contain only digits")
        return value

    class Meta:
        ordered = True

class UpdateFriendSchema(FriendsSchema):
    first_name = fields.Str()
    last_name = fields.Str()
    number = fields.Str()