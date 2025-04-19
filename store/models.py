from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=50)
    preco = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default=1)
    descricao = models.CharField(max_length=255, default='', blank=True, null=True)
    quantidade = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    imagem = models.ImageField(upload_to='uploads/produtos/')
    vendedor = models.ForeignKey(User, related_name='produtos', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
    
