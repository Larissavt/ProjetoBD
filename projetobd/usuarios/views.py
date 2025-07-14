#meus imports 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render, redirect
from django.db import connection
from django.shortcuts import render, redirect
from .models import Profissional 

#Criando a conexão do Login
def realizar_login(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Consulta ajustada: só busca nome na tabela usuario
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT nome FROM usuario WHERE nome = %s AND senha = %s",
                [username, password]
            )
            usuario = cursor.fetchone()

        if usuario:
            # Como só trouxe o nome, pega direto do resultado
            (nome,) = usuario
            request.session['usuario_nome'] = nome
            return redirect('home')
        else:
            error = "Usuário ou senha incorretos."

    return render(request, 'usuarios/login.html', {'error': error})


def home(request):
    if not request.session.get('usuario_nome'):
        return redirect('login')
    return render(request, 'usuarios/telaPrincipal.html', {
        'usuario_nome': request.session['usuario_nome'],
    })
# fim do login 


#meu cliente 
def cliente_view(request):
    clientes = []
    with connection.cursor() as cursor:
        cursor.execute('SELECT id_cliente, nome, email, telefone FROM cliente order by nome')
        for row in cursor.fetchall():
            clientes.append({
                'id': row[0],         
                'nome': row[1],
                'email': row[2],
                'telefone': row[3],
            })
    return render(request, 'usuarios/cliente.html', {'clientes': clientes})

#Função para cadastrar um novo cliente
def cadastrar_cliente(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")
        cpf = request.POST.get("cpf")
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO cliente (nome, cpf, email, telefone) VALUES (%s, %s, %s, %s)",
                [nome, cpf, email, telefone]
            )
        return redirect('cliente')
    return render(request, 'usuarios/cadastrar_cliente.html')

#Função para editar um cliente
def editar_cliente(request, cliente_id):
    if request.method == "POST":
        nome = request.POST.get("nome")
        cpf = request.POST.get("cpf")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE cliente SET nome=%s, cpf=%s, email=%s, telefone=%s WHERE id_cliente=%s",
                [nome, cpf, email, telefone, cliente_id]
            )
        return redirect('cliente')
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT nome, cpf, email, telefone FROM cliente WHERE id_cliente=%s", [cliente_id])
            cliente = cursor.fetchone()
        if cliente:
            context = {
                'id': cliente_id,
                'nome': cliente[0],
                'cpf': cliente[1],
                'email': cliente[2],
                'telefone': cliente[3],
            }
            return render(request, 'usuarios/editar_cliente.html', context)
        else:
            return redirect('cliente')

def excluir_cliente(request, cliente_id):
    # Busca o cliente no banco de dados
    with connection.cursor() as cursor:
        cursor.execute('SELECT nome FROM cliente WHERE id_cliente=%s', [cliente_id])
        row = cursor.fetchone()

    # Se o cliente não for encontrado, redireciona para a lista de clientes
    if not row:
        return redirect('cliente')

    # Nome do cliente (usado para a confirmação)
    nome = row[0]

    # Se for uma requisição POST, exclui o cliente
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM cliente WHERE id_cliente=%s', [cliente_id])
        return redirect('cliente')  # Redireciona após excluir o cliente

    # Se for uma requisição GET, exibe a página de confirmação
    return render(request, 'usuarios/confirmar_exclusao.html', {'nome': nome})

    
#minha tela principal
def home_view (request):
    return render(request,'usuarios/telaPrincipal.html')
#meu agendamento
def agendamento_view (request):
    return render (request, 'usuarios/agendamento.html')


#PROFISSIONAL 

def cadastrar_profissional(request):
    if request.method == 'POST':  # Verifica se o formulário foi submetido
        # Captura os dados do formulário
        nome = request.POST.get('nome')  # Obtém o campo do formulário pelo "name"
        especialidade = request.POST.get('especialidade')
        telefone = request.POST.get('telefone')

        # Insere os dados no banco usando o modelo Profissional
        Profissional.objects.create(
            nome=nome,
            especialidade=especialidade,
            telefone=telefone
        )

        # Redireciona para a página de listagem ou outra página
        return redirect('profissional')  # Substitua pela página de listagem se preferir

    # Se for uma requisição GET, apenas renderiza o formulário
    return render(request, 'usuarios/cadastrar_profissional.html')

def listar_profissionais(request):
    profissionais = Profissional.objects.all()  # Busca todos os registros
    return render(request, 'usuarios/listar_profissionais.html', {'profissionais': profissionais})


