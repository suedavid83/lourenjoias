from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from decimal import Decimal
from .models import (Categoria, VIEW_PRODUTOS, Produto, Maleta, VIEW_MALETA_ABERTA,
    VIEW_MALETA_PRODUTOS, MaletaAbertaProdutos)
from .forms import ProdutoForm, CategoriaForm, MaletaForm, MaletaAbertaForm, MaletaAbertaProdutosForm
from .functions import (deletarCat, deletaMaleta, deletaProduto, inserirProdutoMaleta,
    atualizarEstoqueProdutoMaleta, deletarMaletaProduto, atualizarQtdeEstoqueProdMaleta,
    deletaMaletaAberta, getMaletaAberta, deletaVendaProduto, deletarVenda)
from usuarios.models import Vendedor, VIEW_VENDEDORES
from gerenciamento.models import Fornecedor, VendaProduto, VendaProduto, VIEW_FLUXO_CAIXA

def cadastrarProduto(request):
    categorias = Categoria.objects.all()
    fornecedores = Fornecedor.objects.all()
    context = {
        'categorias': categorias,
        'fornecedores': fornecedores
    }
    return render(request, "cadastrarProduto.html", context)

def cadastrarProdutoVendedor(request):
    categorias = Categoria.objects.all()
    fornecedores = Fornecedor.objects.all()
    context = {
        'categorias': categorias,
        'fornecedores': fornecedores
    }
    return render(request, "cadastrarProdutoVendedor.html", context)

def efetuarCadastroProduto(request):
    cod_produto = request.POST.get("cod_produto")
    des_produto = request.POST.get("des_produto")
    preco_unitario = request.POST.get("preco_unitario")
    valor_custo = request.POST.get("valor_custo")
    preco_unitario = preco_unitario.replace(',','.')
    if valor_custo:
        valor_custo = valor_custo.replace(',','.')
    colecao = request.POST.get("colecao")
    qtde_estoque = request.POST.get("qtde_estoque")
    cod_categoria = request.POST.get("cod_categoria")
    id_fornecedor = request.POST.get("id_fornecedor")
    img_produto = request.FILES.get("img_produto")
    prod = Produto.objects.filter(cod_produto=cod_produto)
    if prod:
        mensagem = "Código de Produto já cadastrado!"
        context = {
            'mensagem': mensagem,
            'error': "Código já existente",
            'tipo': "cadastrar_produto"
        }
        return render(request, "produtosErros.html", context)
    else:
        form_produto = ProdutoForm(request.POST, request.FILES)
        if form_produto.is_valid():
            produto = form_produto.save(commit=False)
            produto.cod_produto = cod_produto
            produto.des_produto = des_produto
            produto.preco_unitario = preco_unitario
            if valor_custo:
                produto.valor_custo = valor_custo
            else:
                produto.valor_custo = 0
            produto.colecao = colecao
            produto.qtde_estoque = qtde_estoque
            produto.cod_categoria = cod_categoria
            produto.id_fornecedor = id_fornecedor
            if img_produto:
                produto.img_produto = img_produto
            produto.save()
            form_produto = ProdutoForm()
            mensagem = "Produto Cadastrado com Sucesso"
            produtos = VIEW_PRODUTOS.objects.filter(id=produto.id)
            context = {
                'mensagem': mensagem,
                'produtos': produtos
            }
            return render(request, "listarProdutos.html", context)
        else:
            mensagem = "Erro ao cadastrar Produto"
            context = {
                'mensagem': mensagem,
                'error': form_produto.errors,
                'tipo': "cadastrar_produto"
            }
            return render(request, "produtosErros.html", context)

def cadastrarCategoria(request):
    return render(request, "cadastrarCategoria.html")

