from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('produto/<int:id_produto>', views.produto, name='pagina_produto'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('carrinho/adicionar/<int:id_produto>/<int:quantidade>', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/remover/<int:id_produto>', views.remover_carrinho, name='remover_carrinho'),
    path('carrinho/excluir/<int:id_produto>', views.excluir_carrinho, name='excluir_carrinho'),
]
