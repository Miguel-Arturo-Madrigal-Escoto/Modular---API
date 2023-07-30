from django.db import models

from authentication import constants
from authentication.models import Company


# Create your models here.
class Role(models.Model):
    position = models.CharField(max_length=50, choices=constants.POSITION_CHOICES)


class CompanyRoles(models.Model):
    description = models.TextField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
