from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .forms import ComissaoMaletaVendedorForm, VendaForm, VendaProdutoForm, FornecedorForm
from .models import (VendaPagamento, VIEW_VENDAS_PARCELAS, VIEW_FLUXO_CAIXA, VIEW_VENDAS_PENDENTES,
    Venda, Fornecedor)
from .functions import (criarVendaPagamento, efetuaPagamento, atualizarValorTotalPago,
    atualizarEstoqueProduto, filtrarRelatorioMes, getValorTotalMes, filtrarRelatorioAno,
    getValorTotalAno, atualizaQtdeTotalVenda, getValorTotalPago, deletarComissaoVendedor,
    deletarFornecedorProduto, atualizarQtdeVendidaMaleta, deletaPagamento, getQtdeParcelasVendas,
    atualizarParcelasVenda, deletaVenda)
from usuarios.models import Vendedor, Cliente
from produtos.models import Produto, VIEW_COMISSAO_MALETA, ComissaoMaletaVendedor, Maleta, VIEW_MALETA_ABERTA

def home(request):
    return render(request, "home.html")

def login(request):
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('/louren/')

def definirComissao(request):
    return render(request, "inicioDefinirComissao.html")

def filtrarVendedor(request):
    nome_vendedor = request.POST.get("nome_vendedor")
    vendedores = Vendedor.objects.filter(nome_vendedor__contains=nome_vendedor)
    context = {
        'vendedores': vendedores
    }
    return render(request, "filtrarMaletaVendedor.html", context)

def filtrarMaleta(request):
    username = request.POST.get("vendedor")
    vendedor = Vendedor.objects.get(username=username)
    maleta = Maleta.objects.get(id=vendedor.id_maleta)
    context = {
        'vendedor': vendedor,
        'maleta': maleta
    }
    return render(request, "definirComissao.html", context)

def definicaoComissao(request):
    id_maleta = request.POST.get("id_maleta")
    vendedor = request.POST.get("vendedor")
    valor_comissao = request.POST.get("valor_comissao")
    comissoes = VIEW_COMISSAO_MALETA.objects.filter(id_maleta=id_maleta, vendedor=vendedor)
    if comissoes:
        mensagem = "Comissão já cadastrada para esse Produto e Vendedor!"
        context = {
            'mensagem': mensagem,
            'comissoes': comissoes
        }
        return render(request, "listarComissoes.html", context)
    else:
        form_comissao = ComissaoMaletaVendedorForm(request.POST)
        if form_comissao.is_valid():
            comissao = form_comissao.save(commit=False)
            comissao.id_maleta = id_maleta
            comissao.vendedor = vendedor
            comissao.valor_comissao = valor_comissao
            comissao.save()
            form_comissao = ComissaoMaletaVendedorForm()
            mensagem = "Comissão cadastrada com sucesso!"
            comissoes = VIEW_COMISSAO_MALETA.objects.filter(vendedor=vendedor)
            context = {
                'mensagem': mensagem,
                'comissoes': comissoes
            }
            return render(request, "listarComissoes.html", context)
        else:
            mensagem = "Erro ao cadastrar Comissão"
            context = {
                'mensagem': mensagem,
                'error': form_comissao.errors,
                'tipo': "cadastro_comissao"
            }
            return render(request, "gerenciamentoErrors.html", context)

def listarComissoes(request):
    return render(request, "listarComissoes.html")

def filtrarComissoes(request):
    nome_maleta = request.POST.get("nome_maleta")
    nome_vendedor = request.POST.get("nome_vendedor")
    if nome_maleta and nome_vendedor:
        comissoes = VIEW_COMISSAO_MALETA.objects.filter(nome_maleta__contains=nome_maleta, nome_vendedor__contains=nome_vendedor)
    elif nome_maleta:
        comissoes = VIEW_COMISSAO_MALETA.objects.filter(nome_maleta__contains=nome_maleta)
    elif nome_vendedor:
        comissoes = VIEW_COMISSAO_MALETA.objects.filter(nome_vendedor__contains=nome_vendedor)
    else:
        comissoes = VIEW_COMISSAO_MALETA.objects.all()
    context = {
        'comissoes': comissoes
    }
    return render(request, "listarComissoes.html", context)

def editarComissao(request, com_id):
    comissao = VIEW_COMISSAO_MALETA.objects.get(id=com_id)
    maletas = Maleta.objects.all().exclude(nome_maleta=comissao.nome_maleta)
    vendedores = Vendedor.objects.all().exclude(username=comissao.vendedor)
    context = {
        'comissao': comissao,
        'maletas': maletas,
        'vendedores': vendedores
    }
    return render(request, "editarComissao.html", context)

