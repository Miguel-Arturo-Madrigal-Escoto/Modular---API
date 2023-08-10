from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Sector
from .serializers import SectorSerializer


# Create your views here.
class SectorsAPIView(ListCreateAPIView):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    permission_classes = (IsAuthenticated, )

    def list(self, request: Request):
        try:
            sector = self.get_queryset().get(name=request.query_params.get('name'))
            serializer = self.get_serializer(instance=sector)
            return Response(serializer.data)

        except Sector.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
