from djoser.serializers import UserCreateSerializer
from djoser.serializers import UserSerializer as USerializer
from rest_framework import serializers

from .models import BaseUser, Company, User


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
        fields = ['id', 'username', 'email', 'password', 'user', 'company']


class MyBaseCurrentUserSerializer(USerializer):
    user = UserSerializer(read_only=True)
    company = CompanySerializer(read_only=True)

    class Meta(UserCreateSerializer.Meta):
        model = BaseUser
        fields = ['id', 'username', 'email', 'user', 'company', 'created_at', 'updated_at']