def alterarComissao(request, com_id):
    id_maleta = request.POST.get("id_maleta")
    vendedor = request.POST.get("vendedor")
    valor_comissao = request.POST.get("valor_comissao")
    comissao = VIEW_COMISSAO_MALETA.objects.get(id=com_id)
    if int(id_maleta) == int(comissao.id_maleta) and str(vendedor) == str(comissao.vendedor):
        comissao = ComissaoMaletaVendedor.objects.get(id=com_id)
        comissao.id_maleta = id_maleta
        comissao.vendedor = vendedor
        comissao.valor_comissao = valor_comissao
        comissao.save()
        mensagem = "Comissão alterada com sucesso!"
        comissoes = VIEW_COMISSAO_MALETA.objects.filter(id=com_id)
        context = {
            'mensagem': mensagem,
            'comissoes': comissoes
        }
        return render(request, "listarComissoes.html", context)
    else:
        comissoes = VIEW_COMISSAO_MALETA.objects.filter(id_maleta=id_maleta, vendedor=vendedor)
        if comissao:
            mensagem = "Comissão já cadastrada para esse Produto e Vendedor!"
            context = {
                'mensagem': mensagem,
                'comissoes': comissoes
            }
            return render(request, "listarComissoes.html", context)
        else:
            comissao = ComissaoMaletaVendedor.objects.get(id=com_id)
            comissao.id_maleta = id_maleta
            comissao.vendedor = vendedor
            comissao.valor_comissao = valor_comissao
            comissao.save()
            mensagem = "Comissão alterada com sucesso!"
            comissoes = VIEW_COMISSAO_MALETA.objects.filter(id=com_id)
            context = {
                'mensagem': mensagem,
                'comissoes': comissoes
            }
            return render(request, "listarComissoes.html", context)

def deletarComissao(request, com_id):
    comissao = ComissaoMaletaVendedor.objects.get(id=com_id)
    username = comissao.vendedor
    vendedor = Venda.objects.filter(vendedor=username)
    if vendedor:
        mensagem = "Não é possível deletar comissão do Vendedor pois já existe Venda registrada em seu nome"
        comissoes = VIEW_COMISSAO_MALETA.objects.filter(vendedor=username)
        context = {
            'mensagem': mensagem,
            'comissoes': comissoes
        }
        return render(request, "listarComissoes.html", context)
    else:
        deletar_comissao = deletarComissaoVendedor(request, username)
        mensagem = "Comissão Vendedor deletada com sucesso"
        comissoes = VIEW_COMISSAO_MALETA.objects.filter(vendedor=username)
        context = {
            'mensagem': mensagem,
            'comissoes': comissoes
        }
        return render(request, "listarComissoes.html", context)

def registrarVenda(request):
    return render(request, "inicioVenda.html")

def filtrarCliente(request):
    nome_cliente = request.POST.get("nome_cliente")
    des_produto = request.POST.get("des_produto")
    if nome_cliente and des_produto:
        clientes = Cliente.objects.filter(nome_cliente__contains=nome_cliente)
        produtos = Produto.objects.filter(des_produto__contains=des_produto)
        vendedores = Vendedor.objects.all()
        context = {
            'clientes': clientes,
            'produtos': produtos,
            'vendedores': vendedores
        }
        return render(request, "registrarVenda.html", context)
    elif nome_cliente:
        clientes = Cliente.objects.filter(nome_cliente__contains=nome_cliente)
        produtos = Produto.objects.all()
        vendedores = Vendedor.objects.all()
        context = {
            'clientes': clientes,
            'produtos': produtos,
            'vendedores': vendedores
        }
        return render(request, "registrarVenda.html", context)
    else:
        mensagem = "Nome do Cliente deve ser informado!"
        context = {
            'mensagem': mensagem
        }
        return render(request, "inicioVenda.html", context)


def efetuarRegistroVenda(request):
    dt_venda = request.POST.get("dt_venda")
    hr_venda = request.POST.get("hr_venda")
    nome_cliente = request.POST.get("nome_cliente")
    cod_produto = request.POST.get("cod_produto")
    quantidade = request.POST.get("quantidade")
    valor_custo = request.POST.get("valor_custo")
    tipo_pagamento = request.POST.get("tipo_pagamento")
    tipo_venda = request.POST.get("tipo_venda")
    qtde_parcelas = request.POST.get("qtde_parcelas")
    vendedor = request.POST.get("vendedor")
    cliente = Cliente.objects.get(id=nome_cliente)
    nome_cliente = cliente.nome_cliente
    produto = Produto.objects.get(cod_produto=cod_produto)
    valor_total = produto.preco_unitario * int(quantidade)
    form_venda = VendaForm(request.POST)
    form_vendaproduto = VendaProdutoForm(request.POST)
    if form_venda.is_valid() and form_vendaproduto.is_valid():
        venda = form_venda.save(commit=False)
        venda.dt_venda = dt_venda
        venda.hr_venda = hr_venda
        venda.nome_cliente = nome_cliente
        venda.valor_total = valor_total
        if valor_custo:
            venda.valor_custo = valor_custo
        else:
            venda.valor_custo = 0
        venda.tipo_pagamento = tipo_pagamento
        venda.tipo_venda = tipo_venda
        venda.qtde_parcelas = qtde_parcelas
        venda.vendedor = vendedor
        venda.valor_pago = 0
        venda.save()
        form_venda = VendaForm()
        i = 1
        while int(i) <= int(qtde_parcelas):
            pagamento = criarVendaPagamento(request, venda.id, i)
            i = int(i) + 1
        venda_produto = form_vendaproduto.save(commit=False)
        venda_produto.id_venda = venda.id
        venda_produto.cod_produto = cod_produto
        venda_produto.quantidade = quantidade
        venda_produto.save()
        form_vendaproduto = VendaProdutoForm()
        atualizar_estoque = atualizarEstoqueProduto(request, cod_produto, quantidade)
        mensagem = "Venda registrada com sucesso!"
        maleta = VIEW_MALETA_ABERTA.objects.filter(vendedor=vendedor, cod_produto=cod_produto)
        if maleta:
            maleta = VIEW_MALETA_ABERTA.objects.get(vendedor=vendedor, cod_produto=cod_produto)
            atualizar_qtde_vendida_maleta = atualizarQtdeVendidaMaleta(request, maleta.id, cod_produto, quantidade)
        vendas = VIEW_FLUXO_CAIXA.objects.filter(id=venda.id)
        context = {
            'mensagem': mensagem,
            'vendas': vendas
        }
        return render(request, "finalizarVenda.html", context)
    else:
        mensagem = "Erro ao registrar venda"
        context = {
            'mensagem': mensagem,
            'error': str(form_venda.errors) + str(form_vendaproduto.errors),
            'tipo': "registrar_venda"
        }
        return render(request, "gerenciamentoErrors.html", context)

def incluirProdutoVenda(request):
    return render(request, "finalizarVenda.html")

def filtrarClienteVenda(request):
    nome_cliente = request.POST.get("nome_cliente")
    vendas = VIEW_VENDAS_PENDENTES.objects.filter(nome_cliente__contains=nome_cliente)
    context = {
        'vendas': vendas
    }
    return render(request, "finalizarVenda.html", context)

def adicionarProduto(request, venda_id):
    context = {
        'venda_id': venda_id
    }
    return render(request, "adicionarProdutoVenda.html", context)

def adicionarProdutoVenda(request):
    venda_id = request.POST.get("id_venda")
    cod_produto = request.POST.get("cod_produto")
    quantidade = request.POST.get("quantidade")
    form_vendaproduto = VendaProdutoForm(request.POST)
    if form_vendaproduto.is_valid():
        venda = form_vendaproduto.save(commit=False)
        venda.id_venda = venda_id
        venda.cod_produto = cod_produto
        venda.quantidade = quantidade
        venda.save()
        form_vendaproduto = VendaProdutoForm()
        produto = Produto.objects.get(cod_produto=cod_produto)
        valor_total_produto = (produto.preco_unitario * int(quantidade))
        atualizar_estoque = atualizarEstoqueProduto(request, cod_produto, quantidade)
        atualizar_qtde_total_venda = atualizaQtdeTotalVenda(request, venda_id, valor_total_produto)
        mensagem = "Produto incluído na Venda com Sucesso!"
        vendas = VIEW_FLUXO_CAIXA.objects.filter(id=venda_id)
        context = {
            'mensagem': mensagem,
            'vendas': vendas
        }
        return render(request, "finalizarVenda.html", context)
    else:
        mensagem = "Erro ao adicionar produto a venda"
        context = {
            'mensagem': mensagem,
            'error': form_vendaproduto.errors,
            'tipo': 'adicionar_produto'
        }
        return render(request, "gerenciamentoErrors.html", context)

