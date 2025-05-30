from django.shortcuts import render, redirect
from .models import Produto
from Usuario.models import Carrinho, ItemCarrinho, Order, ItemOrder
from django.shortcuts import get_object_or_404
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from collections import defaultdict

from apimercadopago import realizar_pagamento
from dotenv import load_dotenv
import os
import mercadopago

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

def pagamento(request):
    carrinho = Carrinho.objects.filter(usuario=request.user).first()

    itens_por_vendedor = defaultdict(list)
    for item in carrinho.itens.all():
        itens_por_vendedor[item.produto.vendedor].append(item)

    payment_items = []
    total_geral = 0
    pedidos_criados = []

    for vendedor, itens in itens_por_vendedor.items():
        order = Order.objects.create(
            vendedor=vendedor,
            comprador=request.user
        )

        for item in itens:
            item_order = ItemOrder.objects.create(
                order=order,
                produto=item.produto,
                quantidade=item.quantidade,
                preco=item.produto.preco
            )

            total_geral = item.quantidade * item.produto.preco

            payment_items.append({
                "id": str(item.produto.id),
                "title": item.produto.nome,
                "quantity": item.quantidade,
                "currency_id": "BRL",
                "unit_price": float(item.produto.preco)
            })

        order.valor_total_pedido = total_geral  # Atualizando o valor total do pedido
        order.save()
        pedidos_criados.append(order)

    link_pagamento = realizar_pagamento(payment_items)
    request.session['pedidos_ids'] = [str(pedido.id) for pedido in pedidos_criados]

    return redirect(link_pagamento)

@csrf_exempt
def mercadopago_webhook(request):
    load_dotenv()
    if request.method == 'POST':
        data = json.loads(request.body)

        payment_id = data.get("data", {}).get("id")

        if payment_id:
            sdk = mercadopago.SDK(f'{os.getenv("MP_ACCESS_TOKEN")}')

            payment_response = sdk.payment().get(payment_id)
            payment_status = payment_response["response"]["status"]

            if payment_status == "approved":
                carrinho = Carrinho.objects.filter(usuario=request.user).first()

                for item in carrinho.itens.all():
                    item.produto.quantidade -= item.quantidade
                    item.produto.save()
                print("Pagamento aprovado!")
        
        return JsonResponse({"status": "ok"})

def compra_success(request):
    return render(request, 'compra_success.html', {})


def compra_failure(request):
    return render(request, 'compra_failure.html', {})

def compra_pending(request):
    return render(request, 'compra_pending.html', {})