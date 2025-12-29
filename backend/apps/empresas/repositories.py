"""
Implementación Django de los repositorios de dominio
"""
from typing import List, Optional
from django.contrib.auth import get_user_model
from nexus_domain.interfaces import IEmpresaRepository
from nexus_domain.entities import Empresa as EmpresaEntity
from nexus_domain.value_objects import NIT
from .orm_models import Empresa as EmpresaORM
from .mappers import EmpresaMapper

User = get_user_model()


class DjangoEmpresaRepository(IEmpresaRepository):
    """Implementación Django del repositorio de empresas"""
    
    def save(self, empresa: EmpresaEntity) -> EmpresaEntity:
        """Guardar o actualizar empresa"""
        try:
            # Intentar obtener registro existente
            orm_obj = EmpresaORM.objects.get(nit=str(empresa.nit))
            orm_obj = EmpresaMapper.to_orm(empresa, orm_obj)
        except EmpresaORM.DoesNotExist:
            # Crear nuevo registro
            orm_obj = EmpresaMapper.to_orm(empresa)
        
        # Asignar created_by si existe
        if empresa.created_by_id:
            try:
                orm_obj.created_by = User.objects.get(id=int(empresa.created_by_id))
            except (User.DoesNotExist, ValueError):
                pass
        
        orm_obj.save()
        return EmpresaMapper.to_entity(orm_obj)
    
    def find_by_nit(self, nit: NIT) -> Optional[EmpresaEntity]:
        """Buscar empresa por NIT"""
        try:
            orm_obj = EmpresaORM.objects.get(nit=str(nit))
            return EmpresaMapper.to_entity(orm_obj)
        except EmpresaORM.DoesNotExist:
            return None
    
    def find_all(self, limit: int = 100, offset: int = 0) -> List[EmpresaEntity]:
        """Obtener todas las empresas con paginación"""
        queryset = EmpresaORM.objects.all()[offset:offset + limit]
        return [EmpresaMapper.to_entity(orm_obj) for orm_obj in queryset]
    
    def search_by_nombre(self, nombre: str) -> List[EmpresaEntity]:
        """Buscar empresas por nombre (búsqueda parcial)"""
        queryset = EmpresaORM.objects.filter(nombre__icontains=nombre)
        return [EmpresaMapper.to_entity(orm_obj) for orm_obj in queryset]
    
    def delete(self, nit: NIT) -> bool:
        """Eliminar empresa por NIT"""
        try:
            orm_obj = EmpresaORM.objects.get(nit=str(nit))
            orm_obj.delete()
            return True
        except EmpresaORM.DoesNotExist:
            return False
    
    def exists(self, nit: str) -> bool:
        """Verificar si existe empresa con el NIT dado"""
        return EmpresaORM.objects.filter(nit=nit).exists()
