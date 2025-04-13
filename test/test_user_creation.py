import pytest
import random
import string

import requests


def random_email():
    return ''.join(random.choices(string.ascii_lowercase, k=7)) + "@test.com"


def test_create_unique_user(create_user):
    response = create_user(random_email(), "password123", "Test User")
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_create_existing_user(create_user):
    email = random_email()
    create_user(email, "password123", "Test User")
    response = create_user(email, "password123", "Test User")
    assert response.status_code == 403
    assert response.json()["message"] == "User already exists"


@pytest.mark.parametrize("missing_field", [
    {"email": "", "password": "pass123", "name": "User"},
    {"email": "user@test.com", "password": "", "name": "User"},
    {"email": "user@test.com", "password": "pass123", "name": ""}
])
def test_create_user_missing_fields(base_url, missing_field):
    response = requests.post(f"{base_url}/auth/register", json=missing_field)
    assert response.status_code == 403
    assert response.json()["message"] == "Email, password and name are required fields"
