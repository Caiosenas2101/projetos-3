from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from sites.models import SiteParceiro
from PIL import Image
import os

STATUS_CHOICES = [
    ('ativo', 'Ativo'),
    ('pendente', 'Pendente'),
    ('expirado', 'Expirado'),
]

def validate_image_size(image):
    max_size = 5 * 1024 * 1024  # 5MB
    if image.size > max_size:
        raise ValidationError('A imagem deve ter no máximo 5MB.')

def validate_image_dimensions(image):
    img = Image.open(image)
    if img.width > 1920 or img.height > 1080:
        raise ValidationError('A imagem deve ter no máximo 1920x1080 pixels.')

def validate_date_range(data_inicio, data_fim):
    if data_inicio and data_fim and data_inicio > data_fim:
        raise ValidationError('A data de início deve ser anterior à data de fim.')

class Anuncio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='anuncios')
    site = models.ForeignKey(SiteParceiro, on_delete=models.CASCADE, related_name='anuncios')
    titulo = models.CharField(max_length=100)
    imagem = models.ImageField(
        upload_to='anuncios/',
        validators=[validate_image_size, validate_image_dimensions]
    )
    data_inicio = models.DateField()
    data_fim = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    clicks = models.PositiveIntegerField(default=0)
    visualizacoes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-data_criacao']
        indexes = [
            models.Index(fields=['status', 'data_inicio', 'data_fim']),
            models.Index(fields=['usuario', 'site']),
        ]

    def __str__(self):
        return self.titulo

    def clean(self):
        validate_date_range(self.data_inicio, self.data_fim)
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def incrementar_click(self):
        self.clicks += 1
        self.save(update_fields=['clicks'])

    def incrementar_visualizacao(self):
        self.visualizacoes += 1
        self.save(update_fields=['visualizacoes'])

    @property
    def esta_ativo(self):
        hoje = timezone.now().date()
        return self.status == 'ativo' and self.data_inicio <= hoje <= self.data_fim

    def atualizar_status(self):
        hoje = timezone.now().date()
        if self.data_fim < hoje:
            self.status = 'expirado'
            self.save(update_fields=['status'])
