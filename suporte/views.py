from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SuporteForm
from .models import Suporte
from django.contrib.auth.decorators import login_required

# Create your views here.

# Formulário de contato

def contato(request):
    if request.method == 'POST':
        form = SuporteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensagem enviada com sucesso! Em breve entraremos em contato.')
            return redirect('sucesso')
    else:
        form = SuporteForm()
    return render(request, 'suporte/contato.html', {'form': form})

# Listagem de chamados do usuário
@login_required
def meus_chamados(request):
    chamados = Suporte.objects.filter(email=request.user.email).order_by('-data_criacao')
    return render(request, 'suporte/chamados.html', {'chamados': chamados})

def sucesso(request):
    return render(request, 'suporte/sucesso.html')
