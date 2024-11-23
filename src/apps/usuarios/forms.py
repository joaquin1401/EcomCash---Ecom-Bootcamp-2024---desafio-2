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
        super(FormTransferencia, self).__init__(*args, **kwargs)
        self.fields['monto'].widget.attrs = {
            'required': True,
            'placeholder': 'Ejemplo de placeholder',
            'type':'text'
        }
    class Meta:
        model = Transferencia
        # solo muestra estos dos campos
        fields = ["monto", "cvu_destino", "motivo"]

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
