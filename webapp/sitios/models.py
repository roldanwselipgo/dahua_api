from django.db import models
from django.utils.timezone import now
from datetime import datetime

# Create your models here.
class Sitio(models.Model):
    sitio = models.IntegerField(primary_key=True,verbose_name='Sitio')
    proyecto = models.CharField(max_length=20, verbose_name = 'Proyecto', null=True, blank=True)
    ip = models.CharField(max_length=80, verbose_name = 'Ip', null=True, blank=True)
    status = models.CharField(max_length=50, verbose_name = 'Status', null=True, blank=True)
    is_alive = models.CharField(max_length=50, verbose_name = 'Is alive', null=True, blank=True)
    last_update = models.DateTimeField(verbose_name = 'Last update')

    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    created = models.DateTimeField(verbose_name = 'Fecha creacion', default = now)
    class Meta:
        verbose_name = 'Sitio'
        verbose_name_plural = 'Sitios'
        ordering = ['-created']

    def __str__(self):
        return str(self.sitio) + " " + '(' +str(self.ip) + ')'




class Config(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    Compression = models.CharField(max_length=100, verbose_name = 'Compression', null=True, blank=True, default="H.264")
    resolution = models.CharField(max_length=100, verbose_name = 'Resolution', null=True, blank=True, default="720p")
    SmartCodec = models.CharField(max_length=100, verbose_name = 'SmartCodec', null=True, blank=True, default="Off")
    FPS = models.IntegerField(verbose_name='FPS', null=True, blank=True, default=4)
    BitRateControl = models.CharField(max_length=100, verbose_name = 'BitRateControl', null=True, blank=True, default="VBR")
    Quality = models.IntegerField(verbose_name='Quality', null=True, blank=True, default=4)
    BitRate = models.IntegerField(verbose_name='BitRate', null=True, blank=True, default=512)
    
    VideoEnable = models.CharField(max_length=20, verbose_name = 'Video Enable', null=True, blank=True, default="true")
    Language = models.CharField(max_length=100, verbose_name = 'Language', null=True, blank=True, default="English")
    CurrentTime = models.DateTimeField(verbose_name = 'CurrentTime', default = now)

    #Channel = models.IntegerField(verbose_name='Channel', null=False, blank=False, default=0)
    #TypeEncode = models.IntegerField(verbose_name='TypeEncode', null=False, blank=False, default=0)
    #TypeStream = models.CharField(max_length=100, verbose_name = 'TypeStream', null=False, blank=False, default="MainFormat")

    created = models.DateTimeField(verbose_name = 'Fecha creacion', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    #sitio_id = models.ForeignKey(Sitio, verbose_name = 'Sitio', related_name='get_config', on_delete = models.CASCADE)
    class Meta:
        verbose_name = 'Config'
        verbose_name_plural = 'Config'
        ordering = ['-created']

    def __str__(self):
        return str(self.id) + " " + str(self.resolution) + " " + str(self.FPS) + " " + str(self.BitRate) 


class Stream(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    name = models.CharField(max_length=100, verbose_name = 'Name', null=False, blank=False)
    created = models.DateTimeField(verbose_name = 'Fecha creacion', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    id_config = models.ForeignKey(Config, verbose_name = 'Config', related_name='get_stream', on_delete = models.CASCADE)
    class Meta:
        verbose_name = 'Stream'
        verbose_name_plural = 'Streams'
        ordering = ['-created']

    def __str__(self):
        return str(self.id)+" "+str(self.name)+" "+str(self.id_config)

class Channel(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    number = models.IntegerField(verbose_name='Number', null=False, blank=False)
    created = models.DateTimeField(verbose_name = 'Fecha creacion', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    #id_config = models.ForeignKey(Config, verbose_name = 'Config', related_name='get_channel', on_delete = models.CASCADE)
    #id_config = models.ForeignKey(Config, verbose_name = 'Config', related_name='get_channel', on_delete = models.CASCADE)
    sitio = models.ForeignKey(Sitio, verbose_name = 'Sitio', related_name='get_channel', on_delete = models.CASCADE)
    #sitios = models.ManyToManyField(Sitio,verbose_name = 'Sitios')
    streams = models.ManyToManyField(Stream,verbose_name = 'Streams')
    class Meta:
        verbose_name = 'Channel'
        verbose_name_plural = 'Channel'
        ordering = ['-created']

    def __str__(self):
        return str(self.number)+" "+ str(self.sitio)

