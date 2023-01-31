# Generated by Django 4.1.4 on 2023-01-30 18:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigB',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('Compression', models.CharField(blank=True, default='H.264', max_length=100, null=True, verbose_name='Compression')),
                ('resolution', models.CharField(blank=True, default='720p', max_length=100, null=True, verbose_name='Resolution')),
                ('SmartCodec', models.CharField(blank=True, default='Off', max_length=100, null=True, verbose_name='SmartCodec')),
                ('FPS', models.IntegerField(blank=True, default=4, null=True, verbose_name='FPS')),
                ('BitRateControl', models.CharField(blank=True, default='VBR', max_length=100, null=True, verbose_name='BitRateControl')),
                ('Quality', models.IntegerField(blank=True, default=4, null=True, verbose_name='Quality')),
                ('BitRate', models.IntegerField(blank=True, default=512, null=True, verbose_name='BitRate')),
                ('VideoEnable', models.CharField(blank=True, default='true', max_length=20, null=True, verbose_name='Video Enable')),
                ('Language', models.CharField(blank=True, default='English', max_length=100, null=True, verbose_name='Language')),
                ('CurrentTime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='CurrentTime')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha creacion')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Ultima modificacion')),
            ],
            options={
                'verbose_name': 'ConfigB',
                'verbose_name_plural': 'ConfigsB',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='SitioB',
            fields=[
                ('sitio', models.IntegerField(primary_key=True, serialize=False, verbose_name='SitioB')),
                ('proyecto', models.CharField(blank=True, max_length=20, null=True, verbose_name='Proyecto')),
                ('ip', models.CharField(blank=True, max_length=80, null=True, verbose_name='Ip')),
                ('status', models.CharField(blank=True, max_length=50, null=True, verbose_name='Status')),
                ('is_alive', models.CharField(blank=True, max_length=50, null=True, verbose_name='Is alive')),
                ('last_update', models.DateTimeField(verbose_name='Last update')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Ultima modificacion')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha creacion')),
            ],
            options={
                'verbose_name': 'SitioB',
                'verbose_name_plural': 'SitiosB',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='StreamB',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha creacion')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Ultima modificacion')),
                ('id_config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_stream', to='comparator.configb', verbose_name='ConfigB')),
            ],
            options={
                'verbose_name': 'StreamB',
                'verbose_name_plural': 'StreamsB',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('number', models.IntegerField(verbose_name='Number')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha creacion')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Ultima modificacion')),
                ('sitio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_channel', to='comparator.sitiob', verbose_name='SitioB')),
                ('streams', models.ManyToManyField(to='comparator.streamb', verbose_name='StreamsB')),
            ],
            options={
                'verbose_name': 'Channel',
                'verbose_name_plural': 'Channel',
                'ordering': ['-created'],
            },
        ),
    ]
