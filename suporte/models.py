from django.db import models
from sites.models import SiteParceiro

STATUS_CHOICES = [
    ('aberto', 'Aberto'),
    ('respondido', 'Respondido'),
    ('fechado', 'Fechado'),
]

class Suporte(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    site = models.ForeignKey(SiteParceiro, on_delete=models.SET_NULL, null=True, blank=True)
    mensagem = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='aberto')
    resposta = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Chamado #{self.pk} - {self.nome}'