def filtrarProduto(request, venda_id):
    des_produto = request.POST.get("des_produto")
    produtos = Produto.objects.filter(des_produto__contains=des_produto)
    context = {
        'produtos': produtos,
        'venda_id': venda_id
    }
    return render(request, "adicionarProdutoVenda.html", context)


def registrarPagamento(request):
    return render(request, "registrarPagamento.html")

def filtrarClienteProduto(request):
    nome_cliente = request.POST.get("nome_cliente")
    des_produto = request.POST.get("des_produto")
    if nome_cliente and des_produto:
        vendas = VIEW_VENDAS_PARCELAS.objects.filter(nome_cliente__contains=nome_cliente, des_produto__contains=des_produto)
        context = {
            'vendas': vendas
        }
        return render(request, "registrarPagamento.html", context)
    elif nome_cliente:
        vendas = VIEW_VENDAS_PARCELAS.objects.filter(nome_cliente__contains=nome_cliente)
        context = {
            'vendas': vendas
        }
        return render(request, "registrarPagamento.html", context)
    else:
        mensagem = "Nome do Cliente deve ser informado!"
        context = {
            'mensagem': mensagem
        }
        return render(request, "registrarPagamento.html", context)

def efetuarPagamento(request, venda_id, parcela):
    venda = VIEW_VENDAS_PARCELAS.objects.get(id=venda_id, parcela=parcela)
    context = {
        'venda': venda
    }
    return render(request, "efetuarRegistroPagamento.html", context)

def efetivarPagamento(request):
    venda_id = request.POST.get("id_venda")
    parcela = request.POST.get("parcela")
    valor_pago = request.POST.get("valor_pago")
    valor_pago = valor_pago.replace(',','.')
    efetua_pagamento = efetuaPagamento(request, venda_id, parcela, valor_pago)
    valor_total_pago = getValorTotalPago(request, venda_id)
    valor_total_pago = valor_total_pago[0]['valor_pago']
    atualiza_valor_pago = atualizarValorTotalPago(request, venda_id, valor_total_pago)
    mensagem = "Pagamento registrado com sucesso!"
    vendas = VIEW_VENDAS_PARCELAS.objects.filter(id=venda_id)
    context = {
        'mensagem': mensagem,
        'vendas': vendas
    }
    return render(request, "registrarPagamento.html", context)

def deletarPagamento(request, venda_id, parcela):
    pagamento = VIEW_VENDAS_PARCELAS.objects.get(id=venda_id, parcela=parcela)
    if pagamento.valor_pago > 0:
        mensagem = "Não é possível excluir pagamento pois o mesmo já foi efetuado!"
        vendas = VIEW_VENDAS_PARCELAS.objects.filter(id=venda_id, parcela=parcela)
        context = {
            'mensagem': mensagem,
            'vendas': vendas
        }
        return render(request, "registrarPagamento.html", context)
    else:
        deletar_pagamento = deletaPagamento(request, venda_id, parcela)
        qtde_parcelas_venda = getQtdeParcelasVendas(request, venda_id)
        qtde_parcelas = qtde_parcelas_venda[0]['qtde_parcelas']
        if int(qtde_parcelas) == int(1):
            deletar_venda = deletaVenda(request, venda_id)
            mensagem = "Pagamento deletado com sucesso. Como a venda só havia uma parcela, a mesma foi excluída também!"
        else:
            atualizar_parcelas_venda = atualizarParcelasVenda(request, venda_id)
            mensagem = "Pagamento deletado com sucesso!"
        vendas = VIEW_VENDAS_PARCELAS.objects.filter(id=venda_id)
        context = {
            'mensagem': mensagem,
            'vendas': vendas
        }
        return render(request, "registrarPagamento.html", context)

def listarClienteProdutoAdmin(request):
    nome_cliente = request.POST.get("nome_cliente")
    des_produto = request.POST.get("des_produto")
    if nome_cliente and des_produto:
        vendas = VIEW_FLUXO_CAIXA.objects.filter(nome_cliente__contains=nome_cliente, des_produto__contains=des_produto)
        context = {
            'vendas': vendas
        }
        return render(request, "relatorioVendasAdmin.html", context)
    elif nome_cliente:
        vendas = VIEW_FLUXO_CAIXA.objects.filter(nome_cliente__contains=nome_cliente)
        context = {
            'vendas': vendas
        }
        return render(request, "relatorioVendasAdmin.html", context)
    else:
        mensagem = "Nome do Cliente deve ser informado!"
        context = {
            'mensagem': mensagem
        }
        return render(request, "relatorioVendasAdmin.html", context)

