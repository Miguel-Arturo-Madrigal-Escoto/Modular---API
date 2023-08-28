import datetime
from enum import Enum

from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import (MaxLengthValidator, MinLengthValidator,
                                    MinValueValidator)
from django.db import models
from mongoengine import (BooleanField, DateTimeField, Document, EmailField,
                         EnumField, IntField)

from .constants import LOCATION_CHOICES, MODALITY_CHOICES
from .managers import CustomUserManager


# Create your models here.
class BaseUser(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=50)
    email = models.EmailField(unique=True, max_length=255)
    # password provided automatically
    is_active = models.BooleanField(default=False)  # email verification

    # django required fields
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']


class User(models.Model):
    name = models.CharField(max_length=50, validators=[
        MinLengthValidator(3),
        MaxLengthValidator(50),
    ])
    lastname = models.CharField(max_length=50, validators=[
        MinLengthValidator(3),
        MaxLengthValidator(50),
    ])
    position = models.ForeignKey('roles.Role', on_delete=models.CASCADE)
    expected_salary = models.FloatField(validators=[
        MinValueValidator(0)
    ])
    modality = models.CharField(max_length=10, choices=MODALITY_CHOICES)
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    about = models.TextField(validators=[
        MinLengthValidator(20)
    ])
    image = models.ImageField(upload_to='images/user', null=True)
    base_user = models.OneToOneField(
        BaseUser, on_delete=models.CASCADE, related_name='user'
    )


class Company(models.Model):
    name = models.CharField(max_length=50, validators=[
        MinLengthValidator(3),
        MaxLengthValidator(50),
    ])
    about = models.TextField(validators=[
        MinLengthValidator(20)
    ])
    mission = models.TextField(validators=[
        MinLengthValidator(20)
    ])
    vision = models.TextField(validators=[
        MinLengthValidator(20)
    ])
    verified = models.BooleanField(default=False)
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    sector = models.ForeignKey('sectors.Sector', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/company', null=True)
    base_user = models.OneToOneField(
        BaseUser, on_delete=models.CASCADE, related_name='company'
    )

class MongoUserRoleEnum(Enum):
    USER = 'user'
    COMPANY = 'company'

class MongoUser(Document):
    """
        This model will be used to populate the user collection
        in MongoDB when running the factories in order to make
        data persistent for the chat via MongoEngine ODM.
    """
    base_user = IntField(min_value=1)
    email = EmailField()
    role = EnumField(MongoUserRoleEnum, choices=[MongoUserRoleEnum.USER, MongoUserRoleEnum.COMPANY])
    online = BooleanField(default=False)
    createdAt = DateTimeField(default=datetime.datetime.now())
    updatedAt = DateTimeField(default=datetime.datetime.now())
    meta = {
        'collection': 'users'
    }
