from django.contrib import admin
from .models import Sucursal

class SucursalAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

admin.site.register(Sucursal,SucursalAdmin)
