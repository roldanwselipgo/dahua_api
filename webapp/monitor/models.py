from django.db import models
from django.utils.timezone import now
from datetime import datetime
from sitios.models import Sitio, Config
# Create your models here.



"""

class Camera(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    #no_local = models.IntegerField(verbose_name='LocalNo', null=False, blank=False)
    #machine_name = models.CharField(max_length=200, verbose_name = 'Machine name', null=True, blank=True)
    #machine_adress = models.CharField(max_length=200, verbose_name = 'Machine address', null=True, blank=True)
    serial_no = models.CharField(max_length=200, verbose_name = 'Numero de serie', null=True, blank=True, default="0")
    usuario = models.CharField(max_length=200, verbose_name = 'Usuario', null=False, blank=False)
    password = models.CharField(max_length=200, verbose_name = 'Password', null=False, blank=False)
    ip = models.CharField(max_length=50, verbose_name = 'Servidor', null=False, blank=False)
    puerto = models.IntegerField(verbose_name='Puerto', null=False, blank=False, default=0)
    created = models.DateTimeField(verbose_name = 'Fecha creacion', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    videoencode_config_id = models.ForeignKey(Config, verbose_name = 'Configuracion de video', related_name='get_camera', on_delete = models.CASCADE)
    class Meta:
        verbose_name = 'Camera'
        verbose_name_plural = 'Cameras'
        ordering = ['-created']

    def __str__(self):
        return str(self.created.date()) + " " + '(' +str(self.ip) + ')'


"""

