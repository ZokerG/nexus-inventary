"""
Casos de uso para Producto - Lógica de aplicación
"""
from typing import List, Optional
from datetime import datetime
from ..entities import Producto
from ..value_objects import ProductCode, NIT
from ..interfaces import IProductoRepository, IEmpresaRepository
from ..exceptions import (
    ValidationError,
    EntityNotFoundError,
    DuplicateEntityError,
    BusinessRuleViolationError
)


class CreateProductoUseCase:
    """Caso de uso: Crear producto"""
    
    def __init__(self, producto_repository: IProductoRepository,
                 empresa_repository: IEmpresaRepository):
        self.producto_repository = producto_repository
        self.empresa_repository = empresa_repository
    
    def execute(self, codigo: str, nombre: str, empresa_nit: str,
                caracteristicas: Optional[str], user_id: str) -> Producto:
        """
        Ejecutar caso de uso: Crear producto
        
        Reglas:
        - Código único
        - Empresa debe existir
        """
        # Validar que no exista producto
        if self.producto_repository.exists(codigo):
            raise DuplicateEntityError(f"Producto con código {codigo} ya existe")
        
        # Validar que empresa exista
        if not self.empresa_repository.exists(empresa_nit):
            raise EntityNotFoundError(f"Empresa con NIT {empresa_nit} no encontrada")
        
        # Crear entidad de dominio
        producto = Producto(
            codigo=ProductCode(codigo),
            nombre=nombre,
            empresa_nit=NIT(empresa_nit),
            caracteristicas=caracteristicas,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by_id=user_id
        )
        
        # Persistir
        return self.producto_repository.save(producto)


class GetProductoUseCase:
    """Caso de uso: Obtener producto por código"""
    
    def __init__(self, repository: IProductoRepository):
        self.repository = repository
    
    def execute(self, codigo: str) -> Producto:
        """Ejecutar caso de uso: Obtener producto"""
        producto = self.repository.find_by_codigo(codigo)
        
        if not producto:
            raise EntityNotFoundError(f"Producto con código {codigo} no encontrado")
        
        return producto


class ListProductosUseCase:
    """Caso de uso: Listar productos"""
    
    def __init__(self, repository: IProductoRepository):
        self.repository = repository
    
    def execute(self, limit: int = 100, offset: int = 0,
                empresa_nit: Optional[str] = None,
                search: Optional[str] = None) -> List[Producto]:
        """Ejecutar caso de uso: Listar productos"""
        if empresa_nit:
            return self.repository.find_by_empresa(empresa_nit)
        
        if search:
            return self.repository.search_by_nombre(search)
        
        return self.repository.find_all(limit=limit, offset=offset)


class UpdateProductoUseCase:
    """Caso de uso: Actualizar producto"""
    
    def __init__(self, repository: IProductoRepository):
        self.repository = repository
    
    def execute(self, codigo: str, nombre: Optional[str] = None,
                caracteristicas: Optional[str] = None) -> Producto:
        """Ejecutar caso de uso: Actualizar producto"""
        # Buscar producto existente
        producto = self.repository.find_by_codigo(codigo)
        if not producto:
            raise EntityNotFoundError(f"Producto con código {codigo} no encontrado")
        
        # Actualizar usando método de dominio
        producto.update_info(nombre=nombre, caracteristicas=caracteristicas)
        
        # Persistir cambios
        return self.repository.save(producto)


class DeleteProductoUseCase:
    """Caso de uso: Eliminar producto"""
    
    def __init__(self, repository: IProductoRepository):
        self.repository = repository
    
    def execute(self, codigo: str) -> bool:
        """Ejecutar caso de uso: Eliminar producto"""
        # Buscar producto
        producto = self.repository.find_by_codigo(codigo)
        if not producto:
            raise EntityNotFoundError(f"Producto con código {codigo} no encontrado")
        
        # Eliminar
        return self.repository.delete(codigo)
