from django import forms
from .models import Casa

class CasaForm(forms.ModelForm):
    class Meta:
        model = Casa
        fields = ['name', 'areaCuadrada']

class AgregarValoresForm(forms.Form):
    valor_kwh = forms.FloatField()
    valor_pagar = forms.FloatField()
