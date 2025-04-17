from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('logar/', views.logar, name='logar'),
    path('deslogar/', views.deslogar, name='deslogar'),
    path('solicitar_vendedor', views.solicitar_vendedor, name='solicitar_vendedor'),
    path('perfil/<str:username>', views.perfil, name='perfil_user')
]
