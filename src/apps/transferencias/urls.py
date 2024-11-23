from django.urls import path

from . import views
# importacion para el logout
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse_lazy


app_name ="transferencias"
urlpatterns = [
    path("comprobante/<int:pk>", views.Comprobante.as_view(), name="comprobante"),
    path("listado/", views.TransferenciaListView.as_view(), name="listado"),
    path("crear/", views.TransferenciaCreateView.as_view(), name="crear"),
    # MOTIVOS
    path('motivos/', views.Motivos.as_view(), name='motivos'),
    path('motivos/eliminar/<int:pk>', views.MotivoDeleteView.as_view(), name='motivos_eliminar'),
]