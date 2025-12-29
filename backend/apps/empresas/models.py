"""
Mantener compatibilidad con Django migrations
Re-exportar modelos desde orm_models
"""
from .orm_models import Empresa

__all__ = ['Empresa']
