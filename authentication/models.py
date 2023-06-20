from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager


# Create your models here.
class Profile(models.Model):
    position = models.CharField(max_length=50)
    expected_salary = models.FloatField()
    modality = models.CharField(max_length=10)
    location = models.CharField(max_length=50)
    image = models.TextField(null=True)


class User(AbstractBaseUser):
    username = models.CharField(
        unique=True,
        max_length=50
    )
    email = models.EmailField(
        unique=True,
        max_length=255
    )
    # password provided automatically
    name = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    is_active = models.BooleanField(default=False) # email verification
    google_id = models.CharField(max_length=255, null=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='user')
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'lastname', 'password']