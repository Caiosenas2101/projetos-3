from django.contrib import admin
from .models import Perfil

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefone', 'website', 'data_criacao')
    search_fields = ('user__username', 'user__email', 'telefone')
    list_filter = ('data_criacao',)
