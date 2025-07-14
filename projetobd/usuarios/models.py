from django.db import models

# Modelo para profissionais
from django.db import models

class Profissional(models.Model):
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)

    class Meta:
        db_table = 'profissional'  # Definindo o nome correto da tabela no PostgreSQL

    def __str__(self):
        return self.nome


# Modelo para clientes
class Cliente(models.Model):
    nome = models.CharField(max_length=100)  # Melhorada a nomenclatura para manter consistência
    cpf = models.CharField(max_length=14)
    email = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    especialidade = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
