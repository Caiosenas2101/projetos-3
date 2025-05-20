from django import forms
from .models import Anuncio

class AnuncioForm(forms.ModelForm):
    class Meta:
        model = Anuncio
        fields = ['site', 'titulo', 'imagem', 'data_inicio', 'data_fim', 'status'] 