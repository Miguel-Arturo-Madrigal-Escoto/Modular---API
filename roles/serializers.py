from rest_framework.serializers import ModelSerializer

from .models import CompanyRoles, Role


class RoleSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Role

class CompanyRolesSerializer(ModelSerializer):
    role = RoleSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = CompanyRoles
