from django.contrib import admin

# Register your models here.
from .models import Camera
from .models import VideoEncode
# Register your models here.

class cameraAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

class VideoEncodeAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)



admin.site.register(Camera,cameraAdmin)
admin.site.register(VideoEncode,VideoEncodeAdmin)
