# Generated by Django 4.1.4 on 2023-01-20 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0008_alter_camera_videoencode_config_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='videoencode_config_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.videoencode', verbose_name='Configuracion de video'),
        ),
    ]
