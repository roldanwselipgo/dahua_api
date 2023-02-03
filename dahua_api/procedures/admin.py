from django.contrib import admin
from .models import Procedure


class ProcedureAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

admin.site.register(Procedure,ProcedureAdmin)