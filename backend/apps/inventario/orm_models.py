from django.db import models
from apps.empresas.models import Empresa
from apps.productos.models import Producto


class Inventario(models.Model):
    """
    Modelo para gestionar inventario (productos por empresa)
    """
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='inventario')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='inventario')
    cantidad = models.IntegerField(default=0, verbose_name='Cantidad en stock')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        unique_together = ('empresa', 'producto')
        ordering = ['-fecha_registro']
    
    def __str__(self):
        return f"{self.empresa.nombre} - {self.producto.nombre} ({self.cantidad})"
