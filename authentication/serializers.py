from djoser.serializers import UserCreateSerializer
from .models import User

class MyUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['username', 'email', 'password', 'name', 'lastname']