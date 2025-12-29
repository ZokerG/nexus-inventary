"""
Mappers: Conversión entre entidades de dominio y modelos ORM de Django
"""
from typing import Optional
from nexus_domain.entities import Inventario as InventarioEntity
from nexus_domain.value_objects import NIT, ProductCode, Quantity
from .orm_models import Inventario as InventarioORM


class InventarioMapper:
    """Mapper para convertir entre Inventario (entity) y Inventario (ORM)"""
    
    @staticmethod
    def to_entity(orm_obj: InventarioORM) -> InventarioEntity:
        """Convertir modelo ORM a entidad de dominio"""
        return InventarioEntity(
            id=str(orm_obj.id),
            empresa_nit=NIT(orm_obj.empresa.nit),
            producto_codigo=ProductCode(orm_obj.producto.codigo),
            cantidad=Quantity(orm_obj.cantidad),
            created_at=orm_obj.fecha_registro,
            updated_at=orm_obj.updated_at
        )
    
    @staticmethod
    def to_orm(entity: InventarioEntity, orm_obj: Optional[InventarioORM] = None) -> InventarioORM:
        """Convertir entidad de dominio a modelo ORM"""
        if orm_obj is None:
            orm_obj = InventarioORM()
        
        # Solo actualizar cantidad, las FKs se manejan en el repositorio
        orm_obj.cantidad = int(entity.cantidad)
        
        return orm_obj