def efetuarCadastroCategoria(request):
    des_categoria = request.POST.get("des_categoria")
    cat = Categoria.objects.filter(des_categoria=des_categoria)
    if cat:
        mensagem = "Categoria já cadastrada"
        context = {
            'mensagem': mensagem,
            'error': "Categoria duplicada!",
            'tipo': "cadastrar_categoria"
        }
        return render(request, "produtosErros.html", context)
    else:
        form_categoria = CategoriaForm(request.POST)
        if form_categoria.is_valid():
            categoria = form_categoria.save(commit=False)
            categoria.des_categoria = des_categoria
            categoria.save()
            form_categoria = CategoriaForm()
            mensagem = "Categoria cadastrada com sucesso!"
            categorias = Categoria.objects.filter(id=categoria.id)
            context = {
                'mensagem': mensagem,
                'categorias': categorias
            }
            return render(request, "listarCategorias.html", context)
        else:
            mensagem = "Erro ao cadastrar Categoria"
            context = {
                'mensagem': mensagem,
                'error': form_categoria.errors,
                'tipo': "cadastrar_categoria"
            }
            return render(request, "produtosErros.html", context)

def listarProdutos(request):
    return render(request, "listarProdutos.html")

def listarProduto(request):
    cod_produto = request.POST.get("cod_produto")
    des_produto = request.POST.get("des_produto")
    if cod_produto:
        produtos = VIEW_PRODUTOS.objects.filter(cod_produto__contains=cod_produto)
    elif des_produto:
        produtos = VIEW_PRODUTOS.objects.filter(des_produto__contains=des_produto)
    else:
        produtos = VIEW_PRODUTOS.objects.all()
    context = {
        'produtos': produtos
    }
    return render(request, "listarProdutos.html", context)

def editarProduto(request, prod_id):
    produto = VIEW_PRODUTOS.objects.get(id=prod_id)
    categorias = Categoria.objects.all().exclude(id=produto.cat_id)
    fornecedores = Fornecedor.objects.all().exclude(id=produto.id_fornecedor)
    if request.user.is_authenticated:
        user_id = request.user.id
        grupo = Group.objects.get(user=user_id)
    context = {
        'produto': produto,
        'categorias': categorias,
        'fornecedores': fornecedores
    }
    if grupo == 'admin':
        return render(request, "editarProduto.html", context)
    else:
        return render(request, "editarProdutoVendedor.html", context)

def alterarProduto(request, prod_id):
    cod_produto = request.POST.get("cod_produto")
    des_produto = request.POST.get("des_produto")
    preco_unitario = request.POST.get("preco_unitario")
    valor_custo = request.POST.get("valor_custo")
    preco_unitario = preco_unitario.replace(',','.')
    if valor_custo:
        valor_custo = valor_custo.replace(',','.')
    colecao = request.POST.get("colecao")
    qtde_estoque = request.POST.get("qtde_estoque")
    cod_categoria = request.POST.get("cod_categoria")
    id_fornecedor = request.POST.get("id_fornecedor")
    img_produto = request.FILES.get("img_produto")
    produto = Produto.objects.get(id=prod_id)
    if cod_produto != produto.cod_produto:
        produto = Produto.objects.filter(cod_produto=cod_produto)
        if produto:
            produto = VIEW_PRODUTOS.objects.get(id=prod_id)
            mensagem = "Código de produto já cadastrado!"
            if request.user.is_authenticated:
                user_id = request.user.id
                grupo = Group.objects.get(user=user_id)
            context = {
                'mensagem': mensagem,
                'produto': produto
            }
            if grupo == 'admin':
                return render(request, "editarProduto.html", context)
            else:
                return render(request, "editarProdutoVendedor.html", context)
    else:
        produto.cod_produto = cod_produto
        produto.des_produto = des_produto
        produto.preco_unitario = preco_unitario
        if valor_custo:
            produto.valor_custo = valor_custo
        produto.colecao = colecao
        produto.qtde_estoque = qtde_estoque
        produto.cod_categoria = cod_categoria
        produto.id_fornecedor = id_fornecedor
        if img_produto:
            produto.img_produto = img_produto
        produto.save()
        produtos = VIEW_PRODUTOS.objects.filter(id=prod_id)
        mensagem = "Produto alterado com sucesso!"
        context = {
            'mensagem': mensagem,
            'produtos': produtos
        }
        return render(request, "listarProdutos.html", context)

