from rest_framework import viewsets
from .models import User, Company
from .serializers import UserSerializer, CompanySerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import UserPermissions, CompanyPermissions

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermissions,)

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (CompanyPermissions,)