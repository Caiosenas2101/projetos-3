from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/<str:username>/', views.perfil_publico, name='perfil_publico'),
    path('site/<int:pk>/', views.perfil_site, name='perfil_site'),
    path('senha/alterar/', 
        auth_views.PasswordChangeView.as_view(
            template_name='usuarios/password_change.html',
            success_url='/usuarios/senha/alterada/'
        ), 
        name='password_change'
    ),
    path('senha/alterada/', 
        auth_views.PasswordChangeDoneView.as_view(
            template_name='usuarios/password_change_done.html'
        ), 
        name='password_change_done'
    ),
    path('dashboard/', views.dashboard, name='dashboard'),
] 