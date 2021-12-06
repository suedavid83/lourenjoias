from django.db import models

class Vendedor(models.Model):
    username = models.CharField(max_length=20)
    nome_vendedor = models.CharField(max_length=100)
    cpf_cnpj = models.CharField(max_length=50)
    rg = models.CharField(max_length=20)
    endereco = models.CharField(max_length=200)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20)
    id_maleta = models.IntegerField()
    ref1_empresa = models.CharField(max_length=50)
    ref1_contato = models.CharField(max_length=30)
    ref1_telefone = models.CharField(max_length=20)
    ref2_empresa = models.CharField(max_length=50)
    ref2_contato = models.CharField(max_length=30)
    ref2_telefone = models.CharField(max_length=20)

class Cliente(models.Model):
    nome_cliente = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    bairro = models.CharField(max_length=30)
    cidade = models.CharField(max_length=30, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    cep = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20)
    email = models.CharField(max_length=200)
    whatsapp = models.CharField(max_length=3)

class VIEW_USUARIOS_GRUPO(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    grupo_id = models.IntegerField()
    grupo = models.CharField(max_length=20)
    email = models.CharField(max_length=200)
    class Meta:
        managed = False
        db_table = 'VIEW_USUARIOS_GRUPO'

class VIEW_VENDEDORES(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=20)
    nome_vendedor = models.CharField(max_length=100)
    cpf_cnpj = models.CharField(max_length=50)
    rg = models.CharField(max_length=20)
    endereco = models.CharField(max_length=200)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20)
    id_maleta = models.IntegerField()
    nome_maleta = models.CharField(max_length=30)
    ref1_empresa = models.CharField(max_length=50)
    ref1_contato = models.CharField(max_length=30)
    ref1_telefone = models.CharField(max_length=20)
    ref2_empresa = models.CharField(max_length=50)
    ref2_contato = models.CharField(max_length=30)
    ref2_telefone = models.CharField(max_length=20)
    class Meta:
        managed = False
        db_table = 'VIEW_VENDEDORES'
