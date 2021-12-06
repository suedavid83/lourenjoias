from django import forms
from django.forms import ModelForm
from .models import Produto, Categoria, Maleta, MaletaAberta, MaletaAbertaProdutos

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'cod_produto',
            'des_produto',
            'preco_unitario',
            'colecao',
            'qtde_estoque',
            'cod_categoria',
            'img_produto',
            'valor_custo'
        ]

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = [
            'des_categoria'
        ]

class MaletaForm(forms.ModelForm):
    class Meta:
        model = Maleta
        fields = [
            'nome_maleta',
            'faixa_inicial',
            'faixa_final'
        ]

class MaletaAbertaForm(forms.ModelForm):
    class Meta:
        model = MaletaAberta
        fields = [
            'vendedor',
            'id_maleta'
        ]

class MaletaAbertaProdutosForm(forms.ModelForm):
    class Meta:
        model = MaletaAbertaProdutos
        fields = [
            'id_maletaaberta',
            'cod_produto',
            'quantidade'
        ]
