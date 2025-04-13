import requests
from utils.api_client import random_email

def test_login_existing_user(create_user, base_url):
    email = random_email()
    password = "pass123"
    create_user(email, password, "User")
    response = requests.post(f"{base_url}/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "accessToken" in response.json()

def test_login_wrong_credentials(base_url):
    response = requests.post(f"{base_url}/auth/login", json={"email": "wrong@test.com", "password": "badpass"})
    assert response.status_code == 401
    assert response.json()["message"] == "email or password are incorrect"
