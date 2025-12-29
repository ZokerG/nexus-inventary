"""
Mappers: Conversión entre entidades de dominio y modelos ORM de Django
"""
from typing import Optional
from nexus_domain.entities import Producto as ProductoEntity
from nexus_domain.value_objects import ProductCode, NIT
from .orm_models import Producto as ProductoORM


class ProductoMapper:
    """Mapper para convertir entre Producto (entity) y Producto (ORM)"""
    
    @staticmethod
    def to_entity(orm_obj: ProductoORM) -> ProductoEntity:
        """Convertir modelo ORM a entidad de dominio"""
        # Convertir caracteristicas dict a string JSON
        import json
        caracteristicas_str = json.dumps(orm_obj.caracteristicas) if orm_obj.caracteristicas else ""
        
        return ProductoEntity(
            codigo=ProductCode(orm_obj.codigo),
            nombre=orm_obj.nombre,
            empresa_nit=NIT(orm_obj.empresa.nit),
            caracteristicas=caracteristicas_str,
            created_at=orm_obj.created_at,
            updated_at=orm_obj.updated_at,
            created_by_id=str(orm_obj.created_by.id) if orm_obj.created_by else None
        )
    
    @staticmethod
    def to_orm(entity: ProductoEntity, orm_obj: Optional[ProductoORM] = None) -> ProductoORM:
        """Convertir entidad de dominio a modelo ORM"""
        import json
        
        if orm_obj is None:
            orm_obj = ProductoORM()
        
        orm_obj.codigo = str(entity.codigo)
        orm_obj.nombre = entity.nombre
        
        # Convertir caracteristicas string a dict
        try:
            orm_obj.caracteristicas = json.loads(entity.caracteristicas) if entity.caracteristicas else {}
        except json.JSONDecodeError:
            orm_obj.caracteristicas = {"descripcion": entity.caracteristicas}
        
        # empresa y created_by se manejan en el repositorio
        
        return orm_obj
