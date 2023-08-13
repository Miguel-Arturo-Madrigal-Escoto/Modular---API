from django.db import models

from authentication.models import Company, User


# Create your models here.
class Match(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user_like = models.BooleanField(null=True)
    company_like = models.BooleanField(null=True)