def deletarProduto(request, cod_produto):
    produto = VendaProduto.objects.filter(cod_produto=cod_produto)
    if produto:
        mensagem = "Não é possível deletar produto pois existe uma ou mais vendas associadas a ele!"
        produtos = VIEW_PRODUTOS.objects.filter(cod_produto=cod_produto)
        context = {
            'mensagem': mensagem,
            'produtos': produtos
        }
        return render(request, "listarProdutos.html", context)
    else:
        deletar_produto = deletaProduto(request, cod_produto)
        mensagem = "Produto excluído com sucesso!"
        produtos = VIEW_PRODUTOS.objects.all()
        context = {
            'mensagem': mensagem,
            'produtos': produtos
        }
        return render(request, "listarProdutos.html", context)

def listarCategorias(request):
    return render(request, "listarCategorias.html")

def listarCategoria(request):
    des_categoria = request.POST.get("des_categoria")
    categorias = Categoria.objects.filter(des_categoria__contains=des_categoria)
    context = {
        'categorias': categorias
    }
    return render(request, "listarCategorias.html", context)

def editarCategoria(request, cat_id):
    categoria = Categoria.objects.get(id=cat_id)
    context = {
        'categoria': categoria
    }
    return render(request, "editarCategoria.html", context)

def alterarCategoria(request, cat_id):
    des_categoria = request.POST.get("des_categoria")
    categoria = Categoria.objects.get(id=cat_id)
    if des_categoria != categoria.des_categoria:
        categoria = Categoria.objects.filter(des_categoria=des_categoria)
        if categoria:
            mensagem = "Categoria já cadastrada!"
            categorias = Categoria.objects.filter(id=cat_id)
            context = {
                'mensagem': mensagem,
                'categorias': categorias
            }
            return render(request, "editarCategoria.html", context)
    else:
        categoria.des_categoria = des_categoria
        categoria.save()
        categorias = Categoria.objects.filter(id=cat_id)
        mensagem = "Categoria alterada com sucesso!"
        context = {
            'mensagem': mensagem,
            'categorias': categorias
        }
        return render(request, "listarCategorias.html", context)

def deletarCategoria(request, cat_id):
    produto = Produto.objects.filter(cod_categoria=cat_id)
    if produto:
        mensagem = "Não é possível excluir Categoria pois existe produto associado a ela!"
        categorias = Categoria.objects.filter(id=cat_id)
        context = {
            'mensagem': mensagem,
            'categorias': categorias
        }
        return render(request, "listarCategorias.html", context)
    else:
        deletar_categoria = deletarCat(request, cat_id)
        mensagem = "Categoria deletada com sucesso!"
        context = {
            'mensagem': mensagem
        }
        return render(request, "listarCategorias.html", context)

def cadastrarMaleta(request):
    return render(request, "cadastrarMaleta.html")

def efetuarCadastroMaleta(request):
    nome_maleta = request.POST.get("nome_maleta")
    faixa_inicial = request.POST.get("faixa_inicial")
    faixa_final = request.POST.get("faixa_final")
    faixa_inicial = faixa_inicial.replace(',','.')
    faixa_final = faixa_final.replace(',','.')
    maleta = Maleta.objects.filter(nome_maleta=nome_maleta)
    if maleta:
        mensagem = "Maleta já cadastrada!"
        context = {
            'mensagem': mensagem
        }
        return render(request, "cadastrarMaleta.html", context)
    else:
        form_maleta = MaletaForm(request.POST)
        if form_maleta.is_valid():
            maleta = form_maleta.save(commit=False)
            maleta.nome_maleta = nome_maleta
            maleta.faixa_inicial = faixa_inicial
            maleta.faixa_final = faixa_final
            maleta.save()
            form_maleta = MaletaForm()
            mensagem = "Maleta cadastrada com sucesso!"
            maletas = Maleta.objects.filter(id=maleta.id)
            context = {
                'mensagem': mensagem,
                'maletas': maletas
            }
            return render(request, "listarMaletas.html", context)
        else:
            mensagem = "Erro ao cadastrar Maleta"
            context = {
                'mensagem': mensagem,
                'error': form_maleta.errors,
                'tipo': "cadastrar_maleta"
            }
            return render(request, "produtosErros.html", context)

