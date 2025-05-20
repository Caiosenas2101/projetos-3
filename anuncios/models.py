from django.db import models
from django.contrib.auth.models import User
from sites.models import SiteParceiro

STATUS_CHOICES = [
    ('ativo', 'Ativo'),
    ('pendente', 'Pendente'),
    ('expirado', 'Expirado'),
]

class Anuncio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='anuncios')
    site = models.ForeignKey(SiteParceiro, on_delete=models.CASCADE, related_name='anuncios')
    titulo = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='anuncios/')
    data_inicio = models.DateField()
    data_fim = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo
