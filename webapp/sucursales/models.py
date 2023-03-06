from django.db import models
from django.utils.timezone import now
from datetime import datetime

# Create your models here.
class Sucursal(models.Model):
    sucursal = models.IntegerField(primary_key=True,verbose_name='Sucursal')
    nombre = models.CharField(max_length=20, verbose_name = 'Nombre', null=True, blank=True)
    fase = models.IntegerField(verbose_name='fase', null=True, blank=True)
    status = models.CharField(max_length=50, verbose_name = 'Status', null=True, blank=True)
    model = models.CharField(max_length=50, verbose_name = 'Model', null=True, blank=True)
    last_update = models.DateTimeField(verbose_name = 'Last update')
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    created = models.DateTimeField(verbose_name = 'Fecha creacion', default = now)
    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
        ordering = ['-created']

    def __str__(self):
        return str(self.sucursal) + " " + '(' +str(self.model) + ')'


class Camera(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    number = models.IntegerField(verbose_name='Number', null=False, blank=False)
    model = models.CharField(max_length=50, verbose_name = 'Model', null=True, blank=True)
    created = models.DateTimeField(verbose_name = 'Fecha creacion', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    #id_config = models.ForeignKey(Config, verbose_name = 'Config', related_name='get_channel', on_delete = models.CASCADE)
    #id_config = models.ForeignKey(Config, verbose_name = 'Config', related_name='get_channel', on_delete = models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, verbose_name = 'Sucursal', related_name='get_camera', on_delete = models.CASCADE)
    #sitios = models.ManyToManyField(Sitio,verbose_name = 'Sitios')
    class Meta:
        verbose_name = 'Camera'
        verbose_name_plural = 'Camera'
        ordering = ['-created']

    def __str__(self):
        return str(self.model)+" "+ str(self.id)

