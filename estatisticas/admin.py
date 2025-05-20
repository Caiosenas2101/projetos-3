from django.contrib import admin
from .models import Estatistica, Post

@admin.register(Estatistica)
class EstatisticaAdmin(admin.ModelAdmin):
    list_display = ('site', 'data', 'visitas', 'cliques', 'curtidas')
    search_fields = ('site__nome',)
    list_filter = ('data',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('autor', 'conteudo', 'data_criacao')
    search_fields = ('conteudo', 'autor__username')
    list_filter = ('data_criacao',)
