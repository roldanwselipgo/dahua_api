from django.db import models
from django.utils.timezone import now
from datetime import datetime

class Procedure(models.Model):
    types = [
    ('every-hours', 'every-hours'),
    ('every-time', 'every-time'),
    ]
    id = models.AutoField(primary_key=True, verbose_name='id')
    name = models.CharField(max_length=100, verbose_name = 'name', null=False, blank=False)
    description = models.CharField(max_length=100, verbose_name = 'Description', null=True, blank=True)
    type = models.CharField(choices=types, max_length=50, verbose_name = 'type', null=True, blank=True, default="every-hours")
    value = models.IntegerField(verbose_name='value', null=True, blank=True)
    time = models.TimeField(verbose_name='time', null=True, blank=True)
    repeat = models.IntegerField(verbose_name='repeats per day', null=True, blank=True)
    priority = models.IntegerField(verbose_name='priority', null=True, blank=True)

    created = models.DateTimeField(verbose_name = 'Fecha creacion', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    class Meta:
        verbose_name = 'Procedure'
        verbose_name_plural = 'Procedure'
        ordering = ['-created']

    def __str__(self):
        return str(self.id) + " " + str(self.description) 