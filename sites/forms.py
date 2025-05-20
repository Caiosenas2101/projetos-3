from django import forms
from .models import SiteParceiro

class SiteParceiroForm(forms.ModelForm):
    class Meta:
        model = SiteParceiro
        fields = ['nome', 'url', 'descricao', 'resumo', 'imagem', 'status']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição curta (opcional)'}),
            'resumo': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Conte para a comunidade o que é o seu site, diferenciais, etc.'}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        } 