from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import CompanyRoles, Role
from .serializers import CompanyRolesSerializer


# Create your views here.
class CompanyRolesViewSet(ModelViewSet):
    queryset = CompanyRoles.objects.all()
    serializer_class = CompanyRolesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    @action(methods=['POST'], detail=False)
    def add_roles(self, request: Request):
        try:
            for role in request.data['roles']:
                current_role = Role.objects.get(position=role['position'])
                company_role = CompanyRoles(
                    name=role['name'],
                    description=role['description'],
                    link=role['link'],
                    company_id=request.data['company_id'],
                    role_id=current_role.pk
                )
                company_role.save()

            return Response(status=status.HTTP_201_CREATED)

        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
