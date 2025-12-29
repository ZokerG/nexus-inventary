"""
Implementación Django de los repositorios de dominio para Productos
"""
from typing import List, Optional
from django.contrib.auth import get_user_model
from nexus_domain.interfaces import IProductoRepository
from nexus_domain.entities import Producto as ProductoEntity
from nexus_domain.value_objects import ProductCode, NIT
from .orm_models import Producto as ProductoORM
from apps.empresas.orm_models import Empresa as EmpresaORM
from .mappers import ProductoMapper

User = get_user_model()


class DjangoProductoRepository(IProductoRepository):
    """Implementación Django del repositorio de productos"""
    
    def save(self, producto: ProductoEntity) -> ProductoEntity:
        """Guardar o actualizar producto"""
        try:
            # Intentar obtener registro existente
            orm_obj = ProductoORM.objects.get(codigo=str(producto.codigo))
            orm_obj = ProductoMapper.to_orm(producto, orm_obj)
        except ProductoORM.DoesNotExist:
            # Crear nuevo registro
            orm_obj = ProductoMapper.to_orm(producto)
        
        # Asignar empresa
        try:
            orm_obj.empresa = EmpresaORM.objects.get(nit=str(producto.empresa_nit))
        except EmpresaORM.DoesNotExist:
            raise ValueError(f"Empresa con NIT {producto.empresa_nit} no encontrada")
        
        # Asignar created_by si existe
        if producto.created_by_id:
            try:
                orm_obj.created_by = User.objects.get(id=int(producto.created_by_id))
            except (User.DoesNotExist, ValueError):
                pass
        
        orm_obj.save()
        return ProductoMapper.to_entity(orm_obj)
    
    def find_by_codigo(self, codigo: ProductCode) -> Optional[ProductoEntity]:
        """Buscar producto por código"""
        try:
            orm_obj = ProductoORM.objects.select_related('empresa').get(codigo=str(codigo))
            return ProductoMapper.to_entity(orm_obj)
        except ProductoORM.DoesNotExist:
            return None
    
    def find_all(self, limit: int = 100, offset: int = 0) -> List[ProductoEntity]:
        """Obtener todos los productos con paginación"""
        queryset = ProductoORM.objects.select_related('empresa').all()[offset:offset + limit]
        return [ProductoMapper.to_entity(orm_obj) for orm_obj in queryset]
    
    def find_by_empresa(self, empresa_nit: NIT) -> List[ProductoEntity]:
        """Buscar productos por empresa"""
        queryset = ProductoORM.objects.select_related('empresa').filter(
            empresa__nit=str(empresa_nit)
        )
        return [ProductoMapper.to_entity(orm_obj) for orm_obj in queryset]
    
    def search_by_nombre(self, nombre: str) -> List[ProductoEntity]:
        """Buscar productos por nombre (búsqueda parcial)"""
        queryset = ProductoORM.objects.select_related('empresa').filter(
            nombre__icontains=nombre
        )
        return [ProductoMapper.to_entity(orm_obj) for orm_obj in queryset]
    
    def delete(self, codigo: ProductCode) -> bool:
        """Eliminar producto por código"""
        try:
            orm_obj = ProductoORM.objects.get(codigo=str(codigo))
            orm_obj.delete()
            return True
        except ProductoORM.DoesNotExist:
            return False
    
    def exists(self, codigo: str) -> bool:
        """Verificar si existe producto con el código dado"""
        return ProductoORM.objects.filter(codigo=codigo).exists()
