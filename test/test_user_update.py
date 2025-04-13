import pytest
import requests
from utils.api_client import random_email


def get_auth_token(base_url, email, password, name):
    requests.post(f"{base_url}/auth/register", json={"email": email, "password": password, "name": name})
    login = requests.post(f"{base_url}/auth/login", json={"email": email, "password": password})
    return login.json()["accessToken"]


def test_user_update_authorized(base_url):
    email = random_email()
    token = get_auth_token(base_url, email, "password123", "User")
    headers = {"Authorization": token}
    payload = {"name": "New Name", "email": email, "password": "password123"}
    response = requests.patch(f"{base_url}/auth/user", headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json()["user"]["name"] == "New Name"

def test_user_update_unauthorized(base_url):
    payload = {"name": "Hacker Name", "email": "hacker@test.com"}
    response = requests.patch(f"{base_url}/auth/user", json=payload)
    assert response.status_code == 401
    assert response.json()["message"] == "You should be authorised"
