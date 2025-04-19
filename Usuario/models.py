from django.db import models
from django.contrib.auth.models import User
from Store.models import Produto

# Create your models here.
class Profile(models.Model):
    usuario = models.OneToOneField(User, related_name='perfil',on_delete=models.CASCADE)
    vendedor = models.BooleanField(default=False)
    foto = models.ImageField(upload_to='uploads/fotos_perfil/', default='uploads/fotos_perfil/DefaultProfileImage.png')
    bios = models.CharField(max_length=255, default='Olá, este é o meu Perfil!')

    def __str__(self):
        return self.usuario.first_name
    
class Carrinho(models.Model):
    usuario = models.OneToOneField(User, related_name='carrinho' ,on_delete=models.CASCADE)

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.produto.preco * self.quantidade