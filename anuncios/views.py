from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Anuncio
from .forms import AnuncioForm
from django.utils import timezone

# Create your views here.

@login_required
def meus_anuncios(request):
    anuncios = Anuncio.objects.filter(usuario=request.user)
    return render(request, 'anuncios/anuncios.html', {'anuncios': anuncios})

@login_required
def cadastrar_anuncio(request):
    if request.method == 'POST':
        form = AnuncioForm(request.POST, request.FILES)
        if form.is_valid():
            anuncio = form.save(commit=False)
            anuncio.usuario = request.user
            anuncio.save()
            messages.success(request, 'Anúncio cadastrado com sucesso!')
            return redirect('anuncios')
    else:
        form = AnuncioForm()
    return render(request, 'anuncios/cadastro_anuncio.html', {'form': form})

@login_required
def editar_anuncio(request, pk):
    anuncio = get_object_or_404(Anuncio, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = AnuncioForm(request.POST, request.FILES, instance=anuncio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Anúncio atualizado com sucesso!')
            return redirect('anuncios')
    else:
        form = AnuncioForm(instance=anuncio)
    return render(request, 'anuncios/editar_anuncio.html', {'form': form, 'anuncio': anuncio})

@login_required
def excluir_anuncio(request, pk):
    anuncio = get_object_or_404(Anuncio, pk=pk, usuario=request.user)
    if request.method == 'POST':
        anuncio.delete()
        messages.success(request, 'Anúncio excluído com sucesso!')
        return redirect('anuncios')
    return render(request, 'anuncios/excluir_anuncio.html', {'anuncio': anuncio})

def anuncios_rotativos(request):
    anuncios = Anuncio.objects.filter(status='ativo', data_inicio__lte=timezone.now(), data_fim__gte=timezone.now())
    return render(request, 'anuncios/anuncios_rotativos.html', {'anuncios': anuncios})