def listarMaletas(request):
    return render(request, "listarMaletas.html")

def listarMaleta(request):
    nome_maleta = request.POST.get("nome_maleta")
    maletas = Maleta.objects.filter(nome_maleta__contains=nome_maleta)
    context = {
        'maletas': maletas
    }
    return render(request, "listarMaletas.html", context)

def editarMaleta(request, mat_id):
    maleta = Maleta.objects.get(id=mat_id)
    context = {
        'maleta': maleta
    }
    return render(request, "editarMaleta.html", context)

def alterarMaleta(request, mat_id):
    nome_maleta = request.POST.get("nome_maleta")
    faixa_inicial = request.POST.get("faixa_inicial")
    faixa_final = request.POST.get("faixa_final")
    faixa_inicial = faixa_inicial.replace(',','.')
    faixa_final = faixa_final.replace(',','.')
    maleta = Maleta.objects.get(id=mat_id)
    if nome_maleta != maleta.nome_maleta:
        maletas = Maleta.objects.filter(nome_maleta=nome_maleta)
        if maletas:
            mensagem = "Maleta já cadastrada!"
            context = {
                'mensagem': mensagem,
                'maletas': maletas
            }
            return render(request, "listarMaletas.html", context)
        else:
            maleta.nome_maleta = nome_maleta
            maleta.faixa_inicial = faixa_inicial
            maleta.faixa_final = faixa_final
            maleta.save()
            mensagem = "Maleta alterada com sucesso!"
            maletas = Maleta.objects.filter(id=mat_id)
            context = {
                'mensagem': mensagem,
                'maletas': maletas
            }
            return render(request, "listarMaletas.html", context)
    else:
        maleta.nome_maleta = nome_maleta
        maleta.faixa_inicial = faixa_inicial
        maleta.faixa_final = faixa_final
        maleta.save()
        mensagem = "Maleta alterada com sucesso!"
        maletas = Maleta.objects.filter(id=mat_id)
        context = {
            'mensagem': mensagem,
            'maletas': maletas
        }
        return render(request, "listarMaletas.html", context)

def deletarMaleta(request, mat_id):
    vendedores = VIEW_VENDEDORES.objects.filter(id_maleta=mat_id)
    if vendedores:
        mensagem = "Maleta não pode ser excluída pois está associada a um ou mais Vendedores(as)"
        context = {
            'mensagem': mensagem,
            'vendedores': vendedores
        }
        return render(request, "listarVendedores.html", context)
    else:
        deletar_maleta = deletaMaleta(request, mat_id)
        mensagem = "Maleta deletada com sucesso!"
        context = {
            'mensagem': mensagem
        }
        return render(request, "listarMaletas.html", context)

def listarProdutosMaleta(request):
    des_produto = request.POST.get("des_produto")
    cod_produto = request.POST.get("cod_produto")
    if des_produto:
        produtos = Produto.objects.filter(des_produto__contains=des_produto)
    elif cod_produto:
        produtos = Produto.objects.filter(cod_produto__contains=cod_produto)
    else:
        produtos = Produto.objects.all()
    if request.user.is_authenticated:
        user_id = request.user.id
        usuario = User.objects.get(id=user_id)
        username = usuario.username
        vendedor = Vendedor.objects.get(username=username)
        id_maleta = vendedor.id_maleta
        maleta = Maleta.objects.get(id=id_maleta)
    context = {
        'produtos': produtos,
        'vendedor': vendedor,
        'maleta': maleta
    }
    return render(request, "abrirMaletaVendedor.html", context)

