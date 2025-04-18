from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from Store.models import Produto
from django.core.files.storage import FileSystemStorage

def cadastrar(request):
    if request.method == "GET":
        return render(request, 'cadastrar.html')
    elif request.method == "POST":
        username = request.POST.get('usuario') 
        nome = request.POST.get('nome')
        password1 = request.POST.get('senha1')
        password2 = request.POST.get('senha2')
        if password1 != password2:
            messages.success(request, ("Senhas diferentes! tente novamente!"))
            return redirect('cadastrar')
        else:
            user = User.objects.filter(username=username)

            if user:
                 messages.success(request, ("O username já está cadastrado, tente novamente!"))
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
            messages.success(request, ("Usuario ou senha incorreto, tente novamente!"))
            return redirect('logar')

def deslogar(request):
        logout(request)
        return redirect('home')

def solicitar_vendedor(request):
    return render(request, 'solicitar_vendedor.html')

def perfil(request, username):
    usuario = User.objects.get(username=username)
    profile = Profile.objects.get(usuario=usuario)
    produtos = Produto.objects.filter(vendedor=usuario)

    return render(request, 'perfil_usuario.html', {'profile':profile, 'produtos':produtos, 'usuario':usuario})

def editar_perfil(request, username):
    usuario = User.objects.get(username=username)
    perfil = Profile.objects.get(usuario=usuario)

    if request.method == 'GET':
        if request.user.username == username:
            return render(request, 'editar_perfil.html', {'usuario':usuario, 'perfil':perfil})
        else:
            return redirect('home')

    elif request.method == 'POST':
        nome = request.POST.get('nome')
        bios = request.POST.get('bios')
        imagem = request.FILES.get('foto_perfil')

        if nome:
            usuario.first_name = nome
            usuario.save()

        if bios:
            perfil.bios = bios

        if imagem:
            fs = FileSystemStorage(location='media/uploads/fotos_perfil/', base_url='/media/uploads/fotos_perfil/')
            filename = fs.save(imagem.name, imagem)
            perfil.foto = 'uploads/fotos_perfil/' + filename 

        perfil.save()

        return redirect('perfil_user', username=username)
    
def lista_produtos(request, username):
    usuario = User.objects.get(username=username)
    produtos = Produto.objects.filter(vendedor=usuario)
    return render(request, 'lista_produtos.html', {'produtos':produtos})

def editar_produto(request, id_produto):
    produto = Produto.objects.get(id=id_produto)
    usuario = User.objects.get(id=produto.vendedor.id)

    if request.method == "GET":
        return render(request, 'editar_produto.html', {'produto':produto})
    elif request.method == "POST":
        produto.nome = request.POST.get('nome')
        produto.descricao = request.POST.get('descricao')
        produto.preco = request.POST.get('preco')
        imagem = request.FILES.get('imagem')

        if imagem:
            fs = FileSystemStorage(location='media/uploads/produtos/', base_url='/media/uploads/produtos/')
            filename = fs.save(imagem.name, imagem)
            produto.imagem = 'uploads/produtos/' + filename 
        
        produto.save()

        return redirect('perfil_user', username=usuario.username)