from rest_framework.serializers import ModelSerializer

from .models import Experience


class ExperienceSerializer(ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'
