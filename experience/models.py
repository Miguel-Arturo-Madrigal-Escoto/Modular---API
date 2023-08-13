from datetime import date

from django.core.validators import MaxValueValidator, MinLengthValidator
from django.db import models

from authentication.models import User
from roles.models import Role


# Create your models here.
class Experience(models.Model):
    start_date = models.DateField(validators=[
        MaxValueValidator(limit_value=date.today()),
    ])
    end_date = models.DateField(validators=[
        MaxValueValidator(limit_value=date.today())
    ])
    description = models.TextField(validators=[
        MinLengthValidator(20)
    ])
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
