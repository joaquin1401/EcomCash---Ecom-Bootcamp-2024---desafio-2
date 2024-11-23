from django.db import models
from apps.usuarios.models import Usuario

class Motivo(models.Model):
    motivo = models.CharField()
    # define como quiero mostrar en el TEMPLATE!!! IMPORTANTE
    def __str__(self):
        return self.motivo  # aca se mostrará en el select

class Transferencia(models.Model):
    origen = models.ForeignKey(Usuario, related_name = "transfiere", on_delete=models.CASCADE)
    destino = models.ForeignKey(Usuario, related_name = "recibe", on_delete=models.CASCADE)
    cvu_destino = models.IntegerField(default=0)
    monto = models.FloatField()
    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.ForeignKey(Motivo, related_name="motivo_de_transferencia", on_delete=models.CASCADE)

