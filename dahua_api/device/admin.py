from django.contrib import admin
from .models import Device
from .models import DefaultConfig
# Register your models here.


class DeviceAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

class DefaultConfigAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)




admin.site.register(Device,DeviceAdmin)
admin.site.register(DefaultConfig,DefaultConfigAdmin)
