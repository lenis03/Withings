import requests
from django.shortcuts import render
from .models import WeightRecord

CLIENT_ID = "C95a81700f3b41f85045913166168479208be836632b7634ce49d09ff53b17d6"
CLIENT_SECRET = "157f794d869ca64df0e5bdadc541ed9e7c48da13629299039fbed668e3f6987b"
REDIRECT_URI = "YOUR_REDIRECT_URI"
AUTHORIZE_URL = "https://account.withings.com/oauth2/authorize2"
TOKEN_URL = "https://account.withings.com/oauth2/token"


def get_authorize_url(mode="normal"):
    scopes = "user.info,user.metrics,user.activity"
    if mode == "demo":
        scopes += ",device.setup"
    return f"{AUTHORIZE_URL}?response_type=code&client_id={CLIENT_ID}&state=a_random_value&scope={scopes}&redirect_uri={REDIRECT_URI}&mode={mode}"


def get_access_token(code):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }
    response = requests.post(TOKEN_URL, data=data)
    return response.json()


def refresh_access_token(refresh_token):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }
    response = requests.post(TOKEN_URL, data=data)
    return response.json()


def get_weight_from_withings_api(user_id, access_token):
    url = "https://wbsapi.withings.net/measure"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "action": "getmeas",
        "meastype": 1,  # weight measurement
        "userid": user_id
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    if "body" in data:
        weight = data["body"]["measuregrps"][0]["measures"][0]["value"]
        return weight
    else:
        return None


def fetch_user_weight(request, user_id):
    # Replace "?" with the actual access token obtained through OAuth 2.0
    access_token = "YOUR_ACCESS_TOKEN_HERE"
    weight = get_weight_from_withings_api(user_id, access_token)
    if weight:
        WeightRecord.objects.create(user_id=user_id, weight=weight)
        return render(request, "success.html", {"weight": weight})
    else:
        return render(request, "error.html")
