from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('cadastrarUsuario', views.cadastrarUsuario, name="cadastrarUsuario"),
    path('efetuarCadastroUsuario', views.efetuarCadastroUsuario, name="efetuarCadastroUsuario"),
    path('listarUsuarios', views.listarUsuarios, name="listarUsuarios"),
    path('filtrarUsuario', views.filtrarUsuario, name="filtrarUsuario"),
    path('editarUsuario/<int:user_id>/', views.editarUsuario, name="editarUsuario"),
    path('deletarUsuario/<int:user_id>/', views.deletarUsuario, name="deletarUsuario"),
    path('alterarUsuario', views.alterarUsuario, name="alterarUsuario"),
    path('cadastrarCliente', views.cadastrarCliente, name="cadastrarCliente"),
    path('efetuarCadastroCliente', views.efetuarCadastroCliente, name="efetuarCadastroCliente"),
    path('listarClientes', views.listarClientes, name="listarClientes"),
    path('listarCliente', views.listarCliente, name="listarCliente"),
    path('editarCliente/<int:cli_id>/', views.editarCliente, name="editarCliente"),
    path('alterarCliente/<int:cli_id>/', views.alterarCliente, name="alterarCliente"),
    path('deletarCliente/<int:cli_id>/', views.deletarCliente, name="deletarCliente"),
    path('cadastrarVendedor', views.cadastrarVendedor, name="cadastrarVendedor"),
    path('efetuarCadastroVendedor', views.efetuarCadastroVendedor, name="efetuarCadastroVendedor"),
    path('listarVendedores', views.listarVendedores, name="listarVendedores"),
    path('listarVendedor', views.listarVendedor, name="listarVendedor"),
    path('editarVendedor/<int:vend_id>/', views.editarVendedor, name="editarVendedor"),
    path('editarVendedor', views.editaVendedor, name="editaVendedor"),
    path('alterarVendedor/<int:vend_id>/', views.alterarVendedor, name="alterarVendedor"),
    path('deletarVendedor/<int:vend_id>/', views.deletarVendedor, name="deletarVendedor")
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
