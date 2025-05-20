from django.contrib import admin
from .models import Anuncio

@admin.register(Anuncio)
class AnuncioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'site', 'status', 'data_inicio', 'data_fim')
    search_fields = ('titulo', 'usuario__username', 'site__nome')
    list_filter = ('status', 'data_inicio', 'data_fim')
