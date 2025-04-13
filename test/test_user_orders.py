import requests
from utils.api_client import random_email, get_auth_token


def test_get_user_orders_authorized(base_url):
    token = get_auth_token(base_url, random_email(), "password123", "Test")
    headers = {"Authorization": token}
    response = requests.get(f"{base_url}/orders", headers=headers)
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_get_user_orders_unauthorized(base_url):
    response = requests.get(f"{base_url}/orders")
    assert response.status_code == 401
    assert response.json()["message"] == "You should be authorised"
