from django.shortcuts import render
# importacionn de los modelos
from django.shortcuts import render
# importacion del modelo
from .models import Transferencia, Motivo
# importacion generic views de django
from django.views.generic.list import ListView
from django.views.generic import UpdateView, DetailView
from django.views.generic.edit import DeleteView, CreateView
from django.contrib.auth.views import LoginView

####
from django.urls import reverse_lazy
from django.contrib import messages
###
from .forms import FormTransferencia, FormMotivo


# LISTADO
class TransferenciaListView(ListView):
    model = Transferencia
    template_name = "transferencias/listado.html"
    context_object_name = "transferencias"


# COMPROBANTE
class Comprobante(DetailView):
    model = Transferencia
    template_name = "transferencias/comprobante.html"
    context_object_name = "transferencia"
    

# CREAR
class TransferenciaCreateView(CreateView):
    model = Transferencia
    template_name = "transferencias/crear.html"
    form_class = FormTransferencia
    success_url = reverse_lazy("usuarios:listado")



# MOTIVOS


class Motivos(CreateView):
    model = Motivo
    template_name = "transferencias/motivos.html"
    form_class = FormMotivo
    success_url = reverse_lazy("transferencias:motivos")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["motivos"] = Motivo.objects.all()
        return context

class MotivoDeleteView(DeleteView):
    model = Motivo
    template_name = "transferencias/motivos_eliminar.html"
    success_url = reverse_lazy("transferencias:motivos")
