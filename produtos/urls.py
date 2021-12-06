from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('cadastrarProduto', views.cadastrarProduto, name="cadastrarProduto"),
    path('cadastrarProdutoVendedor', views.cadastrarProdutoVendedor, name="cadastrarProdutoVendedor"),
    path('efetuarCadastroProduto', views.efetuarCadastroProduto, name="efetuarCadastroProduto"),
    path('cadastrarCategoria', views.cadastrarCategoria, name="cadastrarCategoria"),
    path('efetuarCadastroCategoria', views.efetuarCadastroCategoria, name="efetuarCadastroCategoria"),
    path('listarProdutos', views.listarProdutos, name="listarProdutos"),
    path('listarProduto', views.listarProduto, name="listarProduto"),
    path('editarProduto/<int:prod_id>/', views.editarProduto, name="editarProduto"),
    path('deletarProduto/<str:cod_produto>/', views.deletarProduto, name="deletarProduto"),
    path('alterarProduto/<int:prod_id>/', views.alterarProduto, name="alterarProduto"),
    path('listarCategorias', views.listarCategorias, name="listarCategorias"),
    path('listarCategoria', views.listarCategoria, name="listarCategoria"),
    path('editarCategoria/<int:cat_id>/', views.editarCategoria, name="editarCategoria"),
    path('deletarCategoria/<int:cat_id>/', views.deletarCategoria, name="deletarCategoria"),
    path('alterarCategoria/<int:cat_id>/', views.alterarCategoria, name="alterarCategoria"),
    path('cadastrarMaleta', views.cadastrarMaleta, name="cadastrarMaleta"),
    path('efetuarCadastroMaleta', views.efetuarCadastroMaleta, name="efetuarCadastroMaleta"),
    path('listarMaletas', views.listarMaletas, name="listarMaletas"),
    path('listarMaleta', views.listarMaleta, name="listarMaleta"),
    path('listarMaletaVendedores', views.listarMaletaVendedores, name="listarMaletaVendedores"),
    path('listarMaletaVendedor', views.listarMaletaVendedor, name="listarMaletaVendedor"),
    path('listarProdutosMaleta', views.listarProdutosMaleta, name="listarProdutosMaleta"),
    path('listarProdutoMaleta', views.listarProdutoMaleta, name="listarProdutoMaleta"),
    path('editarMaleta/<int:mat_id>/', views.editarMaleta, name="editarMaleta"),
    path('alterarMaleta/<int:mat_id>/', views.alterarMaleta, name="alterarMaleta"),
    path('deletarMaleta/<int:mat_id>/', views.deletarMaleta, name="deletarMaleta"),
    path('abrirMaletaVendedor', views.abrirMaletaVendedor, name="abrirMaletaVendedor"),
    path('abrirMaleta', views.abrirMaleta, name="abrirMaleta"),
    path('listarMaletaAberta', views.listarMaletaAberta, name="listarMaletaAberta"),
    path('editarMaletaAberta/<int:mal_id>/<str:cod_produto>/', views.editarMaletaAberta, name="editarMaletaAberta"),
    path('alterarMaletaProduto/<int:mal_id>/<str:cod_prod>/', views.alterarMaletaProduto, name="alterarMaletaProduto"),
    path('deletarMaletaAberta/<int:mal_id>/<str:cod_produto>/', views.deletarMaletaAberta, name="deletarMaletaAberta"),
    path('adicionarProdutoMaleta', views.adicionarProdutoMaleta, name="adicionarProdutoMaleta"),
    path('addProdutoMaleta/<int:mal_id>/<str:cod_produto>/', views.addProdutoMaleta, name="addProdutoMaleta"),
    path('efetivarAdicionarProdutoMaleta', views.efetivarAdicionarProdutoMaleta, name="efetivarAdicionarProdutoMaleta")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
