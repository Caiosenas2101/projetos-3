from django.urls import path
from . import views

urlpatterns = [
    path('', views.painel_estatisticas, name='estatisticas'),
    path('post/editar/<int:pk>/', views.edit_post, name='edit_post'),
    path('post/apagar/<int:pk>/', views.delete_post, name='delete_post'),
] 