def relatorioFluxoCaixaAdmin(request):
    vendas = VIEW_FLUXO_CAIXA.objects.all()
    context = {
        'vendas': vendas
    }
    return render(request, "relatorioVendasAdmin.html")

def relatorioFluxoCaixaVendedor(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        usuario = User.objects.get(id=user_id)
        username = usuario.username
        vendas = VIEW_FLUXO_CAIXA.objects.filter(vendedor=username)
        context = {
            'vendas': vendas
        }
        return render(request, "relatorioVendasVendedor.html")
    else:
        mensagem = "Usuário não logado, não é possível exibir relatório"
        context = {
            'mensagem': mensagem
        }
        return render(request, "relatorioVendasVendedor.html")

def listarClienteProduto(request):
    nome_cliente = request.POST.get("nome_cliente")
    des_produto = request.POST.get("des_produto")
    mensagem = ""
    if request.user.is_authenticated:
        user_id = request.user.id
        usuario = User.objects.get(id=user_id)
        username = usuario.username
        if nome_cliente and des_produto:
            vendas = VIEW_FLUXO_CAIXA.objects.filter(nome_cliente__contains=nome_cliente, des_produto__contains=des_produto, vendedor=username)
            if not vendas:
                mensagem = "Nenhuma venda encontrada para esse Cliente e Vendedor"
            context = {
                'vendas': vendas,
                'mensagem': mensagem
            }
            return render(request, "relatorioVendasVendedor.html", context)
        elif nome_cliente:
            vendas = VIEW_FLUXO_CAIXA.objects.filter(nome_cliente__contains=nome_cliente, vendedor=username)
            if not vendas:
                mensagem = "Nenhuma venda encontrada para esse Cliente e Vendedor"
            context = {
                'vendas': vendas,
                'mensagem': mensagem
            }
            return render(request, "relatorioVendasVendedor.html", context)
        else:
            mensagem = "Nome do Cliente deve ser informado!"
            context = {
                'mensagem': mensagem
            }
            return render(request, "relatorioVendasVendedor.html", context)
    else:
        mensagem = "Usuário não logado, não é possível exibir relatório"
        context = {
            'mensagem': mensagem
        }
        return render(request, "relatorioVendasVendedor.html")

def relatorioFluxoCaixaMensal(request):
    return render(request, "relatorioVendasMensal.html")

def filtrarMes(request):
    mes = request.POST.get("mes")
    vendas = filtrarRelatorioMes(request, mes)
    valor_total_mes = getValorTotalMes(request, mes)
    valor_total_mes = valor_total_mes[0]['valor_total']
    context = {
        'vendas': vendas,
        'valor_total_mes': valor_total_mes
    }
    return render(request, "relatorioVendasMensal.html", context)

def relatorioFluxoCaixaAnual(request):
    return render(request, "relatorioVendasAnual.html")

def filtrarAno(request):
    ano = request.POST.get("ano")
    ano = str(ano)
    vendas = filtrarRelatorioAno(request, ano)
    valor_total_ano = getValorTotalAno(request, ano)
    valor_total_ano = valor_total_ano[0]['valor_total']
    context = {
        'vendas': vendas,
        'valor_total_ano': valor_total_ano
    }
    return render(request, "relatorioVendasAnual.html", context)

def listarFornecedores(request):
    return render(request, "listarFornecedores.html")

def cadastrarFornecedor(request):
    return render(request, "cadastrarFornecedor.html")

def efetuarCadastroFornecedor(request):
    nome_fornecedor = request.POST.get("nome_fornecedor")
    endereco = request.POST.get("endereco")
    cidade = request.POST.get("cidade")
    telefone = request.POST.get("telefone")
    contato = request.POST.get("contato")
    form_fornecedor = FornecedorForm(request.POST)
    if form_fornecedor.is_valid():
        fornecedor = form_fornecedor.save(commit=False)
        fornecedor.nome_fornecedor = nome_fornecedor
        fornecedor.endereco = endereco
        fornecedor.cidade = cidade
        fornecedor.telefone = telefone
        fornecedor.contato = contato
        fornecedor.save()
        form_fornecedor = FornecedorForm()
        mensagem = "Fornecedor cadastrado com sucesso"
        fornecedores = Fornecedor.objects.filter(id=fornecedor.id)
        context = {
            'mensagem': mensagem,
            'fornecedores': fornecedores
        }
        return render(request, "listarFornecedores.html", context)
    else:
        mensagem = "Erro ao cadastrar Fornecedor"
        context = {
            'mensagem': mensagem,
            'error': form_fornecedor.errors,
            'tipo': "cadastrar_fornecedor"
        }
        return render(request, "gerenciamentoErrors.html", context)

def filtrarFornecedor(request):
    nome_fornecedor = request.POST.get("nome_fornecedor")
    fornecedores = Fornecedor.objects.filter(nome_fornecedor__contains=nome_fornecedor)
    context = {
        'fornecedores': fornecedores
    }
    return render(request, "listarFornecedores.html", context)

def editarFornecedor(request, forn_id):
    fornecedor = Fornecedor.objects.get(id=forn_id)
    context = {
        'fornecedor': fornecedor
    }
    return render(request, "editarFornecedor.html", context)

def alterarFornecedor(request, forn_id):
    nome_fornecedor = request.POST.get("nome_fornecedor")
    endereco = request.POST.get("endereco")
    cidade = request.POST.get("cidade")
    telefone = request.POST.get("telefone")
    contato = request.POST.get("contato")
    fornecedor = Fornecedor.objects.get(id=forn_id)
    if nome_fornecedor != fornecedor.nome_fornecedor:
        fornecedor = Fornecedor.objects.filter(nome_fornecedor=nome_fornecedor)
        if fornecedor:
            mensagem = "Fornecedor já cadastrado"
            fornecedores = Fornecedor.objects.get(id=forn_id)
            context = {
                'fornecedores': fornecedores,
                'mensagem': mensagem
            }
            return render(request, "listarFornecedores.html", context)
        else:
            fornecedor.nome_fornecedor = nome_fornecedor
            fornecedor.endereco = endereco
            fornecedor.cidade = cidade
            fornecedor.telefone = telefone
            fornecedor.contato = contato
            fornecedor.save()
            mensagem = "Fornecedor alterado com sucesso!"
            fornecedores = Fornecedor.objects.get(id=forn_id)
            context = {
                'fornecedores': fornecedores,
                'mensagem': mensagem
            }
            return render(request, "listarFornecedores.html", context)
    else:
        fornecedor.nome_fornecedor = nome_fornecedor
        fornecedor.endereco = endereco
        fornecedor.cidade = cidade
        fornecedor.telefone = telefone
        fornecedor.contato = contato
        fornecedor.save()
        mensagem = "Fornecedor alterado com sucesso!"
        fornecedores = Fornecedor.objects.filter(id=forn_id)
        context = {
            'fornecedores': fornecedores,
            'mensagem': mensagem
        }
        return render(request, "listarFornecedores.html", context)

def deletarFornecedor(request, forn_id):
    produto = Produto.objects.filter(id_fornecedor=forn_id)
    if produto:
        mensagem = "Fornecedor não pode ser deletado pois está associado a um ou mais produto(s)"
        fornecedores = Fornecedor.objects.filter(id=forn_id)
        context = {
            'mensagem': mensagem,
            'fornecedores': fornecedores
        }
        return render(request, "listarFornecedores.html", context)
    else:
        deletar_fornecedor = deletarFornecedorProduto(request, forn_id)
        mensagem = "Fornecedor deletado com sucesso!"
        fornecedores = Fornecedor.objects.all()
        context = {
            'mensagem': mensagem,
            'fornecedores': fornecedores
        }
        return render(request, "listarFornecedores.html", context)

def inicioVendaVendedor(request):
    return render(request, "inicioVendaVendedor.html")

def listarClienteVendedor(request):
    nome_cliente = request.POST.get("nome_cliente")
    if request.user.is_authenticated:
        user_id = request.user.id
        usuario = User.objects.get(id=user_id)
        username = usuario.username
        vendedor = Vendedor.objects.get(username=username)
        if nome_cliente:
            clientes = Cliente.objects.filter(nome_cliente__contains=nome_cliente)
            produtos = VIEW_MALETA_ABERTA.objects.filter(vendedor=username)
            if not produtos:
                mensagem = "Não existe Maleta aberta para esse vendedor, não é possível registrar Venda"
                context = {
                    'mensagem': mensagem,
                    'error': "Maleta não aberta!",
                    'tipo': "maleta_nao_aberta"
                }
                return render(request, "gerenciamentoErrors.html", context)
            else:
                context = {
                    'clientes': clientes,
                    'produtos': produtos,
                    'vendedor': vendedor
                }
                return render(request, "registrarVendaVendedor.html", context)
        else:
            mensagem = "Nome do Cliente deve ser informado!"
            context = {
                'mensagem': mensagem
            }
            return render(request, "inicioVendaVendedor.html", context)
    else:
        mensagem = "Usuário não logado, não é possível inserir venda"
        context = {
            'mensagem': mensagem,
            'error': "Usuário não logado!",
            'tipo': "maleta_nao_aberta"
        }
        return render(request, "registrarVendaVendedor.html", context)

def efetivarVendaVendedor(request):
    dt_venda = request.POST.get("dt_venda")
    hr_venda = request.POST.get("hr_venda")
    nome_cliente = request.POST.get("nome_cliente")
    cod_produto = request.POST.get("cod_produto")
    quantidade = request.POST.get("quantidade")
    tipo_pagamento = request.POST.get("tipo_pagamento")
    tipo_venda = request.POST.get("tipo_venda")
    qtde_parcelas = request.POST.get("qtde_parcelas")
    vendedor = request.POST.get("vendedor")
    cliente = Cliente.objects.get(id=nome_cliente)
    nome_cliente = cliente.nome_cliente
    produto = Produto.objects.get(cod_produto=cod_produto)
    valor_custo = produto.valor_custo * int(quantidade)
    valor_total = produto.preco_unitario * int(quantidade)
    maleta = VIEW_MALETA_ABERTA.objects.get(vendedor=vendedor, cod_produto=cod_produto)
    if int(quantidade) > int(maleta.quantidade) or maleta.quantidade == maleta.qtde_vendida:
        maletas = VIEW_MALETA_ABERTA.objects.filter(vendedor=vendedor, cod_produto=cod_produto)
        mensagem = "Quantidade registrada para esse produto é maior que a quantidade informada para venda"
        context = {
            'mensagem': mensagem,
            'maletas': maletas
        }
        return render(request, "listarMaletaAberta.html", context)
    else:
        form_venda = VendaForm(request.POST)
        form_vendaproduto = VendaProdutoForm(request.POST)
        if form_venda.is_valid() and form_vendaproduto.is_valid():
            venda = form_venda.save(commit=False)
            venda.dt_venda = dt_venda
            venda.hr_venda = hr_venda
            venda.nome_cliente = nome_cliente
            venda.valor_total = valor_total
            venda.valor_custo = valor_custo
            venda.tipo_pagamento = tipo_pagamento
            venda.tipo_venda = tipo_venda
            venda.qtde_parcelas = qtde_parcelas
            venda.vendedor = vendedor
            venda.valor_pago = 0
            venda.save()
            form_venda = VendaForm()
            i = 1
            while int(i) <= int(qtde_parcelas):
                pagamento = criarVendaPagamento(request, venda.id, i)
                i = int(i) + 1
            venda_produto = form_vendaproduto.save(commit=False)
            venda_produto.id_venda = venda.id
            venda_produto.cod_produto = cod_produto
            venda_produto.quantidade = quantidade
            venda_produto.save()
            form_vendaproduto = VendaProdutoForm()
            atualizar_estoque = atualizarEstoqueProduto(request, cod_produto, quantidade)
            maleta_aberta = VIEW_MALETA_ABERTA.objects.get(vendedor=vendedor, cod_produto=cod_produto)
            id_maletaaberta = maleta_aberta.id
            if int(maleta_aberta.quantidade) <= int(quantidade) and maleta_aberta.quantidade == maleta_aberta.qtde_vendida:
                mensagem = "Não é possível realizar venda pois não existe mais quantidade disponível na maleta para esse produto!"
                maletas = VIEW_MALETA_ABERTA.objects.filter(vendedor=vendedor, cod_produto=cod_produto)
                context = {
                    'mensagem': mensagem,
                    'maletas': maletas
                }
                return render(request, "listarMaletaAberta.html", context)
            else:
                atualizar_qtde_vendida_maleta = atualizarQtdeVendidaMaleta(request, id_maletaaberta, cod_produto, quantidade)
                mensagem = "Venda registrada com sucesso!"
                vendas = VIEW_FLUXO_CAIXA.objects.filter(id=venda.id)
                context = {
                    'mensagem': mensagem,
                    'vendas': vendas
                }
                return render(request, "finalizarVendaVendedor.html", context)
        else:
            mensagem = "Erro ao registrar venda"
            context = {
                'mensagem': mensagem,
                'error': str(form_venda.errors) + str(form_vendaproduto.errors),
                'tipo': "registrar_venda"
            }
            return render(request, "gerenciamentoErrors.html", context)

def filtrarClienteVendedor(request):
    nome_cliente = request.POST.get("nome_cliente")
    vendas = VIEW_VENDAS_PENDENTES.objects.filter(nome_cliente__contains=nome_cliente)
    context = {
        'vendas': vendas
    }
    return render(request, "finalizarVendaVendedor.html", context)

def incluirProdutoVendaVendedor(request):
    return render(request, "finalizarVendaVendedor.html")

def adicionarProdutoVendedor(request, venda_id, cod_produto):
    if request.user.is_authenticated:
        user_id = request.user.id
        usuario = User.objects.get(id=user_id)
        vendedor = usuario.username
        produtos = VIEW_MALETA_ABERTA.objects.filter(vendedor=vendedor).exclude(cod_produto=cod_produto)
        context = {
            'venda_id': venda_id,
            'vendedor': vendedor,
            'produtos': produtos
        }
        return render(request, "adicionarProdutoVendaVendedor.html", context)
    else:
        mensagem = "Usuário não logado, não é possível adicionar produto"
        context = {
            'mensagem': mensagem,
            'error': "Usuário não logado!",
            'tipo': "adicionar_produto_vendedor"
        }
        return render(request, "gerenciamentoErrors.html", context)

def adicionarProdutoVendaVendedor(request, venda_id):
    venda_id = request.POST.get("id_venda")
    cod_produto = request.POST.get("cod_produto")
    quantidade = request.POST.get("quantidade")
    vendedor = request.POST.get("vendedor")
    maleta_aberta = VIEW_MALETA_ABERTA.objects.filter(vendedor=vendedor, cod_produto=cod_produto)
    if not maleta_aberta:
        mensagem = "Não é possível adicionar produto a venda pois o mesmo não consta na Maleta Aberta para esse Vendedor"
        context = {
            'mensagem': mensagem
        }
        return render(request, "finalizarVendaVendedor.html", context)
    else:
        if int(quantidade) > int(maleta_aberta.quantidade):
            mensagem = "Não é possível registrar venda para essa quantidade de produto pois ela é maior do que consta na Maleta!"
            maletas = VIEW_MALETA_ABERTA.objects.filter(vendedor=vendedor, cod_produto=cod_produto)
            context = {
                'mensagem': mensagem,
                'maletas': maletas
            }
            return render(request, "listarMaletaAberta.html", context)
        else:
            form_vendaproduto = VendaProdutoForm(request.POST)
            if form_vendaproduto.is_valid():
                venda = form_vendaproduto.save(commit=False)
                venda.id_venda = venda_id
                venda.cod_produto = cod_produto
                venda.quantidade = quantidade
                venda.save()
                form_vendaproduto = VendaProdutoForm()
                produto = Produto.objects.get(cod_produto=cod_produto)
                valor_total_produto = (produto.preco_unitario * int(quantidade))
                atualizar_estoque = atualizarEstoqueProduto(request, cod_produto, quantidade)
                atualizar_qtde_total_venda = atualizaQtdeTotalVenda(request, venda_id, valor_total_produto)
                maleta_aberta = VIEW_MALETA_ABERTA.objects.get(vendedor=vendedor)
                id_maletaaberta = maleta_aberta.id
                atualizar_qtde_vendida_maleta = atualizarQtdeVendidaMaleta(request, id_maletaaberta, cod_produto, quantidade)
                mensagem = "Produto incluído na Venda com Sucesso!"
                vendas = VIEW_FLUXO_CAIXA.objects.filter(id=venda_id)
                context = {
                    'mensagem': mensagem,
                    'vendas': vendas
                }
                return render(request, "finalizarVendaVendedor.html", context)
            else:
                mensagem = "Erro ao adicionar produto a venda"
                context = {
                    'mensagem': mensagem,
                    'error': form_vendaproduto.errors,
                    'tipo': 'adicionar_produto'
                }
                return render(request, "gerenciamentoErrors.html", context)

def filtrarProdutoVendedor(request, venda_id):
    des_produto = request.POST.get("des_produto")
    produtos = Produto.objects.filter(des_produto__contains=des_produto)
    context = {
        'produtos': produtos,
        'venda_id': venda_id
    }
    return render(request, "adicionarProdutoVendaVendedor.html", context)
