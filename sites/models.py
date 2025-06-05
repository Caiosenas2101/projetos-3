from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = [
    ('ativo', 'Ativo'),
    ('inativo', 'Inativo'),
    ('pendente', 'Pendente'),
]

class SiteParceiro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sites')
    nome = models.CharField(max_length=100)
    url = models.URLField()
    descricao = models.TextField(blank=True)
    resumo = models.TextField('Resumo de apresentação', help_text='Conte para a comunidade o que é o seu site, diferenciais, etc.')
    imagem = models.ImageField(upload_to='sites/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
