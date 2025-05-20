from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
        ('usuarios', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name='Notificacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensagem', models.CharField(max_length=255)),
                ('link', models.CharField(max_length=255, blank=True)),
                ('lida', models.BooleanField(default=False)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('destinatario', models.ForeignKey(on_delete=models.CASCADE, related_name='notificacoes', to=settings.AUTH_USER_MODEL)),
                ('remetente', models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notificacoes_enviadas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-data'],
            },
        ),
    ] 