from django.db import models

class Venda(models.Model):
    dt_venda = models.DateField()
    hr_venda = models.TimeField()
    nome_cliente = models.CharField(max_length=100)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    valor_custo = models.DecimalField(max_digits=10, decimal_places=2)
    vendedor = models.CharField(max_length=30)
    tipo_pagamento = models.CharField(max_length=50)
    tipo_venda = models.CharField(max_length=10)
    qtde_parcelas = models.CharField(max_length=1)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)

class VendaProduto(models.Model):
    id_venda = models.IntegerField()
    cod_produto = models.CharField(max_length=30)
    quantidade = models.IntegerField()

class VendaPagamento(models.Model):
    id_venda = models.IntegerField()
    parcela = models.IntegerField()
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)

class Fornecedor(models.Model):
    nome_fornecedor = models.CharField(max_length=50)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    cidade = models.CharField(max_length=30, blank=True, null=True)
    telefone = models.CharField(max_length=20)
    contato = models.CharField(max_length=50)

class VIEW_VENDAS_PARCELAS(models.Model):
    id = models.IntegerField(primary_key=True)
    dt_venda = models.DateField()
    hr_venda = models.TimeField()
    vendedor = models.CharField(max_length=30)
    nome_vendedor = models.CharField(max_length=100)
    nome_cliente = models.CharField(max_length=100)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    qtde_parcelas = models.IntegerField()
    parcela = models.IntegerField()
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total_pago = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        managed = False
        db_table = 'VIEW_VENDAS_PARCELAS'

class VIEW_FLUXO_CAIXA(models.Model):
    id = models.IntegerField(primary_key=True)
    dt_venda = models.DateField()
    hr_venda = models.TimeField()
    nome_cliente = models.CharField(max_length=100)
    cod_produto = models.CharField(max_length=30)
    des_produto = models.CharField(max_length=100)
    img_produto = models.FileField(upload_to='produtos/produtos.images', blank=True, null=True)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    vendedor = models.CharField(max_length=30)
    nome_vendedor = models.CharField(max_length=100)
    comissao = models.DecimalField(max_digits=3, decimal_places=0)
    valor_comissao = models.DecimalField(max_digits=10, decimal_places=2)
    qtde_parcelas = models.CharField(max_length=1)
    valor_custo = models.DecimalField(max_digits=10, decimal_places=2)
    lucro = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total_venda = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total_pago = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15)
    class Meta:
        managed = False
        db_table = 'VIEW_FLUXO_CAIXA'

class VIEW_VENDAS_PENDENTES(models.Model):
    id = models.IntegerField(primary_key=True)
    dt_venda = models.DateField()
    hr_venda = models.TimeField()
    nome_cliente = models.CharField(max_length=100)
    cod_produto = models.CharField(max_length=30)
    des_produto = models.CharField(max_length=100)
    img_produto = models.FileField(upload_to='produtos/produtos.images', blank=True, null=True)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    vendedor = models.CharField(max_length=30)
    nome_vendedor = models.CharField(max_length=100)
    qtde_parcelas = models.CharField(max_length=1)
    valor_custo = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total_pago = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        managed = False
        db_table = 'VIEW_VENDAS_PENDENTES'
