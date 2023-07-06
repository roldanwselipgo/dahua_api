from django.db import models
from django.utils.timezone import now
from datetime import datetime
# Create your models here.



class Connection(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    ip = models.CharField(max_length=100, verbose_name = 'ip', null=False, blank=False)
    ssh_user = models.CharField(max_length=100, verbose_name = 'ssh user', null=False, blank=False)
    ssh_password = models.CharField(max_length=100, verbose_name = 'ssh password', null=True, blank=True)
    ftp_port = models.IntegerField(verbose_name = 'ftp port', null=True, blank=True, default="22")
    created = models.DateTimeField(verbose_name = 'Fecha creacion', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    class Meta:
        verbose_name = 'Connection'
        verbose_name_plural = 'Connection'
        ordering = ['-created']

    def __str__(self):
        return str(self.ip) + " " + str(self.ssh_user) 

class Mikrotik(models.Model):
    types = [
    ('tipo_A', 'tipo_A'),
    ('tipo_B', 'tipo_B'),
    ]
    proyecto = [
    ('MC', 'MC'),
    ('Otro', 'Otro'),
    ]
    id = models.AutoField(primary_key=True, verbose_name='id')
    mc = models.CharField(max_length=100, verbose_name = 'name', null=False, blank=False)
    proyecto = models.CharField(choices=proyecto,max_length=100, verbose_name = 'Proyecto', null=True, blank=True, default="MC")
    serie = models.CharField(max_length=50, verbose_name = 'type', null=True, blank=True, default="Null")
    type = models.CharField(choices=types, max_length=50, verbose_name = 'type', null=True, blank=True, default="tipo_A")
    p1 = models.IntegerField(verbose_name='p1', null=True, blank=True)
    p2 = models.IntegerField(verbose_name='p2', null=True, blank=True)
    p3 = models.IntegerField(verbose_name='p3', null=True, blank=True)
    p4 = models.IntegerField(verbose_name='p4', null=True, blank=True)
    p5 = models.IntegerField(verbose_name='p5', null=True, blank=True)
    p6 = models.IntegerField(verbose_name='p6', null=True, blank=True)
    p7 = models.IntegerField(verbose_name='p7', null=True, blank=True)
    p8 = models.IntegerField(verbose_name='p8', null=True, blank=True)
    id_connection = models.ForeignKey(Connection, verbose_name = 'Connection', related_name='get_mikrotik', on_delete = models.CASCADE, default=1)
    
    created = models.DateTimeField(verbose_name = 'Fecha creacion', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    class Meta:
        verbose_name = 'Mikrotik'
        verbose_name_plural = 'Mikrotik'
        ordering = ['-created']

    def __str__(self):
        return str(self.mc) + " " + str(self.proyecto) 
    

    '''class Rules(models.Model):
        types = [
        ('tipo_A', 'tipo_A'),
        ('tipo_B', 'tipo_B'),
        ]
        id = models.AutoField(primary_key=True, verbose_name='id')
        mc = models.CharField(max_length=100, verbose_name = 'name', null=False, blank=False)
        serie = models.CharField(max_length=50, verbose_name = 'type', null=True, blank=True, default="Null")
        type = models.CharField(choices=types, max_length=50, verbose_name = 'type', null=True, blank=True, default="tipo_A")
        value = models.IntegerField(verbose_name='value', null=True, blank=True)
        priority = models.IntegerField(verbose_name='priority', null=True, blank=True)
        status = models.CharField(max_length=50, verbose_name = 'status', null=True, blank=True, default="Null")

        created = models.DateTimeField(verbose_name = 'Fecha creacion', default = now)
        updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
        class Meta:
            verbose_name = 'Rules'
            verbose_name_plural = 'Rules'
            ordering = ['-created']

        def __str__(self):
            return str(self.id) + " " + str(self.proyecto)''' 