from django.db import models
from authentication.models import User
from django.core.validators import MinLengthValidator
from roles.models import Role

# Create your models here.
class Experience(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(validators=[
        MinLengthValidator(20)
    ])
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    user =  models.ForeignKey(User, on_delete=models.CASCADE)