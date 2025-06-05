from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from sites.models import SiteParceiro
from .models import Estatistica, Post, Comentario
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.contrib import messages
import random
from usuarios.models import Notificacao

# Create your views here.

@login_required
def painel_estatisticas(request):
    sites = SiteParceiro.objects.filter(usuario=request.user)
    estatisticas = Estatistica.objects.filter(site__in=sites)
    # Resumo geral
    total_visitas = estatisticas.aggregate(total=models.Sum('visitas'))['total'] or 0
    total_cliques = estatisticas.aggregate(total=models.Sum('cliques'))['total'] or 0
    total_curtidas = estatisticas.aggregate(total=models.Sum('curtidas'))['total'] or 0
    # Estatísticas dos últimos 7 dias para gráfico
    hoje = timezone.now().date()
    dias = [hoje - timedelta(days=i) for i in range(6, -1, -1)]
    dados_grafico = []
    for dia in dias:
        dia_stats = estatisticas.filter(data=dia)
        dados_grafico.append({
            'data': dia.strftime('%d/%m'),
            'visitas': dia_stats.aggregate(total=models.Sum('visitas'))['total'] or 0,
            'cliques': dia_stats.aggregate(total=models.Sum('cliques'))['total'] or 0,
            'curtidas': dia_stats.aggregate(total=models.Sum('curtidas'))['total'] or 0,
        })
    labels = [d['data'] for d in dados_grafico]
    visitas = [d['visitas'] for d in dados_grafico]
    cliques = [d['cliques'] for d in dados_grafico]
    curtidas = [d['curtidas'] for d in dados_grafico]
    context = {
        'sites': sites,
        'total_visitas': total_visitas,
        'total_cliques': total_cliques,
        'total_curtidas': total_curtidas,
        'labels': labels,
        'visitas': visitas,
        'cliques': cliques,
        'curtidas': curtidas,
    }
    return render(request, 'estatisticas/estatisticas.html', context)

@login_required
def dashboard(request):
    meus_sites = SiteParceiro.objects.filter(usuario=request.user, status='ativo')
    sugestoes = list(SiteParceiro.objects.filter(status='ativo').exclude(usuario=request.user))
    random.shuffle(sugestoes)
    sugestoes = sugestoes[:4]
    if request.method == 'POST':
        if 'comentario_post_id' in request.POST:
            post_id = request.POST.get('comentario_post_id')
            texto = request.POST.get('comentario_texto', '').strip()
            comentario_pai_id = request.POST.get('comentario_pai_id')
            if texto:
                post = get_object_or_404(Post, pk=post_id)
                comentario_pai = None
                if comentario_pai_id:
                    try:
                        comentario_pai = Comentario.objects.get(pk=comentario_pai_id, post=post)
                    except Comentario.DoesNotExist:
                        comentario_pai = None
                comentario = Comentario.objects.create(
                    autor=request.user,
                    post=post,
                    texto=texto,
                    comentario_pai=comentario_pai
                )
                if post.autor != request.user:
                    Notificacao.objects.create(
                        destinatario=post.autor,
                        remetente=request.user,
                        mensagem=f'{request.user.username} comentou no seu post.',
                        link=f'/dashboard/dashboard/#post-{post.pk}'
                    )
                messages.success(request, 'Comentário publicado!')
            else:
                messages.error(request, 'O comentário não pode ser vazio.')
            return redirect('dashboard')
        elif 'delete_comentario_id' in request.POST:
            comentario_id = request.POST.get('delete_comentario_id')
            comentario = get_object_or_404(Comentario, pk=comentario_id)
            if comentario.autor == request.user or comentario.post.autor == request.user:
                comentario.delete()
                messages.success(request, 'Comentário excluído!')
            else:
                messages.error(request, 'Você não tem permissão para excluir este comentário.')
            return redirect('dashboard')
        else:
            conteudo = request.POST.get('conteudo', '').strip()
            site_id = request.POST.get('site_divulgado')
            site_divulgado = None
            if site_id:
                try:
                    site_divulgado = meus_sites.get(pk=site_id)
                except SiteParceiro.DoesNotExist:
                    site_divulgado = None
            if not conteudo and not site_divulgado:
                messages.error(request, 'Preencha uma mensagem ou selecione um site para divulgar.')
            else:
                Post.objects.create(
                    autor=request.user,
                    conteudo=conteudo,
                    site_divulgado=site_divulgado
                )
                messages.success(request, 'Post publicado com sucesso!')
            return redirect('dashboard')
    posts = Post.objects.all().prefetch_related('comentarios', 'comentarios__autor', 'comentarios__respostas', 'comentarios__respostas__autor')
    return render(request, 'dashboard.html', {'posts': posts, 'meus_sites': meus_sites, 'sugestoes': sugestoes})

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk, autor=request.user)
    meus_sites = SiteParceiro.objects.filter(usuario=request.user, status='ativo')
    if request.method == 'POST':
        conteudo = request.POST.get('conteudo', '').strip()
        site_id = request.POST.get('site_divulgado')
        site_divulgado = None
        if site_id:
            try:
                site_divulgado = meus_sites.get(pk=site_id)
            except SiteParceiro.DoesNotExist:
                site_divulgado = None
        if not conteudo and not site_divulgado:
            messages.error(request, 'Preencha uma mensagem ou selecione um site para divulgar.')
        else:
            post.conteudo = conteudo
            post.site_divulgado = site_divulgado
            post.save()
            messages.success(request, 'Post editado com sucesso!')
            return redirect('dashboard')
    return render(request, 'estatisticas/edit_post.html', {'post': post, 'meus_sites': meus_sites})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, autor=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post apagado com sucesso!')
        return redirect('dashboard')
    return render(request, 'estatisticas/delete_post.html', {'post': post})
