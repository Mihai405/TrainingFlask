import pytest
import tempfile
from flask import Flask
from flask_bcrypt import Bcrypt
import os
from application import db
from application.users.models import Users
from application.friends.models import Friends

@pytest.fixture
def new_user():
    user = Users(email="mihai@yahoo.com", password="mihai", first_name="mihai", last_name="mihai")
    return user

@pytest.fixture
def new_friend():
    user = Users(email="mihai@yahoo.com", password="mihai", first_name="mihai", last_name="mihai")
    friend = Friends(first_name="mihai", last_name="mihai", number="0234567891", user=user)
    return friend

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    basedir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    bcrypt = Bcrypt(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.testing = True
    db.init_app(app)
    # local imports
    from application.friends import friends
    from application.users import users
    app.register_blueprint(friends)
    app.register_blueprint(users)
    with app.app_context():
        db.create_all()
        u = Users(email="mihai@yahoo.com", password="mihai", first_name="mihai", last_name="mihai")
        f = Friends(first_name="mihai", last_name="mihai", number="0234567891", user=u)
        db.session.add(u)
        db.session.commit()
    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    client = app.test_client()
    yield client
