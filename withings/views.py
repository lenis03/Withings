from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import WeightRecord
import requests
from .serializers import WeightSerializer

CLIENT_ID = "C95a81700f3b41f85045913166168479208be836632b7634ce49d09ff53b17d6"
CLIENT_SECRET = "157f794d869ca64df0e5bdadc541ed9e7c48da13629299039fbed668e3f6987b"
REDIRECT_URI = "YOUR_REDIRECT_URI"
AUTHORIZE_URL = "https://account.withings.com/oauth2/authorize2"
TOKEN_URL = "https://account.withings.com/oauth2/token"


class WeightView(APIView):
    def post(self, request):
        serializer = WeightSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get('user_id')
            access_token = "YOUR_ACCESS_TOKEN_HERE"

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
            
            if "body" in data and "measuregrps" in data["body"]:
                weight = data["body"]["measuregrps"][0]["measures"][0]["value"]
                WeightRecord.objects.create(user_id=user_id, weight=weight)
                return Response({"weight": weight}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Error retrieving weight data"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