def abrirMaletaVendedor(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        usuario = User.objects.get(id=user_id)
        username = usuario.username
        maleta_aberta = VIEW_MALETA_ABERTA.objects.filter(vendedor=username)
        if maleta_aberta:
            mensagem = "Maleta já está aberta para esse Vendedor, se desejar incluir mais Produtos na Maleta vá em Adicionar Produto Maleta"
            context = {
                'mensagem': mensagem,
                'maletas': maleta_aberta
            }
            return render(request, "listarMaletaAberta.html", context)
        else:
            try:
                vendedor = Vendedor.objects.get(username=username)
                id_maleta = vendedor.id_maleta
                maleta = Maleta.objects.get(id=id_maleta)
            except:
                mensagem = "Vendedor não cadastrado, não é possível abrir Maleta!"
                maletas = Maleta.objects.all()
                context = {
                    'mensagem': mensagem,
                    'username': username,
                    'maletas': maletas
                }
                return render(request, "cadastrarVendedor.html", context)
            produtos = Produto.objects.all()
            context = {
                'vendedor': vendedor,
                'maleta': maleta,
                'produtos': produtos
            }
            return render(request, "abrirMaletaVendedor.html", context)

def abrirMaleta(request):
    vendedor = request.POST.get("vendedor")
    id_maleta = request.POST.get("id_maleta")
    cod_produto = request.POST.get("cod_produto")
    quantidade = request.POST.get("quantidade")
    id_maletaaberta = request.POST.get("id_maletaaberta")
    maleta = VIEW_MALETA_ABERTA.objects.filter(vendedor=vendedor, id_maleta=id_maleta)
    if maleta:
        mensagem = "Maleta já aberta para esse vendedor"
        context = {
            'mensagem': mensagem,
            'error': "Maleta já aberta!",
            'tipo': "abrir_maleta"
        }
        return render(request, "produtosErros.html", context)
    else:
        vendedores = Vendedor.objects.get(username=vendedor)
        if not vendedores:
            mensagem = "Vendedor não cadastrado para esse usuário, não é possível abrir Maleta!"
            context = {
                'mensagem'
            }
            return render(request, "cadastrarVendedor.html", context)
        else:
            form_maletaaberta = MaletaAbertaForm(request.POST)
            if form_maletaaberta.is_valid():
                maletaaberta = form_maletaaberta.save(commit=False)
                maletaaberta.id_maleta = id_maleta
                maletaaberta.vendedor = vendedor
                maletaaberta.save()
                form_maletaberta = MaletaAbertaForm()
                form_maletaproduto = MaletaAbertaProdutosForm(request.POST)
                if form_maletaproduto.is_valid():
                    maletaproduto = form_maletaproduto.save(commit=False)
                    maletaproduto.id_maletaaberta = maletaaberta.id
                    maletaproduto.cod_produto = cod_produto
                    maletaproduto.quantidade = quantidade
                    maletaproduto.qtde_vendida = 0
                    maletaproduto.save()
                    form_maletaproduto = MaletaAbertaProdutosForm()
                    atualizar_estoque_produto = atualizarEstoqueProdutoMaleta(request, cod_produto, quantidade)
                    mensagem = "Maleta aberta com sucesso!"
                    maletas = VIEW_MALETA_ABERTA.objects.filter(id=maletaaberta.id)
                    context = {
                        'mensagem': mensagem,
                        'maletas': maletas
                    }
                    return render(request, "listarMaletaAberta.html", context)
                else:
                    mensagem = "Não foi possível cadastrar Maleta"
                    context = {
                        'mensagem': mensagem,
                        'error': form_maletaproduto.errors,
                        'tipo': "abrir_maleta"
                    }
                    return render(request, "produtosErros.html", context)
            else:
                mensagem = "Não foi possível cadastrar Maleta"
                context = {
                    'mensagem': mensagem,
                    'error': form_maletaaberta.errors,
                    'tipo': "abrir_maleta"
                }
                return render(request, "produtosErros.html", context)

def listarMaletaAberta(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        usuario = User.objects.get(id=user_id)
        username = usuario.username
        maletas = VIEW_MALETA_ABERTA.objects.filter(vendedor=username)
        context = {
            'maletas': maletas
        }
        return render(request, "listarMaletaAberta.html", context)

def listarProdutoMaleta(request):
    des_produto = request.POST.get("des_produto")
    cod_produto = request.POST.get("cod_produto")
    if request.user.is_authenticated:
        user_id = request.user.id
        usuario = User.objects.get(id=user_id)
        username = usuario.username
        if des_produto:
            maletas = VIEW_MALETA_ABERTA.objects.filter(vendedor=username, des_produto__contains=des_produto)
        elif cod_produto:
            maletas = VIEW_MALETA_ABERTA.objects.filter(vendedor=username, cod_produto__contains=cod_produto)
        else:
            maletas = VIEW_MALETA_ABERTA.objects.filter(vendedor=username)
        context = {
            'maletas': maletas
        }
        return render(request, "listarMaletaAberta.html", context)

def editarMaletaAberta(request, mal_id, cod_produto):
    maleta = VIEW_MALETA_ABERTA.objects.get(id=mal_id, cod_produto=cod_produto)
    produtos = VIEW_MALETA_ABERTA.objects.all().exclude(cod_produto=maleta.cod_produto)
    produto = Produto.objects.get(cod_produto=cod_produto)
    context = {
        'maleta': maleta,
        'produtos': produtos,
        'produto': produto
    }
    return render(request, "editarMaletaProduto.html", context)

def alterarMaletaProduto(request, mal_id, cod_prod):
    cod_produto = request.POST.get("cod_produto")
    quantidade = request.POST.get("quantidade")
    maleta_aberta = VIEW_MALETA_ABERTA.objects.filter(id=mal_id, cod_produto=cod_produto)
    if maleta_aberta:
        maleta_aberta = VIEW_MALETA_ABERTA.objects.get(id=mal_id, cod_produto=cod_produto)
        produto = VIEW_MALETA_PRODUTOS.objects.get(id_maletaaberta=mal_id, cod_produto=cod_produto)
        if int(quantidade) < int(produto.qtde_vendida):
            mensagem = "Quantidade vendida maior que quantidade informada, não é possível alterar!"
            maletas = VIEW_MALETA_ABERTA.objects.filter(id=mal_id)
            if request.user.is_authenticated:
                user_id = request.user.id
                grupo = Group.objects.get(user=user_id)
            context = {
                'mensagem': mensagem,
                'maletas': maletas
            }
            if str(grupo) == 'admin' or str(grupo) == 'supervisor':
                return render(request, "listarMaletaVendedores.html", context)
            else:
                return render(request, "listarMaletaAberta.html", context)
        else:
            if cod_prod != cod_produto:
                vendas_maleta = VendaProduto.objects.filter(id=maleta.id, cod_produto=cod_produto)
                if vendas_maleta:
                    produto = VIEW_MALETA_PRODUTOS.objects.get(id_maletaaberta=mal_id, cod_produto=cod_produto)
                    if produto.qtde_vendida > 0:
                        mensagem = "Não é possível alterar produto da maleta pois o mesmo já possui venda registrada!"
                        vendas = VIEW_FLUXO_CAIXA.objects.filter(id=maleta_aberta.id)
                        context = {
                            'mensagem': mensagem,
                            'vendas': vendas
                        }
                        return render(request, "relatorioVendasVendedor.html", context)
                    else:
                        maleta_aberta = VIEW_MALETA_PRODUTOS.objects.get(id_maletaaberta=mal_id, cod_produto=cod_produto)
                        maleta = MaletaAbertaProdutos.objects.get(id_maletaaberta=maleta_aberta.id_maletaaberta, cod_produto=cod_produto)
                        maleta.cod_produto = cod_produto
                        maleta.quantidade = quantidade
                        maleta.save()
                        mensagem = "Maleta alterada com sucesso!"
                        maletas = VIEW_MALETA_ABERTA.objects.filter(id=maleta_aberta.id_maletaaberta)
                        if request.user.is_authenticated:
                            user_id = request.user.id
                            grupo = Group.objects.get(user=user_id)
                        context = {
                            'mensagem': mensagem,
                            'maletas': maletas
                        }
                        if str(grupo) == 'admin' or str(grupo) == 'supervisor':
                            return render(request, "listarMaletaVendedores.html", context)
                        else:
                            return render(request, "listarMaletaAberta.html", context)
                else:
                    maleta_aberta = VIEW_MALETA_ABERTA.objects.get(id=mal_id, cod_produto=cod_produto)
                    maleta = MaletaAbertaProdutos.objects.get(id_maletaaberta=maleta_aberta.id_maletaaberta, cod_produto=cod_produto)
                    maleta.cod_produto = cod_produto
                    maleta.quantidade = quantidade
                    maleta.save()
                    mensagem = "Maleta alterada com sucesso!"
                    maletas = VIEW_MALETA_ABERTA.objects.filter(id=maleta_aberta.id)
                    if request.user.is_authenticated:
                        user_id = request.user.id
                        grupo = Group.objects.get(user=user_id)
                    context = {
                        'mensagem': mensagem,
                        'maletas': maletas
                    }
                    if str(grupo) == 'admin' or str(grupo) == 'supervisor':
                        return render(request, "listarMaletaVendedores.html", context)
                    else:
                        return render(request, "listarMaletaAberta.html", context)
            else:
                maleta_aberta = VIEW_MALETA_ABERTA.objects.get(id=mal_id, cod_produto=cod_produto)
                maleta = MaletaAbertaProdutos.objects.get(id_maletaaberta=maleta_aberta.id, cod_produto=cod_produto)
                maleta.cod_produto = cod_produto
                maleta.quantidade = quantidade
                maleta.save()
                mensagem = "Maleta alterada com sucesso!"
                maletas = VIEW_MALETA_ABERTA.objects.filter(id=maleta_aberta.id)
                if request.user.is_authenticated:
                    user_id = request.user.id
                    grupo = Group.objects.get(user=user_id)
                context = {
                    'mensagem': mensagem,
                    'maletas': maletas
                }
                if str(grupo) == 'admin' or str(grupo) == 'supervisor':
                    return render(request, "listarMaletaVendedores.html", context)
                else:
                    return render(request, "listarMaletaAberta.html", context)

def listarMaletaVendedores(request):
    return render(request, "listarMaletaVendedores.html")

def listarMaletaVendedor(request):
    nome_vendedor = request.POST.get("nome_vendedor")
    des_produto = request.POST.get("des_produto")
    if nome_vendedor and des_produto:
        maletas = VIEW_MALETA_ABERTA.objects.filter(nome_vendedor__contains=nome_vendedor, des_produto__contains=des_produto)
    elif nome_vendedor:
        maletas = VIEW_MALETA_ABERTA.objects.filter(nome_vendedor__contains=nome_vendedor)
    elif des_produto:
        maletas = VIEW_MALETA_ABERTA.objects.filter(des_produto__contains=des_produto)
    else:
        maletas = VIEW_MALETA_ABERTA.objects.all()
    context = {
        'maletas': maletas
    }
    return render(request, "listarMaletaVendedores.html", context)

def deletarMaletaAberta(request, mal_id, cod_produto):
    venda = ""
    maleta_aberta = VIEW_MALETA_ABERTA.objects.get(id=mal_id, cod_produto=cod_produto)
    try:
        produtos = VIEW_MALETA_PRODUTOS.objects.get(id_maletaaberta=mal_id, cod_produto=cod_produto)
        if produtos.qtde_vendida > 0:
            mensagem = "Não é possível deletar produto da maleta pois o mesmo já possui venda registrada!"
            vendas = VIEW_FLUXO_CAIXA.objects.filter(cod_produto=cod_produto)
            context = {
                'mensagem': mensagem,
                'vendas': vendas
            }
            return render(request, "relatorioVendasVendedor.html", context)
        else:
            vendas_maleta = VendaProduto.objects.filter(id_venda=venda.id, cod_produto=cod_produto)
            if vendas_maleta:
                vendas_maleta = VendaProduto.objects.get(id_venda=venda.id, cod_produto=cod_produto)
                mensagem = "Não é possível deletar produto da maleta pois o mesmo já possui venda registrada!"
                vendas = VIEW_FLUXO_CAIXA.objects.filter(id=vendas_maleta.id_venda)
                context = {
                    'mensagem': mensagem,
                    'vendas': vendas
                }
                return render(request, "relatorioVendasVendedor.html", context)
    except:
        deletar_maleta_produto = deletarMaletaProduto(request, mal_id, cod_produto)
        mal_aberta = getMaletaAberta(request, mal_id, cod_produto)
        cont = mal_aberta[0]['cont']
        if cont == 0:
            deleta_maleta = deletaMaletaAberta(request, mal_id)
            if venda:
                deleta_venda_produto = deletaVendaProduto(request, venda.id, cod_produto)
                deleta_venda = deletarVenda(request, venda.id)
        else:
            if venda:
                deleta_venda_produto = deletaVendaProduto(request, venda.id, cod_produto)
        atualizar_estoque_produto = atualizarQtdeEstoqueProdMaleta(request, cod_produto, maleta_aberta.quantidade)
        mensagem = "Produto deletado da Maleta com sucesso!"
        maletas = VIEW_MALETA_ABERTA.objects.filter(id=mal_id)
        context = {
            'mensagem': mensagem,
            'maletas': maletas
        }
        return render(request, "listarMaletaAberta.html", context)

def adicionarProdutoMaleta(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        usuario = User.objects.get(id=user_id)
        username = usuario.username
        maletas = VIEW_MALETA_ABERTA.objects.filter(vendedor=username)
        context = {
            'maletas': maletas,
            'vendedor': username
        }
        return render(request, "adicionarProdutoMaleta.html", context)
    else:
        mensagem = "Usuário não logado, não é possível adicionar produto à Maleta"
        context = {
            'mensagem': mensagem,
            'error': "Usuário não logado!",
            'tipo': "adicionar_produto_maleta"
        }
        return render(request, "produtosErros.html", context)

def addProdutoMaleta(request, mal_id, cod_produto):
    if request.user.is_authenticated:
        user_id = request.user.id
        usuario = User.objects.get(id=user_id)
        username = usuario.username
        vendedor = Vendedor.objects.get(username=username)
        maleta = VIEW_MALETA_ABERTA.objects.get(id=mal_id, cod_produto=cod_produto)
        produtos = Produto.objects.all().exclude(cod_produto=cod_produto)
        context = {
            'maleta': maleta,
            'produtos': produtos,
            'vendedor': vendedor,
        }
        return render(request, "addProdutoMaleta.html", context)
    else:
        mensagem = "Usuário não logado, não é possível adicionar produto à Maleta"
        context = {
            'mensagem': mensagem,
            'error': "Usuário não logado!",
            'tipo': "adicionar_produto_maleta"
        }
        return render(request, "produtosErros.html", context)

def efetivarAdicionarProdutoMaleta(request):
    vendedor = request.POST.get("vendedor")
    id_maletaaberta = request.POST.get("id_maletaaberta")
    cod_produto = request.POST.get("cod_produto")
    quantidade = request.POST.get("quantidade")
    produto_maleta = VIEW_MALETA_ABERTA.objects.filter(vendedor=vendedor, cod_produto=cod_produto)
    if produto_maleta:
        mensagem = "Produto já adicionado nessa Maleta"
        context = {
            'mensagem': mensagem,
            'maletas': produto_maleta
        }
        return render(request, "listarMaletaAberta.html", context)
    else:
        inserir_produto_maleta = inserirProdutoMaleta(request, id_maletaaberta, cod_produto, quantidade)
        maletas = VIEW_MALETA_ABERTA.objects.filter(id=id_maletaaberta)
        mensagem = "Produto adicionado à Maleta com sucessso!"
        context = {
            'mensagem': mensagem,
            'maletas': maletas
        }
        return render(request, "listarMaletaAberta.html", context)
