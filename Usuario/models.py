from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    vendedor = models.BooleanField(default=False)
    foto = models.ImageField(upload_to='uploads/fotos_perfil/', default='uploads/fotos_perfil/DefaultProfileImage.png')
    bios = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.usuario.first_name