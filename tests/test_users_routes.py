import json

def test_get_users(client):
    response = client.get('/users/users/')
    assert response.status_code == 200

def test_post_users(client):
    valid_user_payload = json.dumps({
        "email": "postman@yahoo.com",
        "password": "postman",
        "first_name": "postman",
        "last_name": "postman"
    })
    response = client.post('/users/users/' ,headers={"Content-Type": "application/json"}, data=valid_user_payload)
    assert response.status_code == 200

    invalid_user_payload = json.dumps({
        "email": "postman@yahoo.com",
        "password": "postman2",
        "first_name": "postman2",
        "last_name": "postman2"
    })
    response = client.post('/users/users/', headers={"Content-Type": "application/json"}, data=invalid_user_payload)
    assert response.status_code == 400

def test_auth_valid_users(client):
    valid_user_payload = json.dumps({
        "email": "mihai@yahoo.com",
        "password": "mihai"
    })
    response = client.post('/users/auth/', headers={"Content-Type": "application/json"}, data=valid_user_payload)
    assert response.status_code == 200

def test_auth_invalid_password(client):
    invalid_user_payload = json.dumps({
        "email": "mihai@yahoo.com",
        "password": "mihai2"
    })
    response = client.post('/users/auth/', headers={"Content-Type": "application/json"}, data=invalid_user_payload)
    assert response.status_code == 400

def test_auth_invalid_email(client):
    invalid_user_payload = json.dumps({
        "email": "miha2i@yahoo.com",
        "password": "mihai"
    })
    response = client.post('/users/auth/', headers={"Content-Type": "application/json"}, data=invalid_user_payload)
    assert response.status_code == 400

def test_logOut(client):
    valid_user_payload = json.dumps({
        "email": "mihai@yahoo.com",
        "password": "mihai"
    })
    response = client.post('/users/auth/', headers={"Content-Type": "application/json"}, data=valid_user_payload)
    assert response.status_code == 200
    response = client.delete('/users/auth/', headers={"Content-Type": "application/json"}, data=valid_user_payload)
    assert response.status_code == 200
    assert b"Log Out" in response.data
    response = client.delete('/users/auth/', headers={"Content-Type": "application/json"}, data=valid_user_payload)
    assert response.status_code == 401
    assert b'{"message": "Unauthenticated"}\n' in response.data
