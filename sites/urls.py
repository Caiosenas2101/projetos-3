from django.urls import path
from . import views

urlpatterns = [
    path('meus/', views.meus_sites, name='meus_sites'),
    path('novo/', views.cadastrar_site, name='cadastrar_site'),
    path('editar/<int:pk>/', views.editar_site, name='editar_site'),
    path('excluir/<int:pk>/', views.excluir_site, name='excluir_site'),
    path('publicos/', views.listar_sites_publicos, name='curtidas'),
    path('curtir/<int:pk>/', views.curtir_site, name='curtir_site'),
    path('status/<int:pk>/', views.alterar_status_site, name='alterar_status_site'),
    path('resumo/<int:pk>/', views.site_resumo, name='site_resumo'),
    path('notificacoes/', views.notificacoes, name='notificacoes'),
] 