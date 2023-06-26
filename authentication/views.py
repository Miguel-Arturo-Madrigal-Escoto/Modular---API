from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from .permissions import UserPermissions, CompanyPermissions
from .models import User, Company
from .serializers import UserSerializer, CompanySerializer
from .oauth2 import OAuth2

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
        oauth2 = OAuth2(provider='google', request=request)
        try:
            oauth_response = oauth2.authenticate()
            return Response(oauth_response, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    