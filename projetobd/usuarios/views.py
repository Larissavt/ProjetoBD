from django.shortcuts import render, redirect
from django.db import connection

# --- LOGIN E HOME ---

def realizar_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        with connection.cursor() as cursor:
            cursor.execute("SELECT nome FROM usuario WHERE nome = %s AND senha = %s", [username, password])
            usuario = cursor.fetchone()
        if usuario:
            request.session['usuario_nome'] = usuario[0]
            return redirect('home')
        else:
            return render(request, 'usuarios/login.html', {'error': "Usuário ou senha incorretos."})
    return render(request, 'usuarios/login.html')

def home_view(request):
    if not request.session.get('usuario_nome'):
        return redirect('login')
    return render(request, 'usuarios/telaPrincipal.html')

# --- CLIENTES ---

def cliente_view(request):
    clientes = []
    with connection.cursor() as cursor:
        cursor.execute('SELECT id_cliente, nome, email, telefone FROM cliente ORDER BY nome')
        for row in cursor.fetchall():
            clientes.append({'id': row[0], 'nome': row[1], 'email': row[2], 'telefone': row[3]})
    return render(request, 'usuarios/cliente.html', {'clientes': clientes})

def cadastrar_cliente(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        cpf = request.POST.get("cpf")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO cliente (nome, cpf, email, telefone) VALUES (%s, %s, %s, %s)", [nome, cpf, email, telefone])
        return redirect('cliente')
    return render(request, 'usuarios/cadastrar_cliente.html')

def editar_cliente(request, cliente_id):
    if request.method == "POST":
        nome = request.POST.get("nome")
        cpf = request.POST.get("cpf")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")
        with connection.cursor() as cursor:
            cursor.execute("UPDATE cliente SET nome=%s, cpf=%s, email=%s, telefone=%s WHERE id_cliente=%s", [nome, cpf, email, telefone, cliente_id])
        return redirect('cliente')
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_cliente, nome, cpf, email, telefone FROM cliente WHERE id_cliente=%s", [cliente_id])
            row = cursor.fetchone()
        if row:
            cliente = {'id': row[0], 'nome': row[1], 'cpf': row[2], 'email': row[3], 'telefone': row[4]}
            return render(request, 'usuarios/editar_cliente.html', {'cliente': cliente})
        return redirect('cliente')

def excluir_cliente(request, cliente_id):
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM cliente WHERE id_cliente=%s", [cliente_id])
        return redirect('cliente')
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT nome FROM cliente WHERE id_cliente=%s", [cliente_id])
            cliente = cursor.fetchone()
        if cliente:
            return render(request, 'usuarios/confirmar_exclusao.html', {'nome': cliente[0]})
        return redirect('cliente')

# --- PROFISSIONAIS ---

def listar_profissionais(request):
    profissionais = []
    with connection.cursor() as cursor:
        cursor.execute('SELECT id_profissional, nome, especialidade, telefone FROM profissional ORDER BY nome')
        for row in cursor.fetchall():
            profissionais.append({'id': row[0], 'nome': row[1], 'especialidade': row[2], 'telefone': row[3]})
    return render(request, 'usuarios/listar_profissionais.html', {'profissionais': profissionais})

def cadastrar_profissional(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        especialidade = request.POST.get("especialidade")
        telefone = request.POST.get("telefone")
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO profissional (nome, especialidade, telefone) VALUES (%s, %s, %s)", [nome, especialidade, telefone])
        return redirect('listar_profissionais')
    return render(request, 'usuarios/cadastrar_profissional.html')

def editar_profissional(request, profissional_id):
    if request.method == "POST":
        nome = request.POST.get("nome")
        especialidade = request.POST.get("especialidade")
        telefone = request.POST.get("telefone")
        with connection.cursor() as cursor:
            cursor.execute("UPDATE profissional SET nome=%s, especialidade=%s, telefone=%s WHERE id_profissional=%s", [nome, especialidade, telefone, profissional_id])
        return redirect('listar_profissionais')
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_profissional, nome, especialidade, telefone FROM profissional WHERE id_profissional=%s", [profissional_id])
            row = cursor.fetchone()
        if row:
            profissional = {'id': row[0], 'nome': row[1], 'especialidade': row[2], 'telefone': row[3]}
            return render(request, 'usuarios/editar_profissional.html', {'profissional': profissional})
        return redirect('listar_profissionais')

def excluir_profissional(request, profissional_id):
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM profissional WHERE id_profissional=%s", [profissional_id])
        return redirect('listar_profissionais')
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT nome FROM profissional WHERE id_profissional=%s", [profissional_id])
            profissional = cursor.fetchone()
        if profissional:
            return render(request, 'usuarios/excluir_profissional.html', {'profissional': {'id': profissional_id, 'nome': profissional[0]}})
        return redirect('listar_profissionais')

# --- AGENDAMENTO (COM QUERIES SIMPLIFICADAS) ---

def listar_agendamentos(request):
    agendamentos = []
    with connection.cursor() as cursor:
        # Query simplificada: Em vez de JOIN, listamos as tabelas no FROM
        # e conectamos elas usando a cláusula WHERE.
        sql = """
            SELECT 
                a.id_agenda, a.dt_agenda, a.hr_agenda,
                c.nome, p.nome, s.descricao, a.vl_total
            FROM 
                agenda a, cliente c, profissional p, servico s
            WHERE
                a.id_cliente = c.id_cliente AND
                a.id_profissional = p.id_profissional AND
                a.id_servico = s.id_servico
            ORDER BY a.dt_agenda, a.hr_agenda
        """
        cursor.execute(sql)
        for row in cursor.fetchall():
            # Simplificação da data: A formatação da data (de YYYY-MM-DD para DD/MM/YYYY)
            # é feita aqui no Python, em vez de usar TO_CHAR no banco de dados.
            data_formatada = row[1].strftime('%d/%m/%Y') if row[1] else ''
            
            agendamentos.append({
                'id': row[0], 'data': data_formatada, 'hora': row[2],
                'cliente': row[3], 'profissional': row[4],
                'servico': row[5], 'valor': row[6]
            })
    return render(request, 'usuarios/listar_agendamentos.html', {'agendamentos': agendamentos})

def cadastrar_agendamento(request):
    context = {}
    with connection.cursor() as cursor:
        cursor.execute("SELECT ID_Cliente, Nome FROM CLIENTE ORDER BY Nome")
        context['clientes'] = cursor.fetchall()
        cursor.execute("SELECT ID_profissional, Nome FROM PROFISSIONAL ORDER BY Nome")
        context['profissionais'] = cursor.fetchall()
        cursor.execute("SELECT ID_Servico, Descricao FROM SERVICO ORDER BY Descricao")
        context['servicos'] = cursor.fetchall()
        cursor.execute("SELECT ID_Forma_Pagto, Descricao FROM FORMA_PAGTO ORDER BY Descricao")
        context['formas_pagamento'] = cursor.fetchall()

    if request.method == "POST":
        dt_agenda = request.POST.get("dt_agenda")
        hr_agenda = request.POST.get("hr_agenda")
        status = request.POST.get("status", "A")
        vl_total = request.POST.get("vl_total")
        id_cliente = request.POST.get("id_cliente")
        id_forma_pagto = request.POST.get("id_forma_pagto")
        id_profissional = request.POST.get("id_profissional")
        id_servico = request.POST.get("id_servico")
        id_usuario = 1 

        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO AGENDA (DT_Agenda, HR_Agenda, Status, VL_Total, ID_Cliente, ID_Forma_Pagto, ID_profissional, ID_Servico, ID_Usuario) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                [dt_agenda, hr_agenda, status, vl_total, id_cliente, id_forma_pagto, id_profissional, id_servico, id_usuario]
            )
        return redirect('listar_agendamentos')
    
    return render(request, 'usuarios/cadastrar_agendamento.html', context)

def editar_agendamento(request, agenda_id):
    context = {}
    with connection.cursor() as cursor:
        cursor.execute("SELECT ID_Cliente, Nome FROM CLIENTE ORDER BY Nome")
        context['clientes'] = cursor.fetchall()
        cursor.execute("SELECT ID_profissional, Nome FROM PROFISSIONAL ORDER BY Nome")
        context['profissionais'] = cursor.fetchall()
        cursor.execute("SELECT ID_Servico, Descricao FROM SERVICO ORDER BY Descricao")
        context['servicos'] = cursor.fetchall()
        cursor.execute("SELECT ID_Forma_Pagto, Descricao FROM FORMA_PAGTO ORDER BY Descricao")
        context['formas_pagamento'] = cursor.fetchall()

    if request.method == "POST":
        dt_agenda = request.POST.get("dt_agenda")
        hr_agenda = request.POST.get("hr_agenda")
        status = request.POST.get("status")
        vl_total = request.POST.get("vl_total")
        id_cliente = request.POST.get("id_cliente")
        id_forma_pagto = request.POST.get("id_forma_pagto")
        id_profissional = request.POST.get("id_profissional")
        id_servico = request.POST.get("id_servico")
        
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE AGENDA SET DT_Agenda=%s, HR_Agenda=%s, Status=%s, VL_Total=%s, ID_Cliente=%s, 
                ID_Forma_Pagto=%s, ID_profissional=%s, ID_Servico=%s 
                WHERE id_agenda=%s
                """,
                [dt_agenda, hr_agenda, status, vl_total, id_cliente, id_forma_pagto, id_profissional, id_servico, agenda_id]
            )
        return redirect('listar_agendamentos')
    else:
        with connection.cursor() as cursor:
            # Query simplificada: Removemos o TO_CHAR. O HTML <input type="date">
            # já espera o formato padrão 'YYYY-MM-DD' que o banco retorna.
            cursor.execute("SELECT id_agenda, dt_agenda, hr_agenda, status, vl_total, id_cliente, id_forma_pagto, id_profissional, id_servico FROM agenda WHERE id_agenda=%s", [agenda_id])
            row = cursor.fetchone()
        
        if row:
            agendamento = {
                'id': row[0], 'dt_agenda': row[1], 'hr_agenda': str(row[2]), 'status': row[3], 'vl_total': row[4],
                'id_cliente': row[5], 'id_forma_pagto': row[6], 'id_profissional': row[7], 'id_servico': row[8]
            }
            context['agendamento'] = agendamento
            return render(request, 'usuarios/editar_agendamento.html', context)
        return redirect('listar_agendamentos')

def excluir_agendamento(request, agenda_id):
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM agenda WHERE id_agenda=%s", [agenda_id])
        return redirect('listar_agendamentos')
    else:
        with connection.cursor() as cursor:

            sql = """
                SELECT a.dt_agenda, c.nome 
                FROM agenda a, cliente c
                WHERE a.id_agenda=%s AND a.id_cliente = c.id_cliente
            """
            cursor.execute(sql, [agenda_id])
            agendamento = cursor.fetchone()
        
        if agendamento:
            # Formatação da data feita no Python.
            data_formatada = agendamento[0].strftime('%d/%m/%Y') if agendamento[0] else ''
            context = {'id': agenda_id, 'data': data_formatada, 'cliente': agendamento[1]}
            return render(request, 'usuarios/excluir_agendamento.html', context)
        return redirect('listar_agendamentos')

# --- SERVIÇOS ---

def listar_servicos(request):
    servicos = []
    with connection.cursor() as cursor:
        cursor.execute('SELECT id_servico, descricao, preco FROM servico ORDER BY descricao')
        for row in cursor.fetchall():
            servicos.append({'id': row[0], 'descricao': row[1], 'preco': row[2]})
    return render(request, 'usuarios/listar_servicos.html', {'servicos': servicos})

def cadastrar_servico(request):
    if request.method == "POST":
        descricao = request.POST.get("descricao")
        preco = request.POST.get("preco")
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO servico (descricao, preco) VALUES (%s, %s)", [descricao, preco])
        return redirect('listar_servicos')
    return render(request, 'usuarios/cadastrar_servico.html')

def editar_servico(request, servico_id):
    if request.method == "POST":
        descricao = request.POST.get("descricao")
        preco = request.POST.get("preco")
        with connection.cursor() as cursor:
            cursor.execute("UPDATE servico SET descricao=%s, preco=%s WHERE id_servico=%s", [descricao, preco, servico_id])
        return redirect('listar_servicos')
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_servico, descricao, preco FROM servico WHERE id_servico=%s", [servico_id])
            row = cursor.fetchone()
        if row:
            servico = {'id': row[0], 'descricao': row[1], 'preco': row[2]}
            return render(request, 'usuarios/editar_servico.html', {'servico': servico})
        return redirect('listar_servicos')

def excluir_servico(request, servico_id):
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM servico WHERE id_servico=%s", [servico_id])
        return redirect('listar_servicos')
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT descricao FROM servico WHERE id_servico=%s", [servico_id])
            servico = cursor.fetchone()
        if servico:
            return render(request, 'usuarios/excluir_servico.html', {'servico': {'id': servico_id, 'descricao': servico[0]}})
        return redirect('listar_servicos')

# --- FORMAS DE PAGAMENTO ---

def listar_formas_pagamento(request):
    formas_pagamento = []
    with connection.cursor() as cursor:
        cursor.execute('SELECT id_forma_pagto, descricao FROM forma_pagto ORDER BY descricao')
        for row in cursor.fetchall():
            formas_pagamento.append({'id': row[0], 'descricao': row[1]})
    return render(request, 'usuarios/listar_formas_pagamento.html', {'formas_pagamento': formas_pagamento})

def cadastrar_forma_pagamento(request):
    if request.method == "POST":
        descricao = request.POST.get("descricao")
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO forma_pagto (descricao) VALUES (%s)", [descricao])
        return redirect('listar_formas_pagamento')
    return render(request, 'usuarios/cadastrar_forma_pagamento.html')

def editar_forma_pagamento(request, forma_pagto_id):
    if request.method == "POST":
        descricao = request.POST.get("descricao")
        with connection.cursor() as cursor:
            cursor.execute("UPDATE forma_pagto SET descricao=%s WHERE id_forma_pagto=%s", [descricao, forma_pagto_id])
        return redirect('listar_formas_pagamento')
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_forma_pagto, descricao FROM forma_pagto WHERE id_forma_pagto=%s", [forma_pagto_id])
            row = cursor.fetchone()
        if row:
            forma_pagamento = {'id': row[0], 'descricao': row[1]}
            return render(request, 'usuarios/editar_forma_pagamento.html', {'forma_pagamento': forma_pagamento})
        return redirect('listar_formas_pagamento')

def excluir_forma_pagamento(request, forma_pagto_id):
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM forma_pagto WHERE id_forma_pagto=%s", [forma_pagto_id])
        return redirect('listar_formas_pagamento')
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT descricao FROM forma_pagto WHERE id_forma_pagto=%s", [forma_pagto_id])
            forma_pagamento = cursor.fetchone()
        if forma_pagamento:
            context = {'forma_pagamento': {'id': forma_pagto_id, 'descricao': forma_pagamento[0]}}
            return render(request, 'usuarios/excluir_forma_pagamento.html', context)
        return redirect('listar_formas_pagamento')