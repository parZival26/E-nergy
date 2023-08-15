from django import forms
from .models import Casa

class CasaForm(forms.ModelForm):
    class Meta:
        model = Casa
        fields = ['name', 'areaCuadrada']

class AgregarValoresForm(forms.Form):
    valor_kwh = forms.IntegerField(label='Valor Kwh', min_value=0)
    valor_pagar = forms.IntegerField(label='Valor de Factura', min_value=0)
