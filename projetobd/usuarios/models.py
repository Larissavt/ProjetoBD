# usuarios/models.py
from django.db import models

class FormaPagto(models.Model):
    # O Django usa 'id' por defeito, que corresponde a 'ID_Forma_Pagto SERIAL PRIMARY KEY'
    id_forma_pagto = models.AutoField(primary_key=True, db_column='id_forma_pagto')
    descricao = models.CharField(max_length=100, db_column='descricao')

    class Meta:
        managed = False  # Diz ao Django para não tocar nesta tabela
        db_table = 'forma_pagto' # Nome exato da tabela no PostgreSQL (normalmente em minúsculas)
        verbose_name = "Forma de Pagamento"
        verbose_name_plural = "Formas de Pagamento"

    def __str__(self):
        return self.descricao

class Profissional(models.Model):
    id_profissional = models.AutoField(primary_key=True, db_column='id_profissional')
    nome = models.CharField(max_length=100, db_column='nome')
    especialidade = models.CharField(max_length=100, db_column='especialidade')
    telefone = models.CharField(max_length=20, db_column='telefone')

    class Meta:
        managed = False
        db_table = 'profissional'

    def __str__(self):
        return self.nome

class Servico(models.Model):
    id_servico = models.AutoField(primary_key=True, db_column='id_servico')
    descricao = models.CharField(max_length=100, db_column='descricao')
    # O seu Preco é NUMERIC(4,2). O DecimalField é o correspondente correto.
    preco = models.DecimalField(max_digits=4, decimal_places=2, db_column='preco')

    class Meta:
        managed = False
        db_table = 'servico'
        verbose_name_plural = "Serviços"

    def __str__(self):
        return self.descricao

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True, db_column='id_usuario')
    nome = models.CharField(max_length=100, db_column='nome')
    login = models.CharField(max_length=30, db_column='login')
    senha = models.CharField(max_length=20, db_column='senha') # ATENÇÃO: Guardar senhas em texto plano não é seguro!
    ativo = models.CharField(max_length=1, db_column='ativo')

    class Meta:
        managed = False
        db_table = 'usuario'

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    # Aqui está o modelo para a sua tabela CLIENTE
    id_cliente = models.AutoField(primary_key=True, db_column='id_cliente')
    nome = models.CharField(max_length=100, db_column='nome')
    cpf = models.CharField(max_length=14, db_column='cpf')
    email = models.EmailField(max_length=100, db_column='email')
    telefone = models.CharField(max_length=20, db_column='telefone')

    class Meta:
        managed = False
        db_table = 'cliente' # Mapeamento para a tabela 'cliente'

    def __str__(self):
        return self.nome

class Agenda(models.Model):
    id_agenda = models.AutoField(primary_key=True, db_column='id_agenda')
    dt_agenda = models.DateField(db_column='dt_agenda')
    hr_agenda = models.TimeField(db_column='hr_agenda')
    status = models.CharField(max_length=1, db_column='status')
    vl_total = models.DecimalField(max_digits=5, decimal_places=2, db_column='vl_total')
    
    # Relações (Foreign Keys)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente')
    id_forma_pagto = models.ForeignKey(FormaPagto, on_delete=models.CASCADE, db_column='id_forma_pagto')
    id_profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, db_column='id_profissional')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    id_servico = models.ForeignKey(Servico, on_delete=models.CASCADE, db_column='id_servico')

    class Meta:
        managed = False
        db_table = 'agenda'

    def __str__(self):
        return f"Agendamento para {self.id_cliente} em {self.dt_agenda}"