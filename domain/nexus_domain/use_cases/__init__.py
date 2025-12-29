"""
Casos de uso del dominio NEXUS
"""
from .empresa_use_cases import (
    CreateEmpresaUseCase,
    GetEmpresaUseCase,
    ListEmpresasUseCase,
    UpdateEmpresaUseCase,
    DeleteEmpresaUseCase
)

from .producto_use_cases import (
    CreateProductoUseCase,
    GetProductoUseCase,
    ListProductosUseCase,
    UpdateProductoUseCase,
    DeleteProductoUseCase
)

from .inventario_use_cases import (
    CreateOrUpdateInventarioUseCase,
    GetInventarioUseCase,
    AddStockUseCase,
    RemoveStockUseCase,
    DeleteInventarioUseCase,
    GetLowStockItemsUseCase
)

__all__ = [
    # Empresa
    'CreateEmpresaUseCase',
    'GetEmpresaUseCase',
    'ListEmpresasUseCase',
    'UpdateEmpresaUseCase',
    'DeleteEmpresaUseCase',
    # Producto
    'CreateProductoUseCase',
    'GetProductoUseCase',
    'ListProductosUseCase',
    'UpdateProductoUseCase',
    'DeleteProductoUseCase',
    # Inventario
    'CreateOrUpdateInventarioUseCase',
    'GetInventarioUseCase',
    'AddStockUseCase',
    'RemoveStockUseCase',
    'DeleteInventarioUseCase',
    'GetLowStockItemsUseCase'
]
