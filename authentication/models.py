from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager

# Create your models here.
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
    # profile_id

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'lastname', 'password']