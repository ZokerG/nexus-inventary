"""
Casos de uso para Inventario - Lógica de aplicación
"""
from typing import List, Optional
from datetime import datetime
from ..entities import Inventario
from ..value_objects import NIT, ProductCode, Quantity
from ..interfaces import IInventarioRepository, IEmpresaRepository, IProductoRepository
from ..exceptions import (
    ValidationError,
    EntityNotFoundError,
    DuplicateEntityError,
    InsufficientStockError
)


class CreateOrUpdateInventarioUseCase:
    """Caso de uso: Crear o actualizar inventario"""
    
    def __init__(self, inventario_repository: IInventarioRepository,
                 empresa_repository: IEmpresaRepository,
                 producto_repository: IProductoRepository):
        self.inventario_repository = inventario_repository
        self.empresa_repository = empresa_repository
        self.producto_repository = producto_repository
    
    def execute(self, empresa_nit: str, producto_codigo: str, 
                cantidad: int) -> Inventario:
        """
        Ejecutar caso de uso: Crear o actualizar inventario
        
        Reglas:
        - Empresa debe existir
        - Producto debe existir
        - Si ya existe inventario, actualizar cantidad
        """
        # Validar empresa existe
        if not self.empresa_repository.exists(empresa_nit):
            raise EntityNotFoundError(f"Empresa con NIT {empresa_nit} no encontrada")
        
        # Validar producto existe
        if not self.producto_repository.exists(producto_codigo):
            raise EntityNotFoundError(f"Producto con código {producto_codigo} no encontrado")
        
        # Buscar inventario existente
        inventario = self.inventario_repository.find_by_empresa_and_producto(
            empresa_nit, producto_codigo
        )
        
        if inventario:
            # Actualizar cantidad existente
            inventario.update_stock(Quantity(cantidad))
        else:
            # Crear nuevo
            inventario = Inventario(
                id=None,
                empresa_nit=NIT(empresa_nit),
                producto_codigo=ProductCode(producto_codigo),
                cantidad=Quantity(cantidad),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        
        # Persistir
        return self.inventario_repository.save(inventario)


class GetInventarioUseCase:
    """Caso de uso: Obtener inventario"""
    
    def __init__(self, repository: IInventarioRepository):
        self.repository = repository
    
    def execute(self, empresa_nit: Optional[str] = None) -> List[Inventario]:
        """
        Ejecutar caso de uso: Obtener inventario
        
        Si empresa_nit es None, retorna todo el inventario
        """
        if empresa_nit:
            return self.repository.find_by_empresa(empresa_nit)
        
        return self.repository.find_all()


class AddStockUseCase:
    """Caso de uso: Agregar stock"""
    
    def __init__(self, repository: IInventarioRepository):
        self.repository = repository
    
    def execute(self, inventario_id: int, cantidad: int) -> Inventario:
        """
        Ejecutar caso de uso: Agregar stock
        
        Regla: Usar método de dominio add_stock
        """
        inventario = self.repository.find_by_id(inventario_id)
        if not inventario:
            raise EntityNotFoundError(f"Inventario con ID {inventario_id} no encontrado")
        
        # Usar método de dominio
        inventario.add_stock(Quantity(cantidad))
        
        # Persistir
        return self.repository.save(inventario)


class RemoveStockUseCase:
    """Caso de uso: Retirar stock"""
    
    def __init__(self, repository: IInventarioRepository):
        self.repository = repository
    
    def execute(self, inventario_id: int, cantidad: int) -> Inventario:
        """
        Ejecutar caso de uso: Retirar stock
        
        Regla: Usar método de dominio remove_stock (valida stock suficiente)
        """
        inventario = self.repository.find_by_id(inventario_id)
        if not inventario:
            raise EntityNotFoundError(f"Inventario con ID {inventario_id} no encontrado")
        
        # Usar método de dominio (puede lanzar InsufficientStockError)
        inventario.remove_stock(Quantity(cantidad))
        
        # Persistir
        return self.repository.save(inventario)


class DeleteInventarioUseCase:
    """Caso de uso: Eliminar registro de inventario"""
    
    def __init__(self, repository: IInventarioRepository):
        self.repository = repository
    
    def execute(self, inventario_id: int) -> bool:
        """Ejecutar caso de uso: Eliminar inventario"""
        inventario = self.repository.find_by_id(inventario_id)
        if not inventario:
            raise EntityNotFoundError(f"Inventario con ID {inventario_id} no encontrado")
        
        return self.repository.delete(inventario_id)


class GetLowStockItemsUseCase:
    """Caso de uso: Obtener items con stock bajo"""
    
    def __init__(self, repository: IInventarioRepository):
        self.repository = repository
    
    def execute(self, threshold: int = 10) -> List[Inventario]:
        """
        Ejecutar caso de uso: Obtener items con stock bajo
        
        Regla de negocio: threshold configurable
        """
        return self.repository.find_low_stock(threshold=threshold)
