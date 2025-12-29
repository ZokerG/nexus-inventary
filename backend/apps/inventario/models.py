"""
Mantener compatibilidad con Django migrations
Re-exportar modelos desde orm_models
"""
from .orm_models import Inventario

__all__ = ['Inventario']
