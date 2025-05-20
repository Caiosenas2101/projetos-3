from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import UserRegistrationForm, UserUpdateForm, PerfilUpdateForm
from sites.models import SiteParceiro
from django.contrib.auth.models import User
from estatisticas.views import dashboard as dashboard_real

dashboard = dashboard_real

def cadastro(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso! Bem-vindo ao Murall!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'usuarios/cadastro.html', {'form': form})

@login_required
def perfil(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = PerfilUpdateForm(request.POST, request.FILES, instance=request.user.perfil)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('perfil')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = PerfilUpdateForm(instance=request.user.perfil)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'usuarios/perfil.html', context)

def perfil_publico(request, username):
    user = get_object_or_404(User, username=username)
    sites = SiteParceiro.objects.filter(usuario=user)
    return render(request, 'usuarios/perfil_publico.html', {'perfil_user': user, 'sites': sites})

def perfil_site(request, pk):
    site = get_object_or_404(SiteParceiro, pk=pk)
    return render(request, 'usuarios/perfil_site.html', {'site': site})
