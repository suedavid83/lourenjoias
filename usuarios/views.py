from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import VIEW_USUARIOS_GRUPO, Cliente, Vendedor, VIEW_VENDEDORES
from .forms import ClienteForm, VendedorForm
from produtos.models import Maleta, ComissaoMaletaVendedor, MaletaAberta, VIEW_MALETA_ABERTA
from .functions import deletaVendedor
from gerenciamento.models import Venda, VIEW_FLUXO_CAIXA

def cadastrarUsuario(request):
    grupos = Group.objects.filter().exclude(name="admin")
    context = {
        'grupos': grupos
    }
    return render(request, "cadastrarUsuario.html", context)

def efetuarCadastroUsuario(request):
    email = request.POST.get('email')
    try:
        usuario = User.objects.get(email=email)
        if usuario:
            mensagem = "Email já cadastrado"
            context = {
                'mensagem': mensagem,
                'error': "Email duplicado!",
                'tipo': "cadastroUsuario"
            }
            return render(request, "errosAcoes.html", context)
    except:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                grupo_id = request.POST.get('grupo')
                user = form.save(commit=False)
                user.username = username
                user.set_password(raw_password)
                user.email = email
                user.save()
                form = UserCreationForm()
                user = authenticate(username=username, password=raw_password)
                grupo = Group.objects.get(id=grupo_id)
                user = User.objects.get(username=username)
                user.groups.add(grupo)
                mensagem = "Usuário cadastrado com successo!"
                context = {
                    'mensagem': mensagem
                }
                return render(request, "home.html", context)
            else:
                mensagem = "Erro ao cadastrar usuário"
                context = {
                    'mensagem': mensagem,
                    'error': form.errors,
                    'tipo': "cadastrarUsuario"
                }
                return render(request, "errosUsuarios.html", context)
        return render(request, 'cadastrarUsuario.html', context)

def listarUsuarios(request):
    return render(request, "listarUsuarios.html")

def filtrarUsuario(request):
    username = request.POST.get("username")
    if username:
        usuarios = VIEW_USUARIOS_GRUPO.objects.filter(username__contains=username)
    else:
        usuarios = VIEW_USUARIOS_GRUPO.objects.all()
    context = {
        'usuarios': usuarios
    }
    return render(request, "listarUsuarios.html", context)

def editarUsuario(request, user_id):
    usuario = VIEW_USUARIOS_GRUPO.objects.get(id=user_id)
    grupos = Group.objects.all().exclude(name=usuario.grupo)
    context = {
        'usuario': usuario,
        'grupos': grupos
    }
    return render(request, "editarUsuario.html", context)

def alterarUsuario(request):
    username = request.POST.get("username")
    grupo = request.POST.get("grupo")
    print('grupo')
    print(grupo)
    email = request.POST.get("email")
    usuario = VIEW_USUARIOS_GRUPO.objects.get(username=username)
    grupo_atual = Group.objects.get(name=usuario.grupo)
    usuario = User.objects.get(username=username)
    usuario.email = email
    usuario.groups.remove(grupo_atual)
    usuario.groups.add(grupo)
    usuario.save()
    mensagem = "Usuário alterado com sucesso"
    usuarios = VIEW_USUARIOS_GRUPO.objects.filter(username__contains=username)
    context = {
        'mensagem': mensagem,
        'usuarios': usuarios
    }
    return render(request, "listarUsuarios.html", context)


def deletarUsuario(request, user_id):
    pass

def cadastrarCliente(request):
    return render(request, "cadastrarCliente.html")

