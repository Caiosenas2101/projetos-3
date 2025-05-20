from django.contrib import admin
from .models import Suporte

@admin.register(Suporte)
class SuporteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'site', 'status', 'data_criacao')
    search_fields = ('nome', 'email', 'mensagem')
    list_filter = ('status', 'data_criacao')
