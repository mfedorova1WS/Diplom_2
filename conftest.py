import pytest
import requests

BASE_URL = "https://stellarburgers.nomoreparties.site/api"

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture
def create_user():
    created_users = []
    def _create_user(email, password, name):
        response = requests.post(f"{BASE_URL}/auth/register", json={
            "email": email,
            "password": password,
            "name": name
        })
        if response.status_code == 200:
            # Получаем токен для удаления
            login_response = requests.post(f"{BASE_URL}/auth/login", json={
                "email": email,
                "password": password
            })
            token = login_response.json().get("accessToken")
            created_users.append(token)
        return response

    yield _create_user

    # Удаляем созданных пользователей
    for token in created_users:
        if token:
            headers = {"Authorization": token}
            requests.delete(f"{BASE_URL}/auth/user", headers=headers)