from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Company, User
from .oauth2 import OAuth2
from .permissions import CompanyPermissions, UserPermissions
from .serializers import CompanySerializer, UserSerializer


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
