from django.contrib import admin
from .models import DNS
# Register your models here.


class DNSAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)


admin.site.register(DNS,DNSAdmin)
