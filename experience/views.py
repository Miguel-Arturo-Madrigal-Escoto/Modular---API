from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Experience
from .permissions import ExperiencePermissions
from .serializers import ExperienceSerializer


# Create your views here.
class ExperienceViewSet(ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated, ExperiencePermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
