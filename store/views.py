from django.shortcuts import render
from .models import Produto

# Create your views here.
def home(request):
    produtos = Produto.objects.all()
    return render(request, 'home.html', {'produtos':produtos})

def product(request, pk):
    product = Produto.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})