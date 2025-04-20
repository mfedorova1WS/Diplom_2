import requests
from utils.api_client import random_email
from utils.api_client import random_email, get_auth_token
from utils.constants import (
    DEFAULT_PASSWORD,
    DEFAULT_NAME,
    UPDATED_NAME,
    UNAUTHORIZED_NAME,
    UNAUTHORIZED_EMAIL,
    MSG_UNAUTHORIZED
)

class TestUserUpdate:

    def test_user_update_authorized(self, base_url):
        email = random_email()
        token = get_auth_token(base_url, email, DEFAULT_PASSWORD, DEFAULT_NAME)
        headers = {"Authorization": token}
        payload = {"name": UPDATED_NAME, "email": email, "password": DEFAULT_PASSWORD}
        response = requests.patch(f"{base_url}/auth/user", headers=headers, json=payload)
        assert response.status_code == 200
        assert response.json()["user"]["name"] == UPDATED_NAME

    def test_user_update_unauthorized(self, base_url):
        payload = {"name": UNAUTHORIZED_NAME, "email": UNAUTHORIZED_EMAIL}
        response = requests.patch(f"{base_url}/auth/user", json=payload)
        assert response.status_code == 401
        assert response.json()["message"] == MSG_UNAUTHORIZED
