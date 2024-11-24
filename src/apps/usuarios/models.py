from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    cvu = models.AutoField(primary_key=True, unique=True)
    dni = models.IntegerField(default=0)
    cuil = models.IntegerField(default=0)
    saldo = models.FloatField(default=0, blank=True)
      # Asegurar unicidad en la base de datos
    # campo para saber si es administrador, por defecto no lo es
    is_admin = models.BooleanField(default=False)
    foto_perfil = models.ImageField(default="default.png",upload_to='fotos_perfil/', null=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