def efetuarCadastroCliente(request):
    nome_cliente = request.POST.get("nome_cliente")
    endereco = request.POST.get("endereco")
    bairro = request.POST.get("bairro")
    cidade = request.POST.get("cidade")
    estado = request.POST.get("estado")
    cep = request.POST.get("cep")
    telefone = request.POST.get("telefone")
    email = request.POST.get("email")
    whatsapp = request.POST.get("whatsapp")
    cliente = Cliente.objects.filter(nome_cliente=nome_cliente)
    if cliente:
        mensagem = "Cliente já existente!"
        context = {
            'mensagem': mensagem,
            'cliente': cliente
        }
        return render(request, "cadastrarCliente.html", context)
    else:
        cliente = Cliente.objects.filter(email=email)
        if cliente:
            mensagem = "Email já cadastrado para outro cliente!"
            context = {
                'mensagem': mensagem,
                'cliente': cliente
            }
            return render(request, "cadastrarCliente.html", context)
        else:
            usuario = User.objects.filter(email=email)
            if usuario:
                mensagem = "Email já cadastrado para outro usuário!"
                context = {
                    'mensagem': mensagem
                }
                return render(request, "listarClientes.html", context)
            else:
                form_cliente = ClienteForm(request.POST)
                if form_cliente.is_valid():
                    cliente = form_cliente.save(commit=False)
                    cliente.nome_cliente = nome_cliente
                    cliente.endereco = endereco
                    cliente.bairro = bairro
                    cliente.cidade = cidade
                    cliente.estado = estado
                    cliente.cep = cep
                    cliente.telefone = telefone
                    cliente.email = email
                    cliente.whatsapp = whatsapp
                    cliente.save()
                    form_cliente = ClienteForm()
                    mensagem = "Cliente cadastrado com sucesso!"
                    clientes = Cliente.objects.filter(id=cliente.id)
                    context = {
                        'mensagem': mensagem,
                        'clientes': clientes
                    }
                    return render(request, "listarClientes.html", context)
                else:
                    mensagem = "Erro ao cadastrar Cliente"
                    context = {
                        'mensagem': mensagem,
                        'error': form_cliente.errors,
                        'tipo': "cadastrar_cliente"
                    }
                    return render(request, "errosUsuarios.html", context)

def listarClientes(request):
    return render(request, "listarClientes.html")

def listarCliente(request):
    nome_cliente = request.POST.get("nome_cliente")
    clientes = Cliente.objects.filter(nome_cliente__contains=nome_cliente)
    context = {
        'clientes': clientes
    }
    return render(request, "listarClientes.html", context)

def editarCliente(request, cli_id):
    cliente = Cliente.objects.get(id=cli_id)
    context = {
        'cliente': cliente
    }
    return render(request, "editarCliente.html", context)

def alterarCliente(request, cli_id):
    nome_cliente = request.POST.get("nome_cliente")
    endereco = request.POST.get("endereco")
    bairro = request.POST.get("bairro")
    cidade = request.POST.get("cidade")
    estado = request.POST.get("estado")
    cep = request.POST.get("cep")
    telefone = request.POST.get("telefone")
    email = request.POST.get("email")
    whatsapp = request.POST.get("whatsapp")
    cliente = Cliente.objects.get(id=cli_id)
    if nome_cliente != cliente.nome_cliente:
        cliente = Cliente.objects.filter(nome_cliente=nome_cliente)
        if cliente:
            mensagem = "Cliente já existente!"
            context = {
                'mensagem': mensagem,
                'cliente': cliente
            }
            return render(request, "cadastrarCliente.html", context)
    elif email != cliente.email:
        cliente = Cliente.objects.filter(email=email)
        if clientes:
            mensagem = "Email já cadastrado para outro Cliente!"
            context = {
                'mensagem': mensagem,
                'cliente': cliente
            }
            return render(request, "cadastrarCliente.html", context)
    else:
        usuario = User.objects.filter(email=email)
        if usuario:
            mensagem = "Email já cadastrado para outro usuário!"
            context = {
                'mensagem': mensagem
            }
            return render(request, "listarClientes.html", context)
        else:
            cliente.nome_cliente = nome_cliente
            cliente.endereco = endereco
            cliente.bairro = bairro
            cliente.cidade = cidade
            cliente.estado = estado
            cliente.cep = cep
            cliente.telefone = telefone
            cliente.email = email
            cliente.whatsapp = whatsapp
            cliente.save()
            mensagem = "Cliente alterado com sucesso!"
            clientes = Cliente.objects.filter(id=cli_id)
            context = {
                'mensagem': mensagem,
                'clientes': clientes
            }
            return render(request, "listarClientes.html", context)

