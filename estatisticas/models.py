from django.db import models
from sites.models import SiteParceiro
from django.contrib.auth.models import User

class Estatistica(models.Model):
    site = models.ForeignKey(SiteParceiro, on_delete=models.CASCADE, related_name='estatisticas')
    data = models.DateField()
    visitas = models.PositiveIntegerField(default=0)
    cliques = models.PositiveIntegerField(default=0)
    curtidas = models.PositiveIntegerField(default=0)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('site', 'data')
        ordering = ['-data']

    def __str__(self):
        return f'Estatísticas de {self.site.nome} em {self.data}'

class Post(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    conteudo = models.TextField(max_length=280, blank=True)
    imagem = models.ImageField(upload_to='posts/', blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    site_divulgado = models.ForeignKey('sites.SiteParceiro', null=True, blank=True, on_delete=models.SET_NULL, related_name='posts_divulgacao')

    class Meta:
        ordering = ['-data_criacao']

    def __str__(self):
        if self.site_divulgado:
            return f'{self.autor.username} divulgou {self.site_divulgado.nome}'
        return f'{self.autor.username}: {self.conteudo[:30]}'

class Curtida(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='curtidas')
    site = models.ForeignKey(SiteParceiro, on_delete=models.CASCADE, related_name='curtidas')
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'site')

    def __str__(self):
        return f'{self.usuario.username} curtiu {self.site.nome}'

class Comentario(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField(max_length=300)
    data_criacao = models.DateTimeField(auto_now_add=True)
    comentario_pai = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='respostas')

    class Meta:
        ordering = ['data_criacao']

    def __str__(self):
        return f'Comentário de {self.autor.username} em {self.post.id}'
