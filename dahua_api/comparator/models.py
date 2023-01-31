from django.db import models
from django.utils.timezone import now
from datetime import datetime

# Create your models here.
class SitioB(models.Model):
    sitio = models.IntegerField(primary_key=True,verbose_name='SitioB')
    #no_local = models.IntegerField(verbose_name='LocalNo', null=False, blank=False)
    #machine_name = models.CharField(max_length=200, verbose_name = 'Machine name', null=True, blank=True)
    #machine_adress = models.CharField(max_length=200, verbose_name = 'Machine address', null=True, blank=True)
    proyecto = models.CharField(max_length=20, verbose_name = 'Proyecto', null=True, blank=True)
    ip = models.CharField(max_length=80, verbose_name = 'Ip', null=True, blank=True)
    status = models.CharField(max_length=50, verbose_name = 'Status', null=True, blank=True)
    is_alive = models.CharField(max_length=50, verbose_name = 'Is alive', null=True, blank=True)
    last_update = models.DateTimeField(verbose_name = 'Last update')

    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    created = models.DateTimeField(verbose_name = 'Fecha creacion', default = now)
    class Meta:
        verbose_name = 'SitioB'
        verbose_name_plural = 'SitiosB'
        ordering = ['-created']

    def __str__(self):
        return str(self.sitio) + " " + '(' +str(self.ip) + ')'




class ConfigB(models.Model):
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

    #ChannelB = models.IntegerField(verbose_name='ChannelB', null=False, blank=False, default=0)
    #TypeEncode = models.IntegerField(verbose_name='TypeEncode', null=False, blank=False, default=0)
    #TypeStreamB = models.CharField(max_length=100, verbose_name = 'TypeStreamB', null=False, blank=False, default="MainFormat")

    created = models.DateTimeField(verbose_name = 'Fecha creacion', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    #sitio_id = models.ForeignKey(SitioB, verbose_name = 'SitioB', related_name='get_config', on_delete = models.CASCADE)
    class Meta:
        verbose_name = 'ConfigB'
        verbose_name_plural = 'ConfigsB'
        ordering = ['-created']

    def __str__(self):
        return str(self.id) + " " + str(self.resolution) + " " + str(self.FPS) + " " + str(self.BitRate) 


class StreamB(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    name = models.CharField(max_length=100, verbose_name = 'Name', null=False, blank=False)
    created = models.DateTimeField(verbose_name = 'Fecha creacion', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    id_config = models.ForeignKey(ConfigB, verbose_name = 'ConfigB', related_name='get_stream', on_delete = models.CASCADE)
    class Meta:
        verbose_name = 'StreamB'
        verbose_name_plural = 'StreamsB'
        ordering = ['-created']

    def __str__(self):
        return str(self.id)+" "+str(self.name)+" "+str(self.id_config)

class ChannelB(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    number = models.IntegerField(verbose_name='Number', null=False, blank=False)
    created = models.DateTimeField(verbose_name = 'Fecha creacion', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    #id_config = models.ForeignKey(ConfigB, verbose_name = 'ConfigB', related_name='get_channel', on_delete = models.CASCADE)
    #id_config = models.ForeignKey(ConfigB, verbose_name = 'ConfigB', related_name='get_channel', on_delete = models.CASCADE)
    sitio = models.ForeignKey(SitioB, verbose_name = 'SitioB', related_name='get_channel', on_delete = models.CASCADE)
    #sitios = models.ManyToManyField(SitioB,verbose_name = 'SitioBs')
    streams = models.ManyToManyField(StreamB,verbose_name = 'StreamsB')
    class Meta:
        verbose_name = 'ChannelB'
        verbose_name_plural = 'ChannelB'
        ordering = ['-created']

    def __str__(self):
        return str(self.number)+" "+ str(self.sitio)

