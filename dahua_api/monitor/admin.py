from django.contrib import admin

# Register your models here.
from .models import Camera
from .models import Config
# Register your models here.

class cameraAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

class ConfigAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)




admin.site.register(Camera,cameraAdmin)
admin.site.register(Config,ConfigAdmin)

