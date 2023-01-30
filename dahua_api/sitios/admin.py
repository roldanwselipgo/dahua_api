from django.contrib import admin
from .models import Sitio, Config, Stream, Channel


class SitioAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

class ConfigAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

class StreamAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

class ChannelAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)


admin.site.register(Sitio,SitioAdmin)
admin.site.register(Config,ConfigAdmin)
admin.site.register(Stream,StreamAdmin)
admin.site.register(Channel,ChannelAdmin)