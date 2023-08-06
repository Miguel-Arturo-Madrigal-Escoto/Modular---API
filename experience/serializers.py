from rest_framework.serializers import ModelSerializer
from roles.serializers import RoleSerializer
from .models import Experience

class ExperienceSerializer(ModelSerializer):
    #role = RoleSerializer()

    class Meta:
        model = Experience
        fields = '__all__'