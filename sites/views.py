from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SiteParceiro
from .forms import SiteParceiroForm
from estatisticas.models import Estatistica, Curtida
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count
from usuarios.models import Notificacao

# Create your views here.

@login_required
def meus_sites(request):
    sites = SiteParceiro.objects.filter(usuario=request.user)
    return render(request, 'sites/meus_sites.html', {'sites': sites})

@login_required
def cadastrar_site(request):
    if request.method == 'POST':
        form = SiteParceiroForm(request.POST, request.FILES)
        if form.is_valid():
            site = form.save(commit=False)
            site.usuario = request.user
            site.save()
            messages.success(request, 'Site cadastrado com sucesso!')
            return redirect('meus_sites')
    else:
        form = SiteParceiroForm()
    return render(request, 'sites/cadastro_site.html', {'form': form})

@login_required
def editar_site(request, pk):
    site = get_object_or_404(SiteParceiro, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = SiteParceiroForm(request.POST, request.FILES, instance=site)
        if form.is_valid():
            form.save()
            messages.success(request, 'Site atualizado com sucesso!')
            return redirect('meus_sites')
    else:
        form = SiteParceiroForm(instance=site)
    return render(request, 'sites/editar_site.html', {'form': form, 'site': site})

@login_required
def excluir_site(request, pk):
    site = get_object_or_404(SiteParceiro, pk=pk, usuario=request.user)
    if request.method == 'POST':
        site.delete()
        messages.success(request, 'Site excluído com sucesso!')
        return redirect('meus_sites')
    return render(request, 'sites/excluir_site.html', {'site': site})

def listar_sites_publicos(request):
    sites = SiteParceiro.objects.filter(status='ativo').annotate(total_curtidas=Count('curtidas')).order_by('-total_curtidas')
    sites_curtidos = []
    if request.user.is_authenticated:
        sites_curtidos = list(Curtida.objects.filter(usuario=request.user).values_list('site_id', flat=True))
    return render(request, 'sites/curtidas.html', {'sites': sites, 'sites_curtidos': sites_curtidos})

@require_POST
@login_required
def curtir_site(request, pk):
    site = get_object_or_404(SiteParceiro, pk=pk)
    user = request.user
    # Impede múltiplas curtidas
    if Curtida.objects.filter(usuario=user, site=site).exists():
        return JsonResponse({'error': 'Você já curtiu este site.'}, status=400)
    Curtida.objects.create(usuario=user, site=site)
    # Atualiza estatística do dia
    from django.utils import timezone
    hoje = timezone.now().date()
    estat, _ = Estatistica.objects.get_or_create(site=site, data=hoje)
    estat.curtidas += 1
    estat.save()
    total = Curtida.objects.filter(site=site).count()
    # Notificação para o dono do site
    if site.usuario != user:
        Notificacao.objects.create(
            destinatario=site.usuario,
            remetente=user,
            mensagem=f'{user.username} curtiu seu site "{site.nome}"',
            link=f'/sites/resumo/{site.pk}/'
        )
    return JsonResponse({'curtidas': total})

@login_required
def alterar_status_site(request, pk):
    site = get_object_or_404(SiteParceiro, pk=pk, usuario=request.user)
    if request.method == 'POST':
        if site.status == 'ativo':
            site.status = 'inativo'
            messages.success(request, f'Site "{site.nome}" inativado com sucesso!')
        else:
            site.status = 'ativo'
            messages.success(request, f'Site "{site.nome}" ativado com sucesso!')
        site.save()
    return redirect('meus_sites')

def site_resumo(request, pk):
    site = get_object_or_404(SiteParceiro, pk=pk, status='ativo')
    return render(request, 'sites/site_resumo.html', {'site': site})

@login_required
def notificacoes(request):
    # Exemplo: lista vazia
    notificacoes = []
    return render(request, 'notificacoes.html', {'notificacoes': notificacoes})
