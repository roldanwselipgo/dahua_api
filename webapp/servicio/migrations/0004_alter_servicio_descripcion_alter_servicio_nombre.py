# Generated by Django 4.1.4 on 2023-07-04 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicio', '0003_servicio_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='descripcion',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Descripcion'),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='nombre',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Nombre'),
        ),
    ]
