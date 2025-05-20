from django.contrib import admin
from .models import SiteParceiro

@admin.register(SiteParceiro)
class SiteParceiroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario', 'status', 'data_criacao')
    search_fields = ('nome', 'url', 'usuario__username')
    list_filter = ('status', 'data_criacao')
