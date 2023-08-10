from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models

from authentication.models import User


# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length=40, validators=[
        MinLengthValidator(5),
        MaxLengthValidator(40)
    ])
    description = models.TextField(validators=[
        MinLengthValidator(20)
    ])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
