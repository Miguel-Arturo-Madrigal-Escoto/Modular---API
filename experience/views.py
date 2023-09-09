from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
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

    def list(self, request: Request):
        try:
            user_id = request.query_params.get('user_id', '')
            experiences = self.get_queryset().filter(user=user_id)
            serializer = self.get_serializer(instance=experiences, many=True)
            return Response(serializer.data)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
