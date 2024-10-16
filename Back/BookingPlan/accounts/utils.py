import requests
from django.conf import settings

def initiate_payment(phone_number, amount, description):
    url = f"{settings.CAMPAY_BASE_URL}/collect/"
    headers = {
        'Authorization': f"Token {get_access_token()}",
        'Content-Type': 'application/json'
    }
    data = {
        "amount": amount,
        "from": phone_number,
        "description": description,
        "external_reference": "your_unique_reference"
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def get_access_token():
    url = f"{settings.CAMPAY_BASE_URL}/token/"
    data = {
        'client_id': settings.CAMPAY_CLIENT_KEY,
        'client_secret': settings.CAMPAY_CLIENT_SECRET
    }
    response = requests.post(url, data=data)
    response_data = response.json()
    return response_data['token']
