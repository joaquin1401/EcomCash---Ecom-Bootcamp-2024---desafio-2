from django.urls import path

from . import views
# importacion para el logout
from django.urls import reverse_lazy


app_name ="usuarios"
urlpatterns = [
    # vistas USUARIO REGISTRADO
    path("registrados/inicio/", views.UsuarioRegistradoInicio.as_view(), name="registrados_inicio"),
    path("registrados/transferir/", views.TransferirUsuarioRegistrado.as_view(), name="registrados_transferir"),
    path("registrados/movimientos/", views.MovimientosUsuarioRegistrado.as_view(), name="registrados_movimientos"),
    path("registrados/perfil/", views.UsuarioRegistradoPerfil.as_view(), name="registrados_perfil"),
    path("editar/<int:pk>", views.EditarUsuarioRegistrado.as_view(), name="editar"),
    path('registrados/editar_foto/', views.EditarFotoPerfilView.as_view(), name='editar_foto'),
    path('registrados/ingresar/', views.UsuarioRegistradoIngresar.as_view(), name='registrados_ingresar'),
    path('registrados/retirar/', views.UsuarioRegistradoRetirar.as_view(), name='registrados_retirar'),

    # vistas ADMIN
    path("listado/", views.UsuarioListView.as_view(), name="listado"),
    path("perfil/<int:pk>", views.UsuarioDetailView.as_view(), name="perfil"),
    path("cambiar_estado/<int:pk>", views.CambiarEstadoUsuarioView.as_view(), name="cambiar_estado"),
    path("ingresar_dinero/<int:pk>", views.IngresarDinero.as_view(), name="ingresar_dinero"),
    path("retirar_dinero/<int:pk>", views.RetirarDinero.as_view(), name="retirar_dinero"),
    path("actividad/", views.Actividad.as_view(), name="actividad"),

    # vistas USUARIO NO REGISTRADO
    path("crear/", views.UsuarioCreateView.as_view(), name="crear"),


]

