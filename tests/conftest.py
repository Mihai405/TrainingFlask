import pytest
import tempfile
import os
from application import db, create_app
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
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": 'sqlite:///' + db_path})
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
