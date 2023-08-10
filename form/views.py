from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.constants import LOCATION_CHOICES, MODALITY_CHOICES
from roles.models import Role
from sectors.models import Sector


# Create your views here.
class FormViewSet(ViewSet):
    """
    This viewset purpose is to retrieve the form data
    that should be rendered in the UI.
    """
    permission_classes = (IsAuthenticated, )

    def list(self, request: Request):
        form_data = {
            'modalities': self.parse_constant(MODALITY_CHOICES),
            'locations': self.parse_constant(LOCATION_CHOICES),
            'positions': self.get_roles(),
            'sectors': self.get_sectors()
        }
        return Response(form_data, status=200)

    def parse_constant(self, constant):
        form_data = []
        for idx, value in enumerate(constant):
            form_data.append({
                'value': value[0],
                'display': value[1],
                'id': idx + 1
            })
        return form_data

    def get_roles(self):
        try:
            response = []
            roles = Role.objects.all()
            for role in roles:
                response.append({
                    'value': role.position,
                    'display': f'{ role.position }'.capitalize(),
                    'id': role.pk
                })
            return response
        except Exception:
            return []

    def get_sectors(self):
        try:
            response = []
            sectors = Sector.objects.all()
            for sector in sectors:
                response.append({
                    'value': sector.name,
                    'display': f'{ sector.name }'.capitalize(),
                    'id': sector.pk
                })
            return response
        except Exception:
            return []
