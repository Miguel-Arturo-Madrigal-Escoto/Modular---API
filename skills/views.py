from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Skill
from .permissions import SkillsPermissions
from .serializers import SkillSerializer


# Create your views here.
class SkillViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = (IsAuthenticated, SkillsPermissions)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
