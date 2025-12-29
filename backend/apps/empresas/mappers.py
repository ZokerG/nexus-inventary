"""
Mappers: Conversión entre entidades de dominio y modelos ORM de Django
"""
from typing import Optional
from nexus_domain.entities import Empresa as EmpresaEntity
from nexus_domain.value_objects import NIT, Phone
from .orm_models import Empresa as EmpresaORM


class EmpresaMapper:
    """Mapper para convertir entre Empresa (entity) y Empresa (ORM)"""
    
    @staticmethod
    def to_entity(orm_obj: EmpresaORM) -> EmpresaEntity:
        """Convertir modelo ORM a entidad de dominio"""
        return EmpresaEntity(
            nit=NIT(orm_obj.nit),
            nombre=orm_obj.nombre,
            direccion=orm_obj.direccion,
            telefono=Phone(orm_obj.telefono),
            created_at=orm_obj.created_at,
            updated_at=orm_obj.updated_at,
            created_by_id=str(orm_obj.created_by.id) if orm_obj.created_by else None
        )
    
    @staticmethod
    def to_orm(entity: EmpresaEntity, orm_obj: Optional[EmpresaORM] = None) -> EmpresaORM:
        """Convertir entidad de dominio a modelo ORM"""
        if orm_obj is None:
            orm_obj = EmpresaORM()
        
        orm_obj.nit = str(entity.nit)
        orm_obj.nombre = entity.nombre
        orm_obj.direccion = entity.direccion
        orm_obj.telefono = str(entity.telefono)
        
        # created_by se maneja por separado en el repositorio
        # porque requiere acceso al modelo User
        
        return orm_obj
