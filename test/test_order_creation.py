import pytest
import requests
from utils.api_client import random_email, get_auth_token

INGREDIENT_HASH = "61c0c5a71d1f82001bdaaa6d"


def test_create_order_authorized(base_url):
    token = get_auth_token(base_url, random_email(), "password123", "Test")
    headers = {"Authorization": token}
    data = {"ingredients": [INGREDIENT_HASH]}
    response = requests.post(f"{base_url}/orders", headers=headers, json=data)
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_create_order_unauthorized(base_url):
    data = {"ingredients": [INGREDIENT_HASH]}
    response = requests.post(f"{base_url}/orders", json=data)
    assert response.status_code == 200
    assert response.json()["success"] is True  # сервис разрешает создание без токена

def test_create_order_no_ingredients(base_url):
    response = requests.post(f"{base_url}/orders", json={"ingredients": []})
    assert response.status_code == 400
    assert response.json()["message"] == "Ingredient ids must be provided"

def test_create_order_invalid_ingredient_hash(base_url):
    data = {"ingredients": ["invalid_hash"]}
    response = requests.post(f"{base_url}/orders", json=data)
    assert response.status_code == 500 or response.status_code == 400
