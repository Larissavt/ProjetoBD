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

    # Rotas para Profissionais
    path('profissionais/', views.listar_profissionais, name='listar_profissionais'),
    path('profissionais/novo/', views.cadastrar_profissional, name='cadastrar_profissional'),
    path('profissionais/editar/<int:profissional_id>/', views.editar_profissional, name='editar_profissional'),
    path('profissionais/excluir/<int:profissional_id>/', views.excluir_profissional, name='excluir_profissional'),

    # Rotas para Agendamentos 
    path('agendamentos/', views.listar_agendamentos, name='listar_agendamentos'),
    path('agendamentos/novo/', views.cadastrar_agendamento, name='cadastrar_agendamento'),
    path('agendamentos/editar/<int:agenda_id>/', views.editar_agendamento, name='editar_agendamento'),
    path('agendamentos/excluir/<int:agenda_id>/', views.excluir_agendamento, name='excluir_agendamento'),

    # Rotas para Serviços
    path('servicos/', views.listar_servicos, name='listar_servicos'),
    path('servicos/novo/', views.cadastrar_servico, name='cadastrar_servico'),
    path('servicos/editar/<int:servico_id>/', views.editar_servico, name='editar_servico'),
    path('servicos/excluir/<int:servico_id>/', views.excluir_servico, name='excluir_servico'),

    # Rotas para Formas de Pagamento
    path('formas-pagamento/', views.listar_formas_pagamento, name='listar_formas_pagamento'),
    path('formas-pagamento/nova/', views.cadastrar_forma_pagamento, name='cadastrar_forma_pagamento'),
    path('formas-pagamento/editar/<int:forma_pagto_id>/', views.editar_forma_pagamento, name='editar_forma_pagamento'),
    path('formas-pagamento/excluir/<int:forma_pagto_id>/', views.excluir_forma_pagamento, name='excluir_forma_pagamento'),
]