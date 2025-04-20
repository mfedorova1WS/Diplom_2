import pytest
import requests
from utils.api_client import random_email
from utils.constants import DEFAULT_PASSWORD, DEFAULT_NAME, MSG_USER_EXISTS, MSG_REQUIRED_FIELDS

class TestUserCreation:

    def test_create_unique_user(self, create_user):
        response = create_user(random_email(), DEFAULT_PASSWORD, DEFAULT_NAME)
        assert response.status_code == 200
        assert response.json()["success"] is True

    def test_create_existing_user(self, create_user):
        email = random_email()
        create_user(email, DEFAULT_PASSWORD, DEFAULT_NAME)
        response = create_user(email, DEFAULT_PASSWORD, DEFAULT_NAME)
        assert response.status_code == 403
        assert response.json()["message"] == MSG_USER_EXISTS


@pytest.mark.parametrize("missing_field", [
    {"email": "", "password": DEFAULT_PASSWORD, "name": DEFAULT_NAME},
    {"email": "user@test.com", "password": "", "name": DEFAULT_NAME},
    {"email": "user@test.com", "password": DEFAULT_PASSWORD, "name": ""}
])
def test_create_user_missing_fields(base_url, missing_field):
    response = requests.post(f"{base_url}/auth/register", json=missing_field)
    assert response.status_code == 403
    assert response.json()["message"] == MSG_REQUIRED_FIELDS
