from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import uuid

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

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendedor = models.ForeignKey(User, related_name='order_seller', on_delete=models.CASCADE)
    comprador = models.ForeignKey(User, related_name='order_buyer', on_delete=models.CASCADE)
    valor_total_pedido = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=50, default='pendente')
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {str(self.id)} - {self.comprador.username} - {self.status} - {self.data.strftime('%Y-%m-%d %H:%M')}"

    @property
    def calcular_valor_total(self):
        return sum(item.subtotal for item in self.itens.all())