from django.db import models
from django.utils.timezone import now
from datetime import datetime
# Create your models here.
class DNS(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    hostname = models.CharField(max_length=50, verbose_name = 'Hostname', null=False, blank=False)
    ip = models.CharField(max_length=50, verbose_name = 'Direccion ip', null=False, blank=False)
    created = models.DateTimeField(verbose_name = 'Fecha creacion', default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    class Meta:
        verbose_name = 'DNS'
        verbose_name_plural = 'DNSs'
        ordering = ['-created']

    def __str__(self):
        return str(self.created.date()) + " " + '(' +str(self.hostname) + ')'

