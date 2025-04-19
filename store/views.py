from django.shortcuts import render, redirect
from .models import Produto
from Usuario.models import Carrinho, ItemCarrinho
from django.shortcuts import get_object_or_404

def home(request):
    produtos = Produto.objects.all()
    return render(request, 'home.html', {'produtos':produtos})

def produto(request, id_produto):
    produto = get_object_or_404(Produto, id=id_produto)

    if request.method == "GET":
        return render(request, 'produto.html', {'produto':produto})
    elif request.method == "POST":
        adicionar_carrinho(request, produto.id)
        return render(request, 'produto.html', {'produto':produto})

def carrinho(request):
    if request.user.is_authenticated:
        return render(request, 'carrinho.html', {'usuario':request.user})
    else:
        return redirect('logar')
    
def adicionar_carrinho(request, id_produto):
    produto = Produto.objects.get(id=id_produto)
    carrinho, criou = Carrinho.objects.get_or_create(usuario=request.user)
    item, criou = ItemCarrinho.objects.get_or_create(carrinho=carrinho, produto=produto)
    
    if not criou:
        if produto.quantidade > item.quantidade:
            item.quantidade += 1
            item.save()

    return redirect('carrinho')

def remover_carrinho(request, id_produto):
    produto = Produto.objects.get(id=id_produto)

    carrinho = Carrinho.objects.filter(usuario=request.user).first()
    if not carrinho:
        return redirect('carrinho')
    
    item = ItemCarrinho.objects.filter(carrinho=carrinho, produto=produto).first()
    if item:
        if item.quantidade > 1:
            item.quantidade -= 1
            item.save()
        else:
            item.delete()

    return redirect('carrinho')