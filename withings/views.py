from django.shortcuts import render
import requests

CLIENT_ID = "C95a81700f3b41f85045913166168479208be836632b7634ce49d09ff53b17d6"
CLIENT_SECRET = "157f794d869ca64df0e5bdadc541ed9e7c48da13629299039fbed668e3f6987b"
REDIRECT_URI = "http://127.0.0.1:8000/withings/callback/"
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


def get_user_weight(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://wbsapi.withings.net/measure?action=getmeas"
    response = requests.get(url, headers=headers)
    return response.json()


def weight_view(request):
    authorize_url = get_authorize_url()
    
    if request.method == 'GET':
        code = request.GET.get('code')
        
        if code:
            access_token_data = get_access_token(code)
            access_token = access_token_data["access_token"]
            user_weight_data = get_user_weight(access_token)
            weight = user_weight_data["body"]["measures"][0]["value"] / 1000  # convert to kilograms
            return render(request, 'withings/weight.html', {'weight': weight})
        
        return render(request, 'withings/authorize.html', {'authorize_url': authorize_url})