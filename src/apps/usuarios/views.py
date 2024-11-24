from django.shortcuts import render
# importacion del modelo
from .models import Usuario
# importacion generic views de django
from django.views.generic.list import ListView
from django.views.generic import UpdateView, DetailView
from django.views.generic.edit import DeleteView, CreateView
from django.contrib.auth.views import LoginView, LogoutView

####
from django.urls import reverse_lazy
from django.contrib import messages
from django import forms

###
from .forms import CrearFormUsuario, FormTransferencia, LoginFormUsuario, FormIngreso, FormUsuarioRegistradoEditar, FormRetiro

from apps.transferencias.models import Transferencia, Motivo
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


                # VISTAS USUARIO REGISTRADO
from django.db.models import Q

# usuario registrado > PERFIL
class UsuarioRegistradoPerfil(LoginRequiredMixin, TemplateView):
    template_name = 'usuarios/registrados/perfil.html'

# usuario registrado > INICIO
class UsuarioRegistradoInicio(LoginRequiredMixin, TemplateView):
    template_name = 'usuarios/registrados/inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user  # Usuario autenticado
        context['user_info'] = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'saldo': user.saldo,
            # Agrega más información si es necesario
        }
        return context
    
# usuario registrado > MOVIMIENTOS
class MovimientosUsuarioRegistrado(LoginRequiredMixin, TemplateView):
    template_name = "usuarios/registrados/movimientos.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # consulta de base de datos > de todas las transferencias filtrar las que corresponden con el usuario
        # Consulta con Q para filtrar por usuario en origen o destino
        usuario = self.request.user
        transferencias = Transferencia.objects.filter(
            Q(origen=usuario) | Q(destino=usuario)
        ).order_by('-fecha')  # Ordenar por fecha descendente

        context["transferencias"] = transferencias
        return context

# usuario registrado > TRANSFERIR
class TransferirUsuarioRegistrado(LoginRequiredMixin, CreateView):
    model = Transferencia
    template_name = "usuarios/registrados/transferir.html"
    context_object_name = "transferencia"
    form_class = FormTransferencia
    
    def form_valid(self, form):
        # EXTRACCION DE DATOS DEL FORM
        monto = form.cleaned_data.get('monto')
        cvu_usuario_destino = form.cleaned_data.get('cvu_destino')
        seleccion_motivo = form.cleaned_data.get('seleccion_motivo')
        # CONTROL QUE EL MONTO NO SEA MAYOR AL SALIDO
        if monto > self.request.user.saldo:
            form.add_error('monto', f"Solo tienes {self.request.user.saldo} en tu cuenta")
            return self.form_invalid(form)  # Regresa al formulario con errores
        
        # LOGICA DE LA TRANSFERENCIA

        # conslto si existe el cvu ingresado
        if Usuario.objects.filter(cvu=cvu_usuario_destino):
            # asigno al objeto transferencia, el usuario de destino
            form.instance.destino = Usuario.objects.filter(cvu=cvu_usuario_destino)[0]
            # actualizo el saldo de la cuenta de destino
            nuevo_saldo_d = monto + Usuario.objects.filter(cvu=cvu_usuario_destino)[0].saldo
            Usuario.objects.filter(cvu=cvu_usuario_destino).update(saldo = nuevo_saldo_d)
        else:
            form.add_error('cvu_destino', f"No existe usuario registrado con ese CVU")
            return self.form_invalid(form) 
        
        # obtengo cvu del usuario logueado
        cvu_usuario_logueado=(self.request.user.cvu)
        # nuevo saldo = saldo del usuario logueado - monto de transferencia
        nuevo_saldo = self.request.user.saldo - monto
        # guardo los cambios
        Usuario.objects.filter(cvu=cvu_usuario_logueado).update(saldo = nuevo_saldo)


        #form.instance.motivo = Motivo.objects.filter(motivo=seleccion_motivo)
        print(seleccion_motivo)
        # origen = usuario > por defecto
        form.instance.origen = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        # Generar la URL dinámica en tiempo de ejecución
        return reverse_lazy('usuarios:registrados_inicio')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # obtener todas las transferencias de un usuario
        context["motivos"] = Motivo.objects.all()
        return context

# usuario registrado > EDITAR
class EditarUsuarioRegistrado(LoginRequiredMixin, UpdateView):
    model = Usuario
    template_name = "usuarios/registrados/editar.html"
    # atributos que quiero modificar
    form_class = FormUsuarioRegistradoEditar
    
    def get_success_url(self):
        # Generar la URL dinámica en tiempo de ejecución
        return reverse_lazy('usuarios:registrados_perfil')

from .forms import FotoPerfilForm