def deletarCliente(request, cli_id):
    pass

def cadastrarVendedor(request):
    usuarios = ""
    username = ""
    if request.user.is_authenticated:
        user_id = request.user.id
        usuario = User.objects.get(id=user_id)
        username = usuario.username
        try:
            vendedor = Vendedor.objects.get(username=username)
            if vendedor:
                mensagem = "Vendedor já cadastrado para esse usuário"
                context = {
                    'mensagem': mensagem,
                    'error': "Vendedor já cadastrado!",
                    'tipo': "cadastro_vendedor"
                }
                return render(request, "errosUsuarios.html", context)
        except:
            vendedor = ""
    else:
        usuarios = VIEW_USUARIOS_GRUPO.objects.filter(grupo="vendedor")
    maletas = Maleta.objects.all()
    context = {
        'username': username,
        'usuarios': usuarios,
        'maletas': maletas
    }
    return render(request, "cadastrarVendedor.html", context)

def efetuarCadastroVendedor(request):
    username = request.POST.get("username")
    nome_vendedor = request.POST.get("nome_vendedor")
    cpf_cnpj = request.POST.get("cpf_cnpj")
    rg = request.POST.get("rg")
    endereco = request.POST.get("endereco")
    bairro = request.POST.get("bairro")
    cidade = request.POST.get("cidade")
    estado = request.POST.get("estado")
    cep = request.POST.get("cep")
    telefone = request.POST.get("telefone")
    id_maleta = request.POST.get("id_maleta")
    ref1_empresa = request.POST.get("ref1_empresa")
    ref1_contato = request.POST.get("ref1_contato")
    ref1_telefone = request.POST.get("ref1_telefone")
    ref2_empresa = request.POST.get("ref2_empresa")
    ref2_contato = request.POST.get("ref2_contato")
    ref2_telefone = request.POST.get("ref2_telefone")
    vendedor = Vendedor.objects.filter(username=username)
    if vendedor:
        mensagem = "Esse usuário já possui Vendedor cadastrado!"
        vendedores = VIEW_VENDEDORES.objects.filter(username=username)
        context = {
            'mensagem': mensagem,
            'vendedores': vendedores
        }
        return render(request, "listarVendedores.html", context)
    else:
        vendedor = Vendedor.objects.filter(cpf_cnpj=cpf_cnpj)
        if vendedor:
            mensagem = "CPF / CNPJ já cadastrado para outro Vendedor"
            vendedores = VIEW_VENDEDORES.objects.filter(cpf_cnpj=cpf_cnpj)
            context = {
                'mensagem': mensagem,
                'vendedores': vendedores
            }
            return render(request, "listarVendedores.html", context)
        else:
            vendedor = Vendedor.objects.filter(rg=rg)
            if vendedor:
                mensagem = "RG já cadastrado para outro Vendedor"
                vendedores = VIEW_VENDEDORES.objects.filter(rg=rg)
                context = {
                    'mensagem': mensagem,
                    'vendedores': vendedores
                }
                return render(request, "listarVendedores.html", context)
            else:
                form_vendedor = VendedorForm(request.POST)
                if form_vendedor.is_valid():
                    vendedor = form_vendedor.save(commit=False)
                    vendedor.username = username
                    vendedor.nome_vendedor = nome_vendedor
                    vendedor.cpf_cnpj = cpf_cnpj
                    vendedor.rg = rg
                    vendedor.endereco = endereco
                    vendedor.bairro = bairro
                    vendedor.cidade = cidade
                    vendedor.estado = estado
                    vendedor.cep = cep
                    vendedor.telefone = telefone
                    vendedor.id_maleta = id_maleta
                    vendedor.ref1_empresa = ref1_empresa
                    vendedor.ref1_contato = ref1_contato
                    vendedor.ref1_telefone = ref1_telefone
                    vendedor.ref2_empresa = ref2_empresa
                    vendedor.ref2_contato = ref2_contato
                    vendedor.ref2_telefone = ref2_telefone
                    vendedor.save()
                    form_vendedor = VendedorForm()
                    mensagem = "Vendedor(a) cadastrado(a) com sucesso!"
                    vendedores = VIEW_VENDEDORES.objects.filter(id=vendedor.id)
                    context = {
                        'mensagem': mensagem,
                        'vendedores': vendedores
                    }
                    return render(request, "listarVendedores.html", context)
                else:
                    mensagem = "Erro ao cadastrar Vendedor"
                    context = {
                        'mensagem': mensagem,
                        'error': form_vendedor.errors,
                        'tipo': "cadastrar_vendedor"
                    }
                    return render(request, "errosUsuarios.html", context)

