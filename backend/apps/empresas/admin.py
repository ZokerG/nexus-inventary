from django.contrib import admin
from .models import Empresa


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nit', 'nombre', 'telefono', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('nit', 'nombre')
    readonly_fields = ('created_at', 'updated_at')
