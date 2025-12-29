from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Empresa(models.Model):
    """
    Modelo para gestionar empresas
    """
    nit = models.CharField(max_length=20, primary_key=True, verbose_name='NIT')
    nombre = models.CharField(max_length=255, verbose_name='Nombre de la empresa')
    direccion = models.TextField(verbose_name='Dirección')
    telefono = models.CharField(max_length=20, verbose_name='Teléfono')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='empresas_creadas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.nombre} ({self.nit})"
