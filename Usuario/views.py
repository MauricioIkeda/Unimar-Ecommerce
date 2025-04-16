from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

def cadastrar(request):
    if request.method == "GET":
        return render(request, 'cadastrar.html')
    elif request.method == "POST":
        username = request.POST.get('usuario') 
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
            
            user = User.objects.create_user(username=username, password=password1)
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