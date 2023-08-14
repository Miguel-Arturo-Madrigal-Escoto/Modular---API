import ast

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import CompanyRoles, Role
from .permissions import CompanyRolesPermissions
from .serializers import CompanyRolesSerializer, RoleSerializer


# Create your views here.
class RolesAPIView(ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = (IsAuthenticated, )

    def list(self, request: Request):
        try:
            role = self.get_queryset().get(position=request.query_params.get('position'))
            serializer = self.get_serializer(instance=role)
            return Response(serializer.data)

        except Role.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CompanyRolesViewSet(ModelViewSet):
    queryset = CompanyRoles.objects.all()
    serializer_class = CompanyRolesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
    permission_classes = (IsAuthenticated, CompanyRolesPermissions)

    def list(self, request: Request):
        try:
            roles = self.get_queryset().filter(company=request.user.company.id)
            serializer = self.get_serializer(instance=roles, many=True)
            return Response(serializer.data)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False)
    def add_roles(self, request: Request):
        errors = {}

        try:
            for role in request.data['roles']:
                role_position = role.get('position', '')
                current_role = Role.objects.get(position=role_position)
                company_role = CompanyRoles(
                    name=role.get('name', ''),
                    description=role.get('description', ''),
                    link=role.get('link', ''),
                    company_id=request.user.company.id,
                    role_id=current_role.pk
                )
                company_role.save()

            return Response(status=status.HTTP_201_CREATED)

        except Role.DoesNotExist as e:
            errors[role_position] = str(e)

        except Exception as e:
            errors[role_position] = ast.literal_eval(str(e))

        if errors:
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
