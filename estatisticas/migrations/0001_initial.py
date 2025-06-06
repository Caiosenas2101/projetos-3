# Generated by Django 4.2.11 on 2025-05-20 14:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estatistica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('visitas', models.PositiveIntegerField(default=0)),
                ('cliques', models.PositiveIntegerField(default=0)),
                ('curtidas', models.PositiveIntegerField(default=0)),
                ('criado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estatisticas', to='sites.siteparceiro')),
            ],
            options={
                'ordering': ['-data'],
                'unique_together': {('site', 'data')},
            },
        ),
    ]
