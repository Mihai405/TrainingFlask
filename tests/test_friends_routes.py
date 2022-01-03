import json
from application.friends.models import Friends
from flask import session

def test_logIn_session(client):
    with client as c:
        valid_user_payload = json.dumps({
            "email": "mihai@yahoo.com",
            "password": "mihai"
        })
        response = c.post('/auth', headers={"Content-Type": "application/json"}, data=valid_user_payload)
        assert response.status_code == 200
        assert session['user_id'] == 1

def test_get_friends(client):
    response = client.get('/friends')
    assert response.status_code == 401
    valid_user_payload = json.dumps({
        "email": "mihai@yahoo.com",
        "password": "mihai"
    })
    response = client.post('/auth', headers={"Content-Type": "application/json"}, data=valid_user_payload)
    response = client.get('/friends')
    response.status_code == 200


def test_post_friends(client):
    valid_user_payload = json.dumps({
        "email": "mihai@yahoo.com",
        "password": "mihai"
    })
    response = client.post('/auth', headers={"Content-Type": "application/json"}, data=valid_user_payload)

    valid_friends_payload = json.dumps({
        "first_name": "user",
        "last_name": "user",
        "number": "0123456789"
    })
    response = client.post('/friends', headers={"Content-Type": "application/json"}, data=valid_friends_payload)
    response.status_code == 200

    invalid_friends_number = json.dumps({
        "first_name": "user",
        "last_name": "user",
        "number": "012345678910"
    })
    response = client.post('/friends', headers={"Content-Type": "application/json"}, data=invalid_friends_number)
    response.status_code == 401

    invalid_friends_number = json.dumps({
        "first_name": "user",
        "last_name": "user",
        "number": "1234567890"
    })
    response = client.post('/friends', headers={"Content-Type": "application/json"}, data=invalid_friends_number)
    response.status_code == 401

    invalid_friends_number = json.dumps({
        "first_name": "user",
        "last_name": "user",
        "number": "0a34567890"
    })
    response = client.post('/friends', headers={"Content-Type": "application/json"}, data=invalid_friends_number)
    response.status_code == 401

def test_update_friends(client):
    valid_user_payload = json.dumps({
        "email": "mihai@yahoo.com",
        "password": "mihai"
    })
    response = client.post('/auth', headers={"Content-Type": "application/json"}, data=valid_user_payload)

    response = client.get('/friends/10', headers={"Content-Type": "application/json"})
    response.status_code == 404

    response = client.get('/friends/1', headers={"Content-Type": "application/json"})
    response.status_code == 200

    valid_friends_payload = json.dumps({
        "first_name": "mihai3",
        "last_name": "user3",
        "number": "0123456789"
    })
    response = client.put('/friends/1', headers={"Content-Type": "application/json"}, data=valid_friends_payload)
    response.status_code == 200

    invalid_friends_payload = json.dumps({
        "first_name": "mihai3",
        "last_name": "user3",
        "number": "012345678910"
    })
    response = client.put('/friends/1', headers={"Content-Type": "application/json"}, data=invalid_friends_payload)
    response.status_code == 401


def test_delete_friends(client):
    valid_user_payload = json.dumps({
        "email": "mihai@yahoo.com",
        "password": "mihai"
    })
    response = client.post('/auth', headers={"Content-Type": "application/json"}, data=valid_user_payload)

    response = client.delete('/friends/1', headers={"Content-Type": "application/json"})
    response.status_code == 200