from django import forms
from .models import Transferencia, Motivo

class FormTransferencia(forms.ModelForm):
    class Meta:
        model = Transferencia
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            clase_existente = campo.widget.attrs.get('class', '')
            campo.widget.attrs['class'] = f'{clase_existente} form-control'.strip()
    


class FormMotivo(forms.ModelForm):
    class Meta:
        model = Motivo
        fields = "__all__"
    # asigna a todos ditectamete la clase >>>>
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            clase_existente = campo.widget.attrs.get('class', '')
            campo.widget.attrs['class'] = f'{clase_existente} form-control'.strip()