from django import forms
from .models import SistemCerdas

class SistemCerdasForm(forms.ModelForm):
    class Meta:
        model = SistemCerdas
        fields = ['file_sistem_cerdas']