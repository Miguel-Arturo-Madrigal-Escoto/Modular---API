from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager

# Create your models here.
class BaseUser(AbstractBaseUser):
    username = models.CharField(
        unique=True,
        max_length=50
    )
    email = models.EmailField(
        unique=True,
        max_length=255
    )
    # password provided automatically
    is_active = models.BooleanField(default=False) # email verification
    # google_id = models.CharField(max_length=255, null=True)
    
    # django required fields
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']


class User(models.Model):
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    expected_salary = models.FloatField()
    modality = models.CharField(max_length=10)
    location = models.CharField(max_length=50)
    image = models.TextField(null=True)
    base_user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='user')

class Company(models.Model):
    name = models.CharField(max_length=50)
    about = models.TextField()
    verified = models.BooleanField(default=False)
    base_user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='company')

