import requests
from utils.api_client import random_email
from utils.constants import DEFAULT_PASSWORD, DEFAULT_NAME, WRONG_EMAIL, WRONG_PASSWORD, MSG_INVALID_CREDENTIALS

class TestUserLogin:

    def test_login_existing_user(self, create_user, base_url):
        email = random_email()
        create_user(email, DEFAULT_PASSWORD, DEFAULT_NAME)
        response = requests.post(f"{base_url}/auth/login", json={"email": email, "password": DEFAULT_PASSWORD})
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()

    def test_login_wrong_credentials(self, base_url):
        response = requests.post(f"{base_url}/auth/login", json={"email": "wrong@test.com", WRONG_EMAIL: WRONG_PASSWORD})
        assert response.status_code == 401
        assert response.json()["message"] == MSG_INVALID_CREDENTIALS
