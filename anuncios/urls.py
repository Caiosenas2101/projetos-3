from django.urls import path
from . import views

urlpatterns = [
    path('', views.meus_anuncios, name='anuncios'),
    path('novo/', views.cadastrar_anuncio, name='cadastrar_anuncio'),
    path('editar/<int:pk>/', views.editar_anuncio, name='editar_anuncio'),
    path('excluir/<int:pk>/', views.excluir_anuncio, name='excluir_anuncio'),
    path('rotativos/', views.anuncios_rotativos, name='anuncios_rotativos'),
] 