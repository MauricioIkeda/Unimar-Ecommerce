from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('produto/<int:id_produto>', views.produto, name='pagina_produto'),
    path('carrinho/<str:username>', views.carrinho, name='carrinho'),
]
