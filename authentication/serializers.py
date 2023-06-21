from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import User, Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class MyUserCreateSerializer(UserCreateSerializer):
    profile = ProfileSerializer(read_only=True)
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['username', 'email', 'password', 'name', 'lastname', 'profile']

class MyCurrentUserSerializer(UserCreateSerializer):
    profile = ProfileSerializer(read_only=True)
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['id', 'username', 'email', 'name', 'lastname', 'profile']


