from django.contrib import admin

# Register your models here.


from .models import Servicio
# Register your models here.


class ServicioAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)





admin.site.register(Servicio,ServicioAdmin)
