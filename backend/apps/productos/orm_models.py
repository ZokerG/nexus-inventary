from django.db import models
from django.contrib.auth import get_user_model
from apps.empresas.models import Empresa

User = get_user_model()


class Producto(models.Model):
    codigo = models.CharField(max_length=50, primary_key=True, verbose_name='Código')
    nombre = models.CharField(max_length=255, verbose_name='Nombre del producto')
    caracteristicas = models.JSONField(default=dict, verbose_name='Características')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='productos')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='productos_creados')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


class PrecioMoneda(models.Model):
    """
    Modelo para manejar precios en diferentes monedas
    """
    class Moneda(models.TextChoices):
        USD = 'USD', 'Dólar Estadounidense'
        EUR = 'EUR', 'Euro'
        COP = 'COP', 'Peso Colombiano'
        MXN = 'MXN', 'Peso Mexicano'
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='precios')
    moneda = models.CharField(max_length=3, choices=Moneda.choices, verbose_name='Moneda')
    precio = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Precio')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Precio por Moneda'
        verbose_name_plural = 'Precios por Moneda'
        unique_together = ('producto', 'moneda')
    
    def __str__(self):
        return f"{self.producto.codigo} - {self.precio} {self.moneda}"
