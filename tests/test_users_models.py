from application.users.models import Users

def test_new_user():
    user = Users(email="mihai@yahoo.com", password="mihai", first_name="mihai", last_name="mihai")
    assert user.email == "mihai@yahoo.com"
    assert user.check_password("mihai")
    assert user.first_name == "mihai"
    assert user.last_name == "mihai"

def test_new_users_with_fixture(new_user):
    assert new_user.email == "mihai@yahoo.com"
    assert new_user.password != "mihai"
    assert new_user.check_password("mihai")

def test_setting_password(new_user):
    assert new_user.password != "mihai"
    assert new_user.check_password("mihai")
    assert not new_user.check_password("mihai2")
