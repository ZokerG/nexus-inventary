from django.contrib import admin
from .models import Producto, PrecioMoneda


class PrecioMonedaInline(admin.TabularInline):
    model = PrecioMoneda
    extra = 1


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'empresa', 'created_by', 'created_at')
    list_filter = ('empresa', 'created_at')
    search_fields = ('codigo', 'nombre')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [PrecioMonedaInline]


@admin.register(PrecioMoneda)
class PrecioMonedaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'moneda', 'precio', 'created_at')
    list_filter = ('moneda',)
    search_fields = ('producto__codigo', 'producto__nombre')
