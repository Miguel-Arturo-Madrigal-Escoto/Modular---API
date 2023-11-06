from django.core.validators import (MaxLengthValidator, MinLengthValidator,
                                    URLValidator)
from django.db import models

from authentication.models import Company


# Create your models here.
class Role(models.Model):
    position = models.CharField(max_length=50, unique=True, blank=False, validators=[
        MinLengthValidator(5),
        MaxLengthValidator(50)
    ])


class CompanyRoles(models.Model):
    name = models.CharField(validators=[
        MinLengthValidator(5)
    ])
    description = models.TextField(validators=[
        MinLengthValidator(20),
    ])
    link = models.TextField(validators=[
        URLValidator()
    ])
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