def listarVendedores(request):
    return render(request, "listarVendedores.html")

def listarVendedor(request):
    nome_vendedor = request.POST.get("nome_vendedor")
    vendedores = VIEW_VENDEDORES.objects.filter(nome_vendedor__contains=nome_vendedor)
    context = {
        'vendedores': vendedores
    }
    return render(request, "listarVendedores.html", context)

def editarVendedor(request, vend_id):
    vendedor = VIEW_VENDEDORES.objects.get(id=vend_id)
    maleta = ComissaoMaletaVendedor.objects.filter(id_maleta=vendedor.id_maleta)
    if not maleta:
        maleta = Maleta.objects.get(id=maleta.id)
        nome_maleta = maleta.nome_maleta
        maletas = Maleta.objects.all().exclude(id=vendedor.id_maleta)
    else:
        maleta = Maleta.objects.filter(id=vendendor.id_maleta)
        nome_maleta = maleta.nome_maleta
        maletas = ""
    context = {
        'vendedor': vendedor,
        'maletas': maletas,
        'nome_maleta': nome_maleta
    }
    return render(request, "editarVendedor.html", context)

def editaVendedor(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        usuario = User.objects.get(id=user_id)
        username = usuario.username
        vendedor = Vendedor.objects.get(username=username)
        maleta = ComissaoMaletaVendedor.objects.filter(id_maleta=vendedor.id_maleta)
        if not maleta:
            maleta = Maleta.objects.get(id=vendedor.id_maleta)
            nome_maleta = maleta.nome_maleta
            maletas = Maleta.objects.all().exclude(id=vendedor.id_maleta)
        else:
            maleta = Maleta.objects.get(id=vendedor.id_maleta)
            nome_maleta = maleta.nome_maleta
            maletas = ""
        context = {
            'vendedor': vendedor,
            'maletas': maletas,
            'nome_maleta': nome_maleta
        }
        return render(request, "editarVendedor.html", context)
    else:
        mensagem = "Usuário não logado, não é possível editar Vendedor"
        context = {
            'mensagem': mensagem,
            'error': "Usuário não logado!",
            'tipo': "alterar_vendedor"
        }
        return render(request, "errosUsuarios.html", context)


def alterarVendedor(request, vend_id):
    username = request.POST.get("username")
    nome_vendedor = request.POST.get("nome_vendedor")
    cpf_cnpj = request.POST.get("cpf_cnpj")
    rg = request.POST.get("rg")
    endereco = request.POST.get("endereco")
    bairro = request.POST.get("bairro")
    cidade = request.POST.get("cidade")
    estado = request.POST.get("estado")
    cep = request.POST.get("cep")
    telefone = request.POST.get("telefone")
    id_maleta = request.POST.get("id_maleta")
    ref1_empresa = request.POST.get("ref1_empresa")
    ref1_contato = request.POST.get("ref1_contato")
    ref1_telefone = request.POST.get("ref1_telefone")
    ref2_empresa = request.POST.get("ref2_empresa")
    ref2_contato = request.POST.get("ref2_contato")
    ref2_telefone = request.POST.get("ref2_telefone")
    vendedor = Vendedor.objects.get(id=vend_id)
    if cpf_cnpj != vendedor.cpf_cnpj:
        vendedores = VIEW_VENDEDORES.objects.filter(cpf_cnpj=cpf_cnpj)
        if vendedores:
            mensagem = "CPF / CNPJ já cadastrado para outro Vendedor"
            context = {
                'mensagem': mensagem,
                'vendedores': vendedores
            }
            return render(request, "listarVendedores.html", context)
    else:
        if rg != vendedor.rg:
            vendedores = VIEW_VENDEDORES.objects.filter(rg=rg)
            if vendedores:
                mensagem = "RG já cadastrado para outro Vendedor"
                context = {
                    'mensagem': mensagem,
                    'vendedores': vendedores
                }
                return render(request, "listarVendedores.html", context)
            else:
                vendedor.nome_vendedor = nome_vendedor
                vendedor.cpf_cnpj = cpf_cnpj
                vendedor.rg = rg
                vendedor.endereco = endereco
                vendedor.bairro = bairro
                vendedor.cidade = cidade
                vendedor.estado = estado
                vendedor.cep = cep
                vendedor.telefone = telefone
                vendedor.id_maleta = id_maleta
                vendedor.ref1_empresa = ref1_empresa
                vendedor.ref1_contato = ref1_contato
                vendedor.ref1_telefone = ref1_telefone
                vendedor.ref2_empresa = ref2_empresa
                vendedor.ref2_contato = ref2_contato
                vendedor.ref2_telefone = ref2_telefone
                vendedor.save()
                mensagem = "Vendedor alterado com sucesso!"
                vendedores = VIEW_VENDEDORES.objects.filter(id=vend_id)
                context = {
                    'mensagem': mensagem,
                    'vendedores': vendedores
                }
                return render(request, "listarVendedores.html", context)
        else:
            vendedor.nome_vendedor = nome_vendedor
            vendedor.cpf_cnpj = cpf_cnpj
            vendedor.rg = rg
            vendedor.endereco = endereco
            vendedor.bairro = bairro
            vendedor.cidade = cidade
            vendedor.estado = estado
            vendedor.cep = cep
            vendedor.telefone = telefone
            vendedor.id_maleta = id_maleta
            vendedor.ref1_empresa = ref1_empresa
            vendedor.ref1_contato = ref1_contato
            vendedor.ref1_telefone = ref1_telefone
            vendedor.ref2_empresa = ref2_empresa
            vendedor.ref2_contato = ref2_contato
            vendedor.ref2_telefone = ref2_telefone
            vendedor.save()
            mensagem = "Vendedor alterado com sucesso!"
            vendedores = VIEW_VENDEDORES.objects.filter(id=vend_id)
            context = {
                'mensagem': mensagem,
                'vendedores': vendedores
            }
            return render(request, "listarVendedores.html", context)


def deletarVendedor(request, vend_id):
    vendedor = Vendedor.objects.get(id=vend_id)
    maleta = MaletaAberta.objects.filter(vendedor=vendedor.username)
    if maleta:
        mensagem = "Não é possível excluir Vendedor pois existe uma Maleta aberta em seu nome!"
        maletas = VIEW_MALETA_ABERTA.objects.filter(vendedor=vendedor.username)
        context = {
            'mensagem': mensagem,
            'maletas': maletas
        }
        return render(request, "listarMaletaAberta.html", context)
    else:
        vendas = Venda.objects.filter(vendedor=vendedor.username)
        if vendas:
            mensagem = "Não é possível excluir Vendedor pois existe venda registrada em seu nome!"
            maletas = VIEW_FLUXO_CAIXA.objects.filter(vendedor=vendedor.username)
            context = {
                'mensagem': mensagem,
                'vendas': maletas
            }
            return render(request, "relatorioVendasVendedor.html", context)
        else:
            deletar_vendedor = deletaVendedor(request, vend_id)
            mensagem = "Vendedor deletado com sucesso!"
            context  = {
                'mensagem': mensagem
            }
            return render(request, "listarVendedores.html", context)
