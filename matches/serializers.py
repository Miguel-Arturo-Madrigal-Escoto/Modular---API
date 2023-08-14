from rest_framework.serializers import ModelSerializer

from .models import Match


class MatchSerializer(ModelSerializer):

    class Meta:
        model = Match
        fields = '__all__'
