from django.shortcuts import redirect, get_object_or_404, render
from store.models import Produto, Carrinho, ItemCarrinho
from django.contrib.auth.decorators import login_required

@login_required
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    # Cria ou recupera o carrinho do usuário
    carrinho, criado = Carrinho.objects.get_or_create(usuario=request.user)

    # Verifica se o item já está no carrinho
    item, criado = ItemCarrinho.objects.get_or_create(carrinho=carrinho, produto=produto)

    if not criado:
        item.quantidade += 1
        item.save()

    return redirect('ver_carrinho')

@login_required
def remover_do_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    # Recupera o carrinho do usuário
    carrinho = Carrinho.objects.filter(usuario=request.user).first()
    if not carrinho:
        return redirect('ver_carrinho')

    # Tenta encontrar o item no carrinho
    item = ItemCarrinho.objects.filter(carrinho=carrinho, produto=produto).first()
    if item:
        if item.quantidade > 1:
            item.quantidade -= 1
            item.save()
        else:
            item.delete()
            
    return redirect('ver_carrinho')

def excluir_do_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    # Recupera o carrinho do usuário
    carrinho = Carrinho.objects.filter(usuario=request.user).first()
    if not carrinho:
        return redirect('ver_carrinho')

    # Tenta encontrar o item no carrinho
    item = ItemCarrinho.objects.filter(carrinho=carrinho, produto=produto).first()
    if item:
        item.delete()
            
    return redirect('ver_carrinho')

@login_required
def ver_carrinho(request):
    carrinho, _ = Carrinho.objects.get_or_create(usuario=request.user)
    itens = carrinho.itens.select_related('produto')
    total = carrinho.total()
    
    return render(request, 'carrinho.html', {'itens': itens, 'total': total})