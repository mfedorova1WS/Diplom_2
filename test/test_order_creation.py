import requests
from utils.api_client import random_email, get_auth_token
from utils.constants import VALID_INGREDIENT_HASH, INVALID_INGREDIENT_HASH, MSG_NO_INGREDIENTS, DEFAULT_PASSWORD, DEFAULT_NAME

class TestOrderCreation:

    def test_create_order_authorized(self,base_url):
        token = get_auth_token(base_url, random_email(), DEFAULT_PASSWORD, DEFAULT_NAME)
        headers = {"Authorization": token}
        data = {"ingredients": [VALID_INGREDIENT_HASH]}
        response = requests.post(f"{base_url}/orders", headers=headers, json=data)
        assert response.status_code == 200
        assert response.json()["success"] is True

    def test_create_order_unauthorized(self,base_url):
        data = {"ingredients": [VALID_INGREDIENT_HASH]}
        response = requests.post(f"{base_url}/orders", json=data)
        assert response.status_code == 200
        assert response.json()["success"] is True  # сервис разрешает создание без токена

    def test_create_order_no_ingredients(self,base_url):
        response = requests.post(f"{base_url}/orders", json={"ingredients": []})
        assert response.status_code == 400
        assert response.json()["message"] == MSG_NO_INGREDIENTS

    def test_create_order_invalid_ingredient_hash(self,base_url):
        data = {"ingredients": [INVALID_INGREDIENT_HASH]}
        response = requests.post(f"{base_url}/orders", json=data)
        assert response.status_code == 500 or response.status_code == 400
