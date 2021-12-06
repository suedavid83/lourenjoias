from django.db import models, connection
from .models import MaletaAbertaProdutos

def deletarCat(self, cat_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM produtos_categoria WHERE id = %s", [cat_id])
    return True

def deletaMaleta(self, maleta_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM produtos_maleta WHERE id = %s", [maleta_id])
    return True

def deletaProduto(self, cod_produto):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM produtos_produto WHERE cod_produto = %s", [cod_produto])
    return True

def inserirProdutoMaleta(self, id_maletaaberta, cod_produto, quantidade):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO produtos_maletaabertaprodutos (id_maletaaberta, cod_produto, quantidade, qtde_vendida) VALUES (%s, %s, %s, 0)", [id_maletaaberta, cod_produto, quantidade])
    return True

def atualizarEstoqueProdutoMaleta(self, cod_produto, quantidade):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE produtos_produto SET qtde_estoque = qtde_estoque + %s WHERE cod_produto = %s", [quantidade, cod_produto])
    return True

def deletarMaletaProduto(self, mal_id, cod_produto):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM produtos_maletaabertaprodutos WHERE id_maletaaberta = %s AND cod_produto = %s", [mal_id, cod_produto])
    return True

def deletaMaletaAberta(request, mal_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM produtos_maletaaberta WHERE id = %s", [mal_id])
    return True

def atualizarQtdeEstoqueProdMaleta(self, cod_produto, quantidade):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE produtos_produto SET qtde_estoque = qtde_estoque - %s WHERE cod_produto = %s", [quantidade, cod_produto])
    return True

def getMaletaAberta(self, mal_id, cod_produto):
    with connection.cursor() as cursor:
        cursor.execute("SELECT count(1) cont FROM produtos_maletaabertaprodutos WHERE id_maletaaberta = %s AND cod_produto != %s", [mal_id, cod_produto])
        row = dictfetchall(cursor)
        class Meta:
            model = MaletaAbertaProdutos
            fields = ['cont']
    return row

def deletaVendaProduto(self, venda_id, cod_produto):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM gerenciamento_vendaproduto WHERE id_venda = %s AND cod_produto = %s", [venda_id, cod_produto])
    return True

def deletarVenda(self, venda_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM gerenciamento_venda WHERE id = %s", [venda_id])
    return True

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
