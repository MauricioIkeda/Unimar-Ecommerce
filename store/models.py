from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=50)
    preco = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default=1)
    descricao = models.CharField(max_length=255, default='', blank=True, null=True)
    imagem = models.ImageField(upload_to='uploads/produtos/')
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)