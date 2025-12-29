"""
NEXUS Domain Layer - Clean Architecture

Capa de dominio pura sin dependencias de frameworks.
Contiene la lógica de negocio del sistema NEXUS.

Uso:
    from nexus_domain.entities import Empresa, Producto, Inventario
    from nexus_domain.use_cases import CreateEmpresaUseCase
    from nexus_domain.value_objects import NIT, Phone
    from nexus_domain.interfaces import IEmpresaRepository
"""

__version__ = "1.0.0"

from .entities import Empresa, Producto, Inventario
from .value_objects import NIT, Email, Phone, ProductCode, Quantity
from .interfaces import IEmpresaRepository, IProductoRepository, IInventarioRepository
from .exceptions import (
    DomainException,
    ValidationError,
    EntityNotFoundError,
    DuplicateEntityError,
    BusinessRuleViolationError,
    InsufficientStockError,
    UnauthorizedOperationError
)

__all__ = [
    # Entities
    'Empresa',
    'Producto',
    'Inventario',
    # Value Objects
    'NIT',
    'Email',
    'Phone',
    'ProductCode',
    'Quantity',
    # Interfaces
    'IEmpresaRepository',
    'IProductoRepository',
    'IInventarioRepository',
    # Exceptions
    'DomainException',
    'ValidationError',
    'EntityNotFoundError',
    'DuplicateEntityError',
    'BusinessRuleViolationError',
    'InsufficientStockError',
    'UnauthorizedOperationError',
]
