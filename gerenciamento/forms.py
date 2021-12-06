from django import forms
from django.forms import ModelForm
from .models import Venda, VendaProduto, Fornecedor
from produtos.models import ComissaoMaletaVendedor

class ComissaoMaletaVendedorForm(forms.ModelForm):
    class Meta:
        model = ComissaoMaletaVendedor
        fields = [
            'id_maleta',
            'vendedor',
            'valor_comissao'
        ]

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = [
            'dt_venda',
            'nome_cliente',
            'valor_custo',
            'vendedor',
            'tipo_pagamento',
            'tipo_venda',
            'qtde_parcelas',
            'valor_pago',
            'vendedor'
        ]

class VendaProdutoForm(forms.ModelForm):
    class Meta:
        model = VendaProduto
        fields = [
            'id_venda',
            'cod_produto',
            'quantidade'
        ]

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = [
            'nome_fornecedor',
            'endereco',
            'cidade',
            'telefone',
            'contato'
        ]
