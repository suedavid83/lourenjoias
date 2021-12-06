from django.db import models, connection
from .models import VIEW_FLUXO_CAIXA, VendaPagamento, Venda
from produtos.models import VIEW_MALETA_ABERTA

def criarVendaPagamento(self, venda_id, nr_parcela):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO gerenciamento_vendapagamento (id_venda, parcela, valor_pago) VALUES (%s, %s, %s)", [venda_id, nr_parcela, 0])
    return True

def efetuaPagamento(self, venda_id, parcela, valor_pago):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE gerenciamento_vendapagamento SET valor_pago = %s WHERE id_venda = %s AND parcela = %s", [valor_pago, venda_id, parcela])
    return True

def getValorTotalPago(self, venda_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT sum(valor_pago) valor_pago FROM gerenciamento_vendapagamento WHERE id_venda = %s", [venda_id])
        row = dictfetchall(cursor)
        class Meta:
            model = VendaPagamento
            fields = ['valor_pago']
    return row

def atualizarValorTotalPago(self, venda_id, valor_total_pago):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE gerenciamento_venda SET valor_pago = %s WHERE id = %s", [valor_total_pago, venda_id])
    return True

def atualizarEstoqueProduto(self, cod_produto, quantidade):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE produtos_produto SET qtde_estoque = qtde_estoque - %s WHERE cod_produto = %s", [quantidade, cod_produto])
    return True

def filtrarRelatorioMes(self, mes):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM VIEW_FLUXO_CAIXA WHERE substr(dt_venda, 1, 7) = %s", [mes])
        row = dictfetchall(cursor)
        class Meta:
            model = VIEW_FLUXO_CAIXA
            fields = ['id, dt_venda, hr_venda, nome_cliente, cod_produto, des_produto, preco_unitario, quantidade, valor_total, vendedor, nome_vendedor, comissao, valor_comissao, qtde_parcelas, valor_custo, lucro, valor_total_venda, status']
    return row

def getValorTotalMes(self, mes):
    with connection.cursor() as cursor:
        cursor.execute("SELECT sum(valor_total) valor_total FROM VIEW_FLUXO_CAIXA WHERE substr(dt_venda, 1, 7) = %s", [mes])
        row = dictfetchall(cursor)
        class Meta:
            model = VIEW_FLUXO_CAIXA
            fields = ['valor_total']
    return row

def filtrarRelatorioAno(self, ano):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM VIEW_FLUXO_CAIXA WHERE substr(dt_venda, 1, 4) = %s", [ano])
        row = dictfetchall(cursor)
        class Meta:
            model = VIEW_FLUXO_CAIXA
            fields = ['id, dt_venda, hr_venda, nome_cliente, cod_produto, des_produto, preco_unitario, quantidade, valor_total, vendedor, nome_vendedor, comissao, valor_comissao, qtde_parcelas, valor_custo, lucro, valor_total_venda, status']
    return row

def getValorTotalAno(self, ano):
    with connection.cursor() as cursor:
        cursor.execute("SELECT sum(valor_total) valor_total FROM VIEW_FLUXO_CAIXA WHERE substr(dt_venda, 1, 4) = %s", [ano])
        row = dictfetchall(cursor)
        class Meta:
            model = VIEW_FLUXO_CAIXA
            fields = ['valor_total']
    return row

def atualizaQtdeTotalVenda(request, venda_id, valor_total_produto):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE gerenciamento_venda SET valor_total = valor_total + %s WHERE id = %s", [valor_total_produto, venda_id])
    return True

def deletarComissaoVendedor(request, vendedor):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM produtos_comissaomaletavendedor WHERE vendedor = %s", [vendedor])
    return True

def deletarFornecedorProduto(self, forn_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM gerenciamento_fornecedor WHERE id = %s", [forn_id])
    return True

def atualizarQtdeVendidaMaleta(self, id_maletaaberta, cod_produto, quantidade):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE produtos_maletaabertaprodutos SET qtde_vendida = qtde_vendida + %s WHERE id_maletaaberta = %s AND cod_produto = %s", [quantidade, id_maletaaberta, cod_produto])
    return True

def atualizarQtdeProdutoMaleta(request, id_maletaaberta, cod_produto, quantidade):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE produtos_maletaabertaprodutos SET quantidade = quantidade + %s WHERE id_maletaaberta = %s AND cod_produto = %s", [quantidade, id_maletaaberta, cod_produto])
    return True

def deletaPagamento(self, venda_id, parcela):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM gerenciamento_vendapagamento WHERE id = %s AND parcela = %s", [venda_id, parcela])
    return True

def getQtdeParcelasVendas(self, venda_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT qtde_parcelas FROM gerenciamento_venda WHERE id = %s", [venda_id])
        row = dictfetchall(cursor)
        class Meta:
            model = Venda
            fields = ['qtde_parcelas']
    return row

def deletaVenda(self, venda_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM gerenciamento_venda WHERE id = %s", [venda_id])
        cursor.execute("DELETE FROM gerenciamento_vendaproduto WHERE id_venda = %s", [venda_id])
    return True

def atualizarParcelasVenda(self, venda_id):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE gerenciamento_venda SET qtde_parcelas = qtde_parcelas - 1 WHERE id = %s", [venda_id])
    return True

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
