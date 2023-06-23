from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import BaseUser, User, Company

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class MyBaseUserCreateSerializer(UserCreateSerializer):
    user = UserSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    class Meta(UserCreateSerializer.Meta):
        model = BaseUser
        fields = ['username', 'email', 'password', 'user', 'company']

class MyBaseCurrentUserSerializer(UserCreateSerializer):
    user = UserSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    class Meta(UserCreateSerializer.Meta):
        model = BaseUser
        fields = ['id', 'username', 'email', 'name', 'lastname', 'user', 'company']


