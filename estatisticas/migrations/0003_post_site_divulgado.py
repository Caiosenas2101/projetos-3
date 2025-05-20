from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('estatisticas', '0002_post'),
        ('sites', '0001_initial'),
    ]
    operations = [
        migrations.AddField(
            model_name='post',
            name='site_divulgado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts_divulgacao', to='sites.siteparceiro'),
        ),
    ] 