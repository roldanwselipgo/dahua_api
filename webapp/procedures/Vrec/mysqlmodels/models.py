# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Camara(models.Model):
    sucursal = models.IntegerField(primary_key=True)
    camara = models.IntegerField()
    nombre = models.CharField(max_length=120, blank=True, null=True)
    host = models.CharField(max_length=15, blank=True, null=True)
    port = models.IntegerField(blank=True, null=True)
    sdk = models.CharField(max_length=120, blank=True, null=True)
    user = models.CharField(max_length=45, blank=True, null=True)
    password = models.CharField(max_length=45, blank=True, null=True)
    fps = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)
    enable = models.CharField(max_length=45, blank=True, null=True)
    recycle_mode = models.CharField(max_length=45, blank=True, null=True)
    recycle_status = models.CharField(max_length=45, blank=True, null=True)
    first_video = models.DateTimeField(blank=True, null=True)
    last_video = models.DateTimeField(blank=True, null=True)
    last_update = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'camara'
        unique_together = (('sucursal', 'camara'),)


class CamaraVideoLost(models.Model):
    sucursal = models.IntegerField()
    camara = models.IntegerField()
    segmento_inicio = models.DateTimeField(blank=True, null=True)
    segmento_fin = models.DateTimeField(blank=True, null=True)
    tiempo_total = models.FloatField(blank=True, null=True)
    last_update = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'camara_video_lost'


class CamarasPrv(models.Model):
    sucursal = models.IntegerField(primary_key=True)
    c1 = models.CharField(max_length=16, blank=True, null=True)
    c2 = models.CharField(max_length=16, blank=True, null=True)
    c3 = models.CharField(max_length=16, blank=True, null=True)
    c4 = models.CharField(max_length=16, blank=True, null=True)
    c5 = models.CharField(max_length=16, blank=True, null=True)
    c6 = models.CharField(max_length=16, blank=True, null=True)
    c7 = models.CharField(max_length=16, blank=True, null=True)
    c8 = models.CharField(max_length=16, blank=True, null=True)
    c9 = models.CharField(max_length=16, blank=True, null=True)
    c10 = models.CharField(max_length=16, blank=True, null=True)
    c11 = models.CharField(max_length=16, blank=True, null=True)
    c12 = models.CharField(max_length=16, blank=True, null=True)
    c13 = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'camaras_prv'


class Direccionamiento(models.Model):
    sucursal = models.IntegerField(primary_key=True)
    gateway = models.CharField(max_length=16, blank=True, null=True)
    xvr = models.CharField(max_length=120, blank=True, null=True)
    xvr_port = models.IntegerField(blank=True, null=True)
    xvr_user = models.CharField(max_length=45, blank=True, null=True)
    xvr_password = models.CharField(max_length=45, blank=True, null=True)
    alarma = models.CharField(max_length=16, blank=True, null=True)
    control_acceso = models.CharField(max_length=16, blank=True, null=True)
    syncroback = models.CharField(max_length=16, blank=True, null=True)
    switch = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'direccionamiento'


class DireccionamientoPrv(models.Model):
    id_sedena = models.CharField(primary_key=True, max_length=10)
    centro_costos = models.IntegerField(blank=True, null=True)
    sucursal = models.CharField(max_length=120, blank=True, null=True)
    gw = models.CharField(max_length=15, blank=True, null=True)
    xvr = models.CharField(max_length=15, blank=True, null=True)
    cam1 = models.CharField(max_length=15, blank=True, null=True)
    cam2 = models.CharField(max_length=15, blank=True, null=True)
    cam3 = models.CharField(max_length=15, blank=True, null=True)
    cam4 = models.CharField(max_length=15, blank=True, null=True)
    cam5 = models.CharField(max_length=15, blank=True, null=True)
    cam6 = models.CharField(max_length=15, blank=True, null=True)
    alarma = models.CharField(max_length=15, blank=True, null=True)
    control_acceso = models.CharField(max_length=15, blank=True, null=True)
    syncroback = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'direccionamiento_prv'


class Entregas(models.Model):
    centro_costos = models.IntegerField(primary_key=True)
    id_sedena = models.CharField(max_length=10, blank=True, null=True)
    sucursal = models.CharField(max_length=120, blank=True, null=True)
    semana = models.CharField(max_length=45, blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)
    dummy = models.CharField(max_length=45, blank=True, null=True)
    fecha1 = models.DateField(blank=True, null=True)
    fecha2 = models.DateField(blank=True, null=True)
    dummy2 = models.CharField(max_length=45, blank=True, null=True)
    nombre1 = models.CharField(max_length=45, blank=True, null=True)
    nombre2 = models.CharField(max_length=45, blank=True, null=True)
    nombre3 = models.CharField(max_length=45, blank=True, null=True)
    importe = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entregas'


class ProcessLog(models.Model):
    sucursal = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=45)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'process_log'
        unique_together = (('sucursal', 'timestamp', 'status'),)


class SbLogistica(models.Model):
    centro_costos = models.IntegerField(primary_key=True)
    id_sedena = models.CharField(max_length=12, blank=True, null=True)
    sucursal = models.CharField(max_length=120, blank=True, null=True)
    calle = models.CharField(max_length=120, blank=True, null=True)
    numero = models.CharField(max_length=45, blank=True, null=True)
    colonia = models.CharField(max_length=120, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    entre_calle = models.CharField(max_length=120, blank=True, null=True)
    y_calle = models.CharField(max_length=120, blank=True, null=True)
    municipio = models.CharField(max_length=120, blank=True, null=True)
    estado = models.CharField(max_length=45, blank=True, null=True)
    latitud = models.CharField(max_length=45, blank=True, null=True)
    longitud = models.CharField(max_length=45, blank=True, null=True)
    sb = models.CharField(max_length=45, blank=True, null=True)
    bloque = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sb_logistica'


class Status(models.Model):
    host = models.CharField(max_length=100, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'status'


class Sucursal(models.Model):
    sucursal = models.IntegerField(primary_key=True)
    sedena = models.CharField(max_length=45, blank=True, null=True)
    nombre = models.CharField(max_length=120, blank=True, null=True)
    fase = models.IntegerField(blank=True, null=True)
    implementacion = models.CharField(max_length=45, blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)
    lastupdate = models.DateTimeField(db_column='lastUpdate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sucursal'


class Syncroback(models.Model):
    centro_costos = models.IntegerField(primary_key=True)
    id_sedena = models.CharField(max_length=10, blank=True, null=True)
    sucursal = models.CharField(max_length=120, blank=True, null=True)
    enviado = models.CharField(max_length=15, blank=True, null=True)
    fecha_envio = models.DateTimeField(blank=True, null=True)
    no_serie = models.CharField(max_length=45, blank=True, null=True)
    observaciones = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'syncroback'
