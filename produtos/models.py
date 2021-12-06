from django.db import models

class Produto(models.Model):
    cod_produto = models.CharField(max_length=20)
    des_produto = models.CharField(max_length=100)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_custo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    colecao = models.CharField(max_length=30, blank=True, null=True)
    qtde_estoque = models.IntegerField()
    dt_insercao = models.DateField(auto_now_add=True)
    cod_categoria = models.IntegerField()
    id_fornecedor = models.IntegerField()
    img_produto = models.FileField(upload_to='produtos/produtos.images', blank=True, null=True)

class Categoria(models.Model):
    des_categoria = models.CharField(max_length=40)

class Maleta(models.Model):
    nome_maleta = models.CharField(max_length=30)
    faixa_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    faixa_final = models.DecimalField(max_digits=10, decimal_places=2)

class ComissaoMaletaVendedor(models.Model):
    id_maleta = models.IntegerField()
    vendedor = models.CharField(max_length=20)
    valor_comissao = models.DecimalField(max_digits=3, decimal_places=0)

class MaletaAberta(models.Model):
    vendedor = models.CharField(max_length=30)
    id_maleta = models.IntegerField()

class MaletaAbertaProdutos(models.Model):
    id_maletaaberta = models.IntegerField()
    cod_produto = models.CharField(max_length=50)
    quantidade = models.IntegerField()
    qtde_vendida = models.IntegerField(blank=True, null=True)

class VIEW_PRODUTOS(models.Model):
    id = models.IntegerField(primary_key=True)
    cod_produto = models.CharField(max_length=20)
    des_produto = models.CharField(max_length=100)
    img_produto = models.FileField(upload_to='produtos/produtos.images', blank=True, null=True)
    id_fornecedor = models.IntegerField()
    nome_fornecedor = models.CharField(max_length=50)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_custo = models.DecimalField(max_digits=10, decimal_places=2)
    colecao = models.CharField(max_length=30, blank=True, null=True)
    qtde_estoque = models.IntegerField()
    dt_insercao = models.DateField(auto_now_add=True)
    cat_id = models.IntegerField()
    des_categoria = models.CharField(max_length=30)
    class Meta:
        managed = False
        db_table = 'VIEW_PRODUTOS'

class VIEW_COMISSAO_MALETA(models.Model):
    id = models.IntegerField(primary_key=True)
    id_maleta = models.CharField(max_length=20)
    nome_maleta = models.CharField(max_length=30)
    vendedor = models.CharField(max_length=20)
    nome_vendedor = models.CharField(max_length=20)
    valor_comissao = models.DecimalField(max_digits=3, decimal_places=0)
    class Meta:
        managed = False
        db_table = 'VIEW_COMISSAO_MALETA'

class VIEW_MALETA_ABERTA(models.Model):
    id = models.IntegerField(primary_key=True)
    id_maleta = models.IntegerField()
    nome_maleta = models.CharField(max_length=30)
    vendedor = models.CharField(max_length=20)
    nome_vendedor = models.CharField(max_length=20)
    cod_produto = models.CharField(max_length=20)
    des_produto = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    qtde_vendida = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'VIEW_MALETA_ABERTA'

class VIEW_MALETA_PRODUTOS(models.Model):
    id = models.IntegerField(primary_key=True)
    vendedor = models.CharField(max_length=20)
    nome_vendedor = models.CharField(max_length=20)
    id_maletaaberta = models.IntegerField()
    nome_maleta = models.CharField(max_length=30)
    cod_produto = models.CharField(max_length=20)
    des_produto = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    qtde_vendida = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'VIEW_MALETA_PRODUTOS'
