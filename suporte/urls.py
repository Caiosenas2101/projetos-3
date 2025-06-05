from django.urls import path
from . import views

urlpatterns = [
    path('contato/', views.contato, name='contato'),
    path('sucesso/', views.sucesso, name='sucesso'),
    path('chamados/', views.meus_chamados, name='meus_chamados'),
] 