from django.shortcuts import render, redirect
from .models import Produto
from Usuario.models import Carrinho, ItemCarrinho
from django.shortcuts import get_object_or_404
from django.contrib import messages

def home(request):
    produtos = Produto.objects.all()
    return render(request, 'home.html', {'produtos':produtos})

def produto(request, id_produto):
    produto = get_object_or_404(Produto, id=id_produto)

    if request.method == "GET":
        return render(request, 'produto.html', {'produto':produto})
    elif request.method == "POST":
        if request.user.is_authenticated:
            quantidade = int(request.POST.get('quantidade', 1))
            adicionar_carrinho(request, produto.id, quantidade)
            return render(request, 'produto.html', {'produto':produto})
        else:
            messages.error(request, ("Você deve estar logado para acessar o carrinho"))
            return redirect('logar')

def carrinho(request):
    if request.user.is_authenticated:
        return render(request, 'carrinho.html', {'usuario':request.user})
    else:
        messages.error(request, ("Você deve estar logado para acessar o carrinho"))
        return redirect('logar')
    
def adicionar_carrinho(request, id_produto, quantidade):
    produto = Produto.objects.get(id=id_produto)
    carrinho, criou = Carrinho.objects.get_or_create(usuario=request.user)
    item, criou = ItemCarrinho.objects.get_or_create(carrinho=carrinho, produto=produto)
    
    if item.quantidade + quantidade <= produto.quantidade:
        item.quantidade += quantidade
        item.save()
    else:
        item.quantidade = produto.quantidade
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

def excluir_carrinho(request, id_produto):
    produto = Produto.objects.get(id=id_produto)

    carrinho = Carrinho.objects.filter(usuario=request.user).first()
    
    item = ItemCarrinho.objects.filter(carrinho=carrinho, produto=produto).first()
    if item:
        item.delete()
    return redirect('carrinho')