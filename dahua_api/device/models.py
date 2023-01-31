from django.db import models
from django.utils.timezone import now
from datetime import datetime
# Create your models here.

class Device(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    #no_local = models.IntegerField(verbose_name='LocalNo', null=False, blank=False)
    #machine_name = models.CharField(max_length=200, verbose_name = 'Machine name', null=True, blank=True)
    #machine_adress = models.CharField(max_length=200, verbose_name = 'Machine address', null=True, blank=True)
    usuario = models.CharField(max_length=200, verbose_name = 'Usuario', null=False, blank=False)
    password = models.CharField(max_length=200, verbose_name = 'Password', null=False, blank=False)
    ip = models.CharField(max_length=50, verbose_name = 'Servidor', null=False, blank=False)
    puerto = models.IntegerField(verbose_name='Puerto', null=False, blank=False)
    serial_no = models.CharField(max_length=200, verbose_name = 'Numero de serie', null=True, blank=True, default="0")
    deviceType = models.CharField(max_length=200, verbose_name = 'DeviceType', null=True, blank=True, default="0")
    status = models.CharField(max_length=50, verbose_name = 'Status', null=True, blank=True, default="0")
    last_update = models.DateTimeField(verbose_name = 'Last update', null=True, blank=True)
    
    created = models.DateTimeField(verbose_name = 'Fecha creacion', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    #default_config = models.ForeignKey(DefaultConfig, verbose_name = 'Configuracion de video', related_name='get_camera', on_delete = models.CASCADE)
    
    class Meta:
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'
        ordering = ['-created']

    def __str__(self):
        return str(self.created.date()) + " " + '(' +str(self.ip) + ')'




class DefaultConfig(models.Model):
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
    priority = models.IntegerField(verbose_name='Priority', null=True, blank=True, default=1)
    created = models.DateTimeField(verbose_name = 'Fecha creacion', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    #sitio_id = models.ForeignKey(Sitio, verbose_name = 'Sitio', related_name='get_config', on_delete = models.CASCADE)
    class Meta:
        verbose_name = 'DefaultConfig'
        verbose_name_plural = 'DefaultConfigs'
        ordering = ['-priority']

    def __str__(self):
        return str(self.id) + " " + str(self.resolution) + " " + str(self.FPS) + " " + str(self.BitRate) 