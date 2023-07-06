from django.db import models
from django.utils.timezone import now
from datetime import datetime

# Create your models here.
class Servicio(models.Model):
    servicio = models.AutoField(primary_key=True,verbose_name='Servicio')
    nombre = models.CharField(max_length=50, verbose_name = 'Nombre', null=True, blank=True)
    descripcion = models.CharField(max_length=200, verbose_name = 'Descripcion', null=True, blank=True)
    tiempo_de_toleracia = models.IntegerField(verbose_name = 'Tiempo de tolerancia', null=True, blank=True)
    servidor = models.CharField(max_length=50, verbose_name = 'Servidor', null=True, blank=True)
    puerto = models.CharField(max_length=50, verbose_name = 'Puerto', null=True, blank=True)
    bd = models.CharField(max_length=50, verbose_name = 'BD', null=True, blank=True)
    tabla = models.CharField(max_length=50, verbose_name = 'Tabla', null=True, blank=True)
    columna = models.CharField(max_length=50, verbose_name = 'Columna', null=True, blank=True)
    usuario = models.CharField(max_length=50, verbose_name = 'Usuario', null=True, blank=True, default="Null")
    password = models.CharField(max_length=50, verbose_name = 'Password', null=True, blank=True, default="Null")
    status = models.CharField(max_length=50, verbose_name = 'Status', null=True, blank=True, default="Null")
    ultima_vez_activo = models.CharField(max_length=50, verbose_name = 'Ultima vez activo', null=True, blank=True, default="Null")
    #last_update = models.DateTimeField(verbose_name = 'Last update')

    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    created = models.DateTimeField(verbose_name = 'Fecha creacion', default = now)
    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['-created']

    def __str__(self):
        return str(self.servicio) + " " + '(' +str(self.descripcion) + ')'



