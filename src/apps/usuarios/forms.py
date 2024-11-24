from django import forms
from .models import Usuario
from apps.transferencias.models import Transferencia
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm


# personalizacion del login
class LoginFormUsuario(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"id": "usuario",'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        label="Usuario"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"id": "password",'class': 'form-control', 'placeholder': 'Contraseña'}),
        label="Contraseña"
    )

class CrearFormUsuario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = "__all__"
    # asigna a todos ditectamete la clase >>>>
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            clase_existente = campo.widget.attrs.get('class', '')
            campo.widget.attrs['class'] = f'{clase_existente} form-control'.strip()


class FormTransferencia(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            clase_existente = campo.widget.attrs.get('class', '')
            campo.widget.attrs['class'] = f'{clase_existente} form-control'.strip()
    class Meta:
        model = Transferencia
        # solo muestra estos dos campos
        fields = ["monto", "cvu_destino", "motivo"]


class FormRetiro(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            clase_existente = campo.widget.attrs.get('class', '')
            campo.widget.attrs['class'] = f'{clase_existente} form-control'.strip()
    class Meta:
        model = Transferencia
        # solo muestra estos dos campos
        fields = ["monto",  "motivo"]


class FormIngreso(forms.ModelForm):
    class Meta:
        model = Transferencia
        # solo muestra estos dos campos
        fields = ["monto", "motivo"]
    # asigna a todos ditectamete la clase >>>>
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            clase_existente = campo.widget.attrs.get('class', '')
            campo.widget.attrs['class'] = f'{clase_existente} form-control'.strip()



class FormUsuarioRegistradoEditar(forms.ModelForm):
    class Meta:
        model = Usuario
        # solo muestra estos dos campos
        fields = ["dni", "cuil","first_name", "last_name", "email", "password"]
    # asigna a todos ditectamete la clase >>>>
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            clase_existente = campo.widget.attrs.get('class', '')
            campo.widget.attrs['class'] = f'{clase_existente} form-control'.strip()




# usuario registrado > EDITAR foto perfil
class FotoPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['foto_perfil']
        widgets = {
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }