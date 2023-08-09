from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet
from .models import Skill
from .serializers import SkillSerializer

# Create your views here.
class SkillViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    # permission_classes = [IsAuthenticated,]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'