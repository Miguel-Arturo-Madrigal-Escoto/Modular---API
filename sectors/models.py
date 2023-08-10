from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models


# Create your models here.
class Sector(models.Model):
    name = models.CharField(max_length=50, unique=True, validators=[
        MinLengthValidator(5),
        MaxLengthValidator(50)
    ])
