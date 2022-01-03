from application.friends.models import Friends
from application.users.models import Users


def test_friend():
    user = Users(email="mihai@yahoo.com", password="mihai", first_name="mihai", last_name="mihai")
    friend = Friends(first_name="mihai", last_name="mihai", number="0234567891", user=user)
    assert friend.first_name == "mihai"
    assert friend.last_name == "mihai"
    assert friend.number == "0234567891"
    assert friend.user_id == user.id

def test_new_users_with_fixture(new_friend):
    assert new_friend.first_name == "mihai"
    assert new_friend.last_name == "mihai"
    assert new_friend.number == "0234567891"

def test_invalid_data(new_friend):
    assert new_friend.first_name != "mihai2"
    assert new_friend.last_name != "mihai2"
    assert new_friend.number != "1234567891"