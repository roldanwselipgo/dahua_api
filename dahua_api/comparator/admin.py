from django.contrib import admin
from .models import SitioB, ConfigB, StreamB, ChannelB


class SitioBAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

class ConfigBAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

class StreamBAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

class ChannelBAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)


admin.site.register(SitioB,SitioBAdmin)
admin.site.register(ConfigB,ConfigBAdmin)
admin.site.register(StreamB,StreamBAdmin)
admin.site.register(ChannelB,ChannelBAdmin)