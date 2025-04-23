from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('logar/', views.logar, name='logar'),
    path('deslogar/', views.deslogar, name='deslogar'),
    path('solicitar_vendedor', views.solicitar_vendedor, name='solicitar_vendedor'),
    path('perfil/<str:username>', views.perfil, name='perfil_user'),
    path('perfil/editar_perfil/<str:username>', views.editar_perfil, name='editar_perfil'),
    path('perfil/lista_produtos/<str:username>', views.lista_produtos, name='lista_produtos'),
    path('perfil/lista_produtos/editar/<int:id_produto>', views.editar_produto, name='editar_produto'),
    path('perfil/lista_produtos/<str:username>/adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('perfil/lista_produtos/<int:id_produto>/excluir/', views.excluir_produto, name='excluir_produto'),
    path('perfil/vendas/', views.vendas, name='vendas'),
    path('perfil/vendas/<str:order_id>', views.vendas_details, name='vendas_details')
]
