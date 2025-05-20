from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('sites', '0001_initial'),
    ]
    operations = [
        migrations.AddField(
            model_name='siteparceiro',
            name='resumo',
            field=models.TextField(default='', verbose_name='Resumo de apresentação', help_text='Conte para a comunidade o que é o seu site, diferenciais, etc.'),
            preserve_default=False,
        ),
    ] 