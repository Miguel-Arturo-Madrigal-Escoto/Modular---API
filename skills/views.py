from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
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

    def list(self, request: Request):
        try:
            skills = self.get_queryset().filter(user=request.user.user.id)
            serializer = self.get_serializer(instance=skills, many=True)
            return Response(serializer.data)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
