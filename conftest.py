import pytest
import requests

BASE_URL = "https://stellarburgers.nomoreparties.site/api"

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture
def create_user():
    def _create_user(email, password, name):
        return requests.post(f"{BASE_URL}/auth/register", json={
            "email": email,
            "password": password,
            "name": name
        })
    return _create_user
