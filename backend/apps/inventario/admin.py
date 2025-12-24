from django.contrib import admin
from .models import Inventario


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'producto', 'cantidad', 'fecha_registro', 'updated_at')
    list_filter = ('empresa', 'fecha_registro')
    search_fields = ('empresa__nombre', 'producto__nombre', 'producto__codigo')
    readonly_fields = ('fecha_registro', 'updated_at')
