from django import forms
from .models import Suporte

class SuporteForm(forms.ModelForm):
    class Meta:
        model = Suporte
        fields = ['nome', 'email', 'site', 'mensagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome', 'autofocus': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Seu e-mail'}),
            'site': forms.Select(attrs={'class': 'form-select'}),
            'mensagem': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descreva sua dúvida ou problema', 'rows': 5}),
        } 