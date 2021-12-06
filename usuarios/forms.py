from django import forms
from django.forms import ModelForm
from .models import Cliente, Vendedor

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nome_cliente',
            'endereco',
            'bairro',
            'cidade',
            'estado',
            'cep',
            'telefone',
            'email',
            'whatsapp'
        ]

class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = [
            'username',
            'nome_vendedor',
            'cpf_cnpj',
            'rg',
            'endereco',
            'bairro',
            'cidade',
            'estado',
            'cep',
            'telefone',
            'id_maleta',
            'ref1_empresa',
            'ref1_contato',
            'ref1_telefone',
            'ref2_empresa',
            'ref2_contato',
            'ref2_telefone'
        ]
