"""
Implementación Django de los repositorios de dominio para Inventario
"""
from typing import List, Optional
from nexus_domain.interfaces import IInventarioRepository
from nexus_domain.entities import Inventario as InventarioEntity
from nexus_domain.value_objects import NIT, ProductCode
from .orm_models import Inventario as InventarioORM
from apps.empresas.orm_models import Empresa as EmpresaORM
from apps.productos.orm_models import Producto as ProductoORM
from .mappers import InventarioMapper


class DjangoInventarioRepository(IInventarioRepository):
    """Implementación Django del repositorio de inventario"""
    
    def save(self, inventario: InventarioEntity) -> InventarioEntity:
        """Guardar o actualizar inventario"""
        # Obtener empresa y producto
        try:
            empresa = EmpresaORM.objects.get(nit=str(inventario.empresa_nit))
            producto = ProductoORM.objects.get(codigo=str(inventario.producto_codigo))
        except (EmpresaORM.DoesNotExist, ProductoORM.DoesNotExist) as e:
            raise ValueError(f"Empresa o producto no encontrado: {e}")
        
        # Intentar obtener registro existente
        if inventario.id and inventario.id != 'None':
            try:
                orm_obj = InventarioORM.objects.get(id=int(inventario.id))
                orm_obj = InventarioMapper.to_orm(inventario, orm_obj)
            except (InventarioORM.DoesNotExist, ValueError):
                # Si no existe por ID, buscar por empresa+producto
                orm_obj, created = InventarioORM.objects.get_or_create(
                    empresa=empresa,
                    producto=producto,
                    defaults={'cantidad': int(inventario.cantidad)}
                )
                if not created:
                    orm_obj = InventarioMapper.to_orm(inventario, orm_obj)
        else:
            # Buscar o crear por empresa+producto
            orm_obj, created = InventarioORM.objects.get_or_create(
                empresa=empresa,
                producto=producto,
                defaults={'cantidad': int(inventario.cantidad)}
            )
            if not created:
                orm_obj = InventarioMapper.to_orm(inventario, orm_obj)
        
        orm_obj.empresa = empresa
        orm_obj.producto = producto
        orm_obj.save()
        
        return InventarioMapper.to_entity(orm_obj)
    
    def find_by_id(self, inventario_id: str) -> Optional[InventarioEntity]:
        """Buscar inventario por ID"""
        try:
            orm_obj = InventarioORM.objects.select_related('empresa', 'producto').get(id=int(inventario_id))
            return InventarioMapper.to_entity(orm_obj)
        except (InventarioORM.DoesNotExist, ValueError):
            return None
    
    def find_by_empresa_and_producto(self, empresa_nit: NIT, producto_codigo: ProductCode) -> Optional[InventarioEntity]:
        """Buscar inventario por empresa y producto"""
        try:
            orm_obj = InventarioORM.objects.select_related('empresa', 'producto').get(
                empresa__nit=str(empresa_nit),
                producto__codigo=str(producto_codigo)
            )
            return InventarioMapper.to_entity(orm_obj)
        except InventarioORM.DoesNotExist:
            return None
    
    def find_all(self, limit: int = 100, offset: int = 0) -> List[InventarioEntity]:
        """Obtener todo el inventario con paginación"""
        queryset = InventarioORM.objects.select_related('empresa', 'producto').all()[offset:offset + limit]
        return [InventarioMapper.to_entity(orm_obj) for orm_obj in queryset]
    
    def find_by_empresa(self, empresa_nit: NIT) -> List[InventarioEntity]:
        """Buscar inventario por empresa"""
        queryset = InventarioORM.objects.select_related('empresa', 'producto').filter(
            empresa__nit=str(empresa_nit)
        )
        return [InventarioMapper.to_entity(orm_obj) for orm_obj in queryset]
    
    def find_low_stock(self, threshold: int = 10) -> List[InventarioEntity]:
        """Buscar items con stock bajo"""
        queryset = InventarioORM.objects.select_related('empresa', 'producto').filter(
            cantidad__lte=threshold
        )
        return [InventarioMapper.to_entity(orm_obj) for orm_obj in queryset]
    
    def delete(self, inventario_id: str) -> bool:
        """Eliminar inventario por ID"""
        try:
            orm_obj = InventarioORM.objects.get(id=int(inventario_id))
            orm_obj.delete()
            return True
        except (InventarioORM.DoesNotExist, ValueError):
            return False
    
    def exists(self, empresa_nit: str, producto_codigo: str) -> bool:
        """Verificar si existe inventario para empresa+producto"""
        return InventarioORM.objects.filter(
            empresa__nit=empresa_nit,
            producto__codigo=producto_codigo
        ).exists()
