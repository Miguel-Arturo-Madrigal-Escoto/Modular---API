from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import User, Profile

class MyUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['username', 'email', 'password', 'name', 'lastname', 'profile']

class MyCurrentUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['id', 'username', 'email', 'name', 'lastname', 'profile']

class ProfileSerializer(serializers.ModelSerializer):
    user = MyUserCreateSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'

