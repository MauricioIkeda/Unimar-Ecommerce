from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    vendedor = models.BooleanField(default=False)