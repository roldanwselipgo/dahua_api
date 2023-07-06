from django.contrib import admin

# Register your models here.
from .models import Mikrotik,Connection
# Register your models here.


class MikrotikAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)


class ConnectionAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

admin.site.register(Connection,ConnectionAdmin)
admin.site.register(Mikrotik,MikrotikAdmin)
