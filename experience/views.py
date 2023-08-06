from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Experience
from .serializers import ExperienceSerializer
from .permissions import ExperiencePermission

# Create your views here.
class ExperienceViewSet(ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    #permission_classes = [IsAuthenticated, ExperiencePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
