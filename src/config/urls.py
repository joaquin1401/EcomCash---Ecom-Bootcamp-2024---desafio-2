from django.contrib import admin
from django.urls import path, include
from . import views
from apps.usuarios import views as views_usuarios
from django.contrib.auth import views as views_django
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # prueba /generales
    path('admin/', admin.site.urls),
    path("base/", views.prueba, name="base"),
    # apps
    path("usuarios/", include("apps.usuarios.urls")),
    path("transferencias/", include("apps.transferencias.urls")),
    # login y logout
    path('accounts/login/', views_usuarios.CustomLoginView.as_view(), name='login'),
    path("logout/", views_django.logout_then_login, name="logout"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
