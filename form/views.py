from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.constants import (LOCATION_CHOICES, MODALITY_CHOICES,
                                      POSITION_CHOICES, SECTOR_CHOICES)


# Create your views here.
class FormViewSet(ViewSet):
    """
    This viewset purpose is to retrieve the form data
    that should be rendered in the UI.
    """

    def list(self, request: Request):
        form_data = {
            'modalities': self.parse_constant(MODALITY_CHOICES),
            'locations': self.parse_constant(LOCATION_CHOICES),
            'positions': self.parse_constant(POSITION_CHOICES),
            'sectors': self.parse_constant(SECTOR_CHOICES),
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
