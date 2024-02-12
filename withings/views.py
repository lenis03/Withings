# Importing the required modules
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import WeightRecord
import requests
from .serializers import WeightSerializer

# Defining the constants for the Withings API
WITHINGS_CLIENT_ID = "C95a81700f3b41f85045913166168479208be836632b7634ce49d09ff53b17d6"
WITHINGS_CLIENT_SECRET = "157f794d869ca64df0e5bdadc541ed9e7c48da13629299039fbed668e3f6987b"
REDIRECT_URI = "YOUR_REDIRECT_URI"
AUTHORIZE_URL = "https://account.withings.com/oauth2/authorize2"
TOKEN_URL = "https://account.withings.com/oauth2/token"

# Defining the WeightView class that handles the weight data
class WeightView(APIView):
    """
    A class that handles the POST request for getting and saving the user's weight data
    from the Withings API.
    It expects a JSON data with the user_id field.
    It returns a JSON response with the weight field or an error message.
    """
    def post(self, request):
        # Validating the request data using the WeightSerializer
        serializer = WeightSerializer(data=request.data)
        if serializer.is_valid():
            # Getting the user_id from the validated data
            user_id = serializer.validated_data.get('user_id')
            # Getting the access token from the environment variable or a file
            access_token = "YOUR_ACCESS_TOKEN_HERE"
            
            # Setting the URL, headers, and parameters for the Withings API request
            url = "https://wbsapi.withings.net/measure"
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            params = {
                "action": "getmeas",
                "meastype": 1,  # weight measurement
                "userid": user_id
            }
            # Sending the GET request to the Withings API and getting the response
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            # Checking if the response contains the weight data
            if "body" in data and "measuregrps" in data["body"]:
                # Getting the weight value from the response data
                weight = data["body"]["measuregrps"][0]["measures"][0]["value"]
                # Creating a WeightRecord object and saving it to the database
                WeightRecord.objects.create(user_id=user_id, weight=weight)
                # Returning a success response with the weight value
                return Response({"weight": weight}, status=status.HTTP_200_OK)
            # Returning an error response if the weight data is not found
            return Response({"message": "Error retrieving weight data"}, status=status.HTTP_400_BAD_REQUEST)
        # Returning an error response if the request data is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
