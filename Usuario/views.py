from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Order
from Store.models import Produto
from django.core.files.storage import FileSystemStorage
import os

def cadastrar(request):
    if request.method == "GET":
        return render(request, 'cadastrar.html')
    elif request.method == "POST":
        username = request.POST.get('usuario') 
        nome = request.POST.get('nome')
        password1 = request.POST.get('senha1')
        password2 = request.POST.get('senha2')
        if password1 != password2:
            messages.error(request, ("Senhas diferentes! tente novamente!"))
            return redirect('cadastrar')
        else:
            user = User.objects.filter(username=username)

            if user:
                 messages.error(request, ("O username já está cadastrado, tente novamente!"))
                 return redirect('cadastrar') 
            
            user = User.objects.create_user(username=username, password=password1, first_name=nome)
            user.save()


            messages.success(request, ("Cadastrado com sucesso! Faça seu login!"))
            return redirect('logar')

def logar(request):
    if request.method == 'GET':
        return render(request, 'logar.html')
    elif request.method == 'POST':
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        user = authenticate(request, username=usuario, password=senha)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, ("Usuario ou senha incorreto, tente novamente!"))
            return redirect('logar')

def deslogar(request):
        logout(request)
        return redirect('home')

def solicitar_vendedor(request):
    return render(request, 'solicitar_vendedor.html')

def perfil(request, username):
    usuario = User.objects.get(username=username)

    return render(request, 'perfil_usuario.html', {'usuario':usuario})

def editar_perfil(request, username):
    usuario = User.objects.get(username=username)

    if request.method == 'GET':
        if request.user.username == username:
            return render(request, 'editar_perfil.html', {'usuario':usuario})
        else:
            return redirect('home')

    elif request.method == 'POST':
        if 'salvar' in request.POST:
            nome = request.POST.get('nome')
            bios = request.POST.get('bios')
            imagem = request.FILES.get('foto_perfil')

            if nome:
                usuario.first_name = nome
                usuario.save()

            if bios:
                usuario.perfil.bios = bios

            if imagem:
                perfil = usuario.perfil
                caminho_imagem_default = perfil._meta.get_field('foto').default

                if perfil.foto and perfil.foto.name != caminho_imagem_default:
                    if os.path.isfile(perfil.foto.path):
                        os.remove(perfil.foto.path)
                fs = FileSystemStorage(location='media/uploads/fotos_perfil/', base_url='/media/uploads/fotos_perfil/')
                filename = fs.save(imagem.name, imagem)
                usuario.perfil.foto = 'uploads/fotos_perfil/' + filename 

            usuario.perfil.save()

            return redirect('perfil_user', username=username)
        elif 'excluir' in request.POST:
            perfil = usuario.perfil
            caminho_imagem_default = perfil._meta.get_field('foto').default

            if perfil.foto and perfil.foto.name != caminho_imagem_default:
                if os.path.isfile(perfil.foto.path):
                    os.remove(perfil.foto.path)

            user = request.user
            user.delete()
            logout(request)
            return redirect('home')
    
def lista_produtos(request, username):
    usuario = User.objects.get(username=username)

    if request.user.username == username:
        return render(request, 'lista_produtos.html', {'usuario':usuario, 'usuariousername':username})
    else:
        return redirect('home')

def editar_produto(request, id_produto):
    produto = Produto.objects.get(id=id_produto)
    usuario = User.objects.get(id=produto.vendedor.id)

    if request.method == "GET":
        if request.user == usuario:
            return render(request, 'editar_produto.html', {'produto':produto})
        else:
            return redirect('home')
    elif request.method == "POST":
        produto.nome = request.POST.get('nome')
        produto.descricao = request.POST.get('descricao')
        produto.preco = request.POST.get('preco')
        produto.quantidade = request.POST.get('quantidade_estoque')
        imagem = request.FILES.get('imagem')

        if imagem:
            fs = FileSystemStorage(location='media/uploads/produtos/', base_url='/media/uploads/produtos/')
            filename = fs.save(imagem.name, imagem)
            produto.imagem = 'uploads/produtos/' + filename 
        
        produto.save()

        return redirect('perfil_user', username=usuario.username)
    
def adicionar_produto(request, username):
    if request.user.is_authenticated:
        perfil = get_object_or_404(Profile, usuario=request.user)
    else:
        return redirect('home')

    if request.method == 'GET':
        if perfil.vendedor and request.user.username == username:
            return render(request, 'adicionar_produto.html', {'usuariousername':username})
        else:
            return redirect('home')

    elif request.method == 'POST':
        produto = Produto.objects.create(vendedor=request.user)
        produto.nome = request.POST.get('nome')
        produto.descricao = request.POST.get('descricao')
        produto.preco = request.POST.get('preco')
        produto.quantidade = request.POST.get('quantidade_estoque')
        imagem = request.FILES.get('imagem')

        fs = FileSystemStorage(location='media/uploads/produtos/', base_url='/media/uploads/produtos/')
        filename = fs.save(imagem.name, imagem)
        produto.imagem = 'uploads/produtos/' + filename 
        
        produto.save()

        return redirect('perfil_user', username=request.user.username)
    
def excluir_produto(request, id_produto):
    produto = get_object_or_404(Produto, id=id_produto)

    if request.method == 'POST':

        if produto.imagem:
            imagem_path = produto.imagem.path
            if os.path.exists(imagem_path):
                os.remove(imagem_path)
        produto.delete()
        return redirect('lista_produtos', username=request.user.username)
    
    return redirect('lista_produtos', username=request.user.username)

def vendas(request):
    orders = request.user.order_seller.all()
    return render(request, 'vendas.html', {'orders':orders})

def vendas_details(request, order_id):
    order = Order.objects.get(id=order_id)
    itemOrders = order.itens.all()
    return render(request, 'vendas_details.html', {'itemOrders': itemOrders})
