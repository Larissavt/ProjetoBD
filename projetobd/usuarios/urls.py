from django.urls import path
from . import views


urlpatterns = [
    # Rota de login
    path('login/', views.realizar_login, name='login'),

    # Tela principal (home)
    path('home/', views.home_view, name='home'),

    # Rotas para clientes
    path('cliente/', views.cliente_view, name='cliente'),
    path('clientes/novo/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('clientes/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/excluir/<int:cliente_id>/', views.excluir_cliente, name='excluir_cliente'),
    # Rota para cadastro de profissionais
     path('profissional/', views.cadastrar_profissional, name='profissional'),
     path('profissionais/', views.listar_profissionais, name='listar_profissionais'),

     
]