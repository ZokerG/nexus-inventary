"""
Interfaces (contratos) para repositorios - Sin implementación
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities import Empresa, Producto, Inventario


class IEmpresaRepository(ABC):
    """
    Contrato para repositorio de empresas
    La implementación será en la capa de infraestructura
    """
    
    @abstractmethod
    def save(self, empresa: Empresa) -> Empresa:
        """Guardar o actualizar empresa"""
        pass
    
    @abstractmethod
    def find_by_nit(self, nit: str) -> Optional[Empresa]:
        """Buscar empresa por NIT"""
        pass
    
    @abstractmethod
    def find_all(self, limit: int = 100, offset: int = 0) -> List[Empresa]:
        """Listar todas las empresas con paginación"""
        pass
    
    @abstractmethod
    def search_by_nombre(self, nombre: str) -> List[Empresa]:
        """Buscar empresas por nombre (parcial)"""
        pass
    
    @abstractmethod
    def delete(self, nit: str) -> bool:
        """Eliminar empresa por NIT"""
        pass
    
    @abstractmethod
    def exists(self, nit: str) -> bool:
        """Verificar si existe una empresa"""
        pass


class IProductoRepository(ABC):
    """
    Contrato para repositorio de productos
    La implementación será en la capa de infraestructura
    """
    
    @abstractmethod
    def save(self, producto: Producto) -> Producto:
        """Guardar o actualizar producto"""
        pass
    
    @abstractmethod
    def find_by_codigo(self, codigo: str) -> Optional[Producto]:
        """Buscar producto por código"""
        pass
    
    @abstractmethod
    def find_all(self, limit: int = 100, offset: int = 0) -> List[Producto]:
        """Listar todos los productos con paginación"""
        pass
    
    @abstractmethod
    def find_by_empresa(self, empresa_nit: str) -> List[Producto]:
        """Buscar productos de una empresa"""
        pass
    
    @abstractmethod
    def search_by_nombre(self, nombre: str) -> List[Producto]:
        """Buscar productos por nombre (parcial)"""
        pass
    
    @abstractmethod
    def delete(self, codigo: str) -> bool:
        """Eliminar producto por código"""
        pass
    
    @abstractmethod
    def exists(self, codigo: str) -> bool:
        """Verificar si existe un producto"""
        pass


class IInventarioRepository(ABC):
    """
    Contrato para repositorio de inventario
    La implementación será en la capa de infraestructura
    """
    
    @abstractmethod
    def save(self, inventario: Inventario) -> Inventario:
        """Guardar o actualizar inventario"""
        pass
    
    @abstractmethod
    def find_by_id(self, inventario_id: int) -> Optional[Inventario]:
        """Buscar inventario por ID"""
        pass
    
    @abstractmethod
    def find_by_empresa_and_producto(self, empresa_nit: str, 
                                     producto_codigo: str) -> Optional[Inventario]:
        """Buscar inventario por empresa y producto"""
        pass
    
    @abstractmethod
    def find_all(self, limit: int = 100, offset: int = 0) -> List[Inventario]:
        """Listar todo el inventario con paginación"""
        pass
    
    @abstractmethod
    def find_by_empresa(self, empresa_nit: str) -> List[Inventario]:
        """Buscar inventario de una empresa"""
        pass
    
    @abstractmethod
    def find_low_stock(self, threshold: int = 10) -> List[Inventario]:
        """Buscar items con stock bajo"""
        pass
    
    @abstractmethod
    def delete(self, inventario_id: int) -> bool:
        """Eliminar registro de inventario"""
        pass
    
    @abstractmethod
    def exists(self, empresa_nit: str, producto_codigo: str) -> bool:
        """Verificar si existe un registro de inventario"""
        pass
