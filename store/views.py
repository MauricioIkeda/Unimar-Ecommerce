from django.shortcuts import render
from .models import Produto
from django.shortcuts import get_object_or_404

def home(request):
    produtos = Produto.objects.all()
    return render(request, 'home.html', {'produtos':produtos})

def produto(request, id_produto):
    produto = get_object_or_404(Produto, id=id_produto)
    return render(request, 'produto.html', {'produto':produto})

def carrinho(request):
    return render(request, 'carrinho.html', {})