from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from .permissions import UserPermissions, CompanyPermissions
from .models import User, Company
from .serializers import UserSerializer, CompanySerializer
import requests
import os

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermissions,)

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (CompanyPermissions,)

class GoogleOAuth2(APIView):
    def get(self, request: Request):
        session_id = request.COOKIES.get('sessionid')
        oauth_url = os.environ.get('SOCIAL_AUTH_GOOGLE_AUTHENTICATE_URI', '')

        params = {
            'state': request.query_params.get('state', ''),
            'code': request.query_params.get('code', ''),
            'scope': request.query_params.get('scope', ''),
            'authuser': request.query_params.get('authuser', ''),
            'prompt': request.query_params.get('prompt', ''),
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': f'sessionid={ session_id }'
        }
        
        api_response = requests.post(oauth_url, params=params, headers=headers)
        return Response(api_response.json())
    