class EditarFotoPerfilView(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = FotoPerfilForm
    template_name = 'usuarios/registrados/editar_foto_perfil.html'

    def get_object(self):
        # Retorna el usuario actualmente autenticado
        return self.request.user

    def get_success_url(self):
        # Redirige al perfil del usuario o donde desees
        return reverse_lazy('usuarios:registrados_perfil')


class UsuarioRegistradoIngresar(TemplateView):
    template_name = 'usuarios/registrados/registrados_ingresar.html'

#  de retiro
class UsuarioRegistradoRetirar(LoginRequiredMixin, CreateView):
    model = Transferencia
    template_name = 'usuarios/registrados/retiro.html'
    context_object_name = "transferencia"
    form_class = FormRetiro
    
    def form_valid(self, form):
        # EXTRACCION DE DATOS DEL FORM
        monto = form.cleaned_data.get('monto')

        cvu_usuario_destino = 0
        seleccion_motivo = form.cleaned_data.get('seleccion_motivo')
        # CONTROL QUE EL MONTO NO SEA MAYOR AL SALIDO
        if monto > self.request.user.saldo:
            form.add_error('monto', f"Solo tienes {self.request.user.saldo} en tu cuenta")
            return self.form_invalid(form)  # Regresa al formulario con errores
        
        # LOGICA DE LA TRANSFERENCIA

        # conslto si existe el cvu ingresado
        if Usuario.objects.filter(cvu=cvu_usuario_destino):
            # asigno al objeto transferencia, el usuario de destino
            form.instance.destino = Usuario.objects.filter(cvu=cvu_usuario_destino)[0]
            # actualizo el saldo de la cuenta de destino
            nuevo_saldo_d = monto + Usuario.objects.filter(cvu=cvu_usuario_destino)[0].saldo
            Usuario.objects.filter(cvu=cvu_usuario_destino).update(saldo = nuevo_saldo_d)
        else:
            form.add_error('cvu_destino', f"No existe usuario registrado con ese CVU")
            return self.form_invalid(form) 
        
        # obtengo cvu del usuario logueado
        cvu_usuario_logueado=(self.request.user.cvu)
        # nuevo saldo = saldo del usuario logueado - monto de transferencia
        nuevo_saldo = self.request.user.saldo - monto
        # guardo los cambios
        Usuario.objects.filter(cvu=cvu_usuario_logueado).update(saldo = nuevo_saldo)


        #form.instance.motivo = Motivo.objects.filter(motivo=seleccion_motivo)
        print(seleccion_motivo)
        # origen = usuario > por defecto
        form.instance.origen = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        # Generar la URL dinámica en tiempo de ejecución
        return reverse_lazy('usuarios:registrados_inicio')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # obtener todas las transferencias de un usuario
        context["motivos"] = Motivo.objects.all()
        return context



                # VISTAS ADMIN
# admin > ACTIVIDAD

class Actividad(LoginRequiredMixin, TemplateView):
    template_name = "usuarios/admin/actividad.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # consulta de base de datos > de todas las transferencias filtrar las que corresponden con el usuario
        # Consulta con Q para filtrar por usuario en origen o destino
        usuario = self.request.user
        transferencias = Transferencia.objects.filter(
            Q(origen=usuario) | Q(destino=usuario)
        ).order_by('-fecha')  # Ordenar por fecha descendente

        context["transferencias"] = transferencias
        return context


# admin > LISTADO USUARIOS
class UsuarioListView(ListView):
    model = Usuario
    template_name = "usuarios/admin/listado.html"
    context_object_name = "usuarios"
    paginate_by = 20  # Opcional: Para paginación

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q') # aplicar filtros a la busqueda
        
        try:
            if query:
                queryset = queryset.filter(cvu=query)  # Filtra según el término
            return queryset
        except:
            return queryset # error Z>>>>>


# admin > PERFIL USUARIO REGISTRADO
class UsuarioDetailView(DetailView):
    model = Usuario
    template_name = "usuarios/perfil.html"
    context_object_name = "usuario"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # consulta de base de datos > de todas las transferencias filtrar las que corresponden con el usuario
        # Consulta con Q para filtrar por usuario en origen o destino
        usuario = self.object
        transferencias = Transferencia.objects.filter(
            Q(origen=usuario) | Q(destino=usuario)
        ).order_by('-fecha')  # Ordenar por fecha descendente

        context["transferencias"] = transferencias
        return context

class CambiarEstadoUsuarioView(LoginRequiredMixin, UpdateView):
    model = Usuario
    fields = ["is_active"]  # No necesitas incluir ningún campo del formulario
    template_name = "usuarios/admin/cambiar_estado.html"

    def form_valid(self, form):
        usuario = form.instance
        if usuario.is_active:
            print(usuario.is_active)
            usuario.is_active = False
            print(usuario.is_active)
        else:
            print(usuario.is_active)
            usuario.is_active = True
            print(usuario.is_active)
        # Cambio el estado directamente en el objeto
        # Guarda el cambio
        usuario.save()
        return super().form_valid(form)
        # obtengo el cvu del usuario a cambiar
        #cvu_usuario = form.instance.cvu
        #estado_actual = Usuario.objects.filter(cvu=cvu_usuario)[0].is_active
        #estado_nuevo = not(estado_actual)
        #print(f"estado actual >>>>>: {estado_actual}")
        #print(f"estado nuevo >>>>>: {estado_nuevo}")
        #Usuario.objects.filter(cvu=cvu_usuario).update(is_active = estado_nuevo)
        #return super().form_valid(form)
    

    def get_success_url(self):
        # Generar la URL dinámica en tiempo de ejecución
        return reverse_lazy('usuarios:perfil', kwargs={'pk': self.kwargs['pk']})

# 
class IngresarDinero(LoginRequiredMixin, CreateView):
    model = Transferencia
    template_name = "usuarios/admin/ingresar_dinero.html"
    context_object_name = "transferencia"
    form_class = FormIngreso

    def form_valid(self, form):
        # EXTRACCION DE DATOS DEL FORM
        monto = form.cleaned_data.get('monto')
        seleccion_motivo = form.cleaned_data.get('seleccion_motivo')
        # obtengo el usuario del que estoy viendo
        cvu_usuario_destino = self.kwargs.get('pk')

        # LOGICA DE LA TRANSFERENCIA

        # conslto si existe el cvu ingresado
        if Usuario.objects.filter(cvu=cvu_usuario_destino):
            # asigno al objeto transferencia, el usuario de destino
            form.instance.destino = Usuario.objects.filter(cvu=cvu_usuario_destino)[0]
            # actualizo el saldo de la cuenta de destino
            nuevo_saldo_d = monto + Usuario.objects.filter(cvu=cvu_usuario_destino)[0].saldo
            Usuario.objects.filter(cvu=cvu_usuario_destino).update(saldo = nuevo_saldo_d)
        else:
            form.add_error('cvu_destino', f"No existe usuario registrado con ese CVU")
            return self.form_invalid(form) 
        
        # obtengo cvu del usuario logueado
        cvu_usuario_logueado=(self.request.user.cvu)
        # nuevo saldo = saldo del usuario logueado - monto de transferencia
        nuevo_saldo = self.request.user.saldo - monto
        # guardo los cambios
        Usuario.objects.filter(cvu=cvu_usuario_logueado).update(saldo = nuevo_saldo)


        #form.instance.motivo = Motivo.objects.filter(motivo=seleccion_motivo)
        print(seleccion_motivo)
        # origen = usuario > por defecto
        form.instance.origen = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        # Generar la URL dinámica en tiempo de ejecución
        return reverse_lazy('usuarios:perfil', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# 
class RetirarDinero(LoginRequiredMixin, CreateView):
    model = Transferencia
    template_name = "usuarios/admin/retirar_dinero.html"
    context_object_name = "transferencia"
    form_class = FormIngreso
    
    def form_valid(self, form):
        # EXTRACCION DE DATOS DEL FORM
        monto = form.cleaned_data.get('monto')
        seleccion_motivo = form.cleaned_data.get('seleccion_motivo')



        # destino es ADMIN
        cvu_usuario_destino = self.request.user.cvu 


        # conslto si existe el cvu ingresado
        if Usuario.objects.filter(cvu=cvu_usuario_destino):
            # asigno al objeto transferencia, el usuario de destino
            form.instance.destino = Usuario.objects.filter(cvu=cvu_usuario_destino)[0]
            # actualizo el saldo de la cuenta de destino
            nuevo_saldo_d = monto + Usuario.objects.filter(cvu=cvu_usuario_destino)[0].saldo
            Usuario.objects.filter(cvu=cvu_usuario_destino).update(saldo = nuevo_saldo_d)
        else:
            form.add_error('cvu_destino', f"No existe usuario registrado con ese CVU")
            return self.form_invalid(form) 
        
        # obtengo cvu del usuario origen > le tenfo que descontar
        cvu_usuario_origen=self.kwargs.get('pk')

        # nuevo saldo = saldo del usuario logueado - monto de transferencia
        # le descuento el montooooo
        nuevo_saldo = Usuario.objects.filter(cvu=cvu_usuario_origen)[0].saldo - monto
        # guardo los cambios
        Usuario.objects.filter(cvu=cvu_usuario_origen).update(saldo = nuevo_saldo)


        #form.instance.motivo = Motivo.objects.filter(motivo=seleccion_motivo)
        print(seleccion_motivo)
        # origen = usuario > por defecto
        form.instance.origen = Usuario.objects.filter(cvu=cvu_usuario_origen)[0]
        return super().form_valid(form)
    
    def get_success_url(self):
        # Generar la URL dinámica en tiempo de ejecución
        return reverse_lazy('usuarios:perfil', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context




                        # usuarios NO LOGUEADOS

# CREAR
class UsuarioCreateView(CreateView):
    model = Usuario
    template_name = "usuarios/crear.html"
    form_class = CrearFormUsuario
    success_url = reverse_lazy("login")


# LOGIN
class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'  # Plantilla que se renderiza
    redirect_authenticated_user = True  # Redirige si el usuario ya está autenticado
     # Redirección tras login exitoso (opcional)
    authentication_form = LoginFormUsuario
    # redefino la variable success_url
    def get_success_url(self):
        user = self.request.user
        if user.is_admin:  # Verifica si el usuario es administrador
            return reverse_lazy('usuarios:listado')  # URL para admin
        else:
            return reverse_lazy('usuarios:registrados_inicio')  # URL para usuarios normales


