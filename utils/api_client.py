import random
import string
import requests

BASE_URL = "https://stellarburgers.nomoreparties.site/api"

def random_email():
    return ''.join(random.choices(string.ascii_lowercase, k=7)) + "@test.com"

def get_auth_token(base_url, email, password, name):
    requests.post(f"{base_url}/auth/register", json={"email": email, "password": password, "name": name})
    login = requests.post(f"{base_url}/auth/login", json={"email": email, "password": password})
    return login.json()["accessToken"]
