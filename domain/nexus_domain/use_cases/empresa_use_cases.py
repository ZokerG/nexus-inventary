"""
Casos de uso para Empresa - Lógica de aplicación
"""
from typing import List, Optional
from datetime import datetime
from ..entities import Empresa
from ..value_objects import NIT, Phone
from ..interfaces import IEmpresaRepository
from ..exceptions import (
    ValidationError, 
    EntityNotFoundError, 
    DuplicateEntityError,
    BusinessRuleViolationError
)


class CreateEmpresaUseCase:
    """Caso de uso: Crear empresa"""
    
    def __init__(self, repository: IEmpresaRepository):
        self.repository = repository
    
    def execute(self, nit: str, nombre: str, direccion: str, 
                telefono: str, user_id: str) -> Empresa:
        """
        Ejecutar caso de uso: Crear empresa
        
        Reglas:
        - NIT único (no duplicado)
        - Datos válidos según entidad
        """
        # Validar que no exista
        if self.repository.exists(nit):
            raise DuplicateEntityError(f"Empresa con NIT {nit} ya existe")
        
        # Crear entidad de dominio
        empresa = Empresa(
            nit=NIT(nit),
            nombre=nombre,
            direccion=direccion,
            telefono=Phone(telefono),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by_id=user_id
        )
        
        # Persistir
        return self.repository.save(empresa)


class GetEmpresaUseCase:
    """Caso de uso: Obtener empresa por NIT"""
    
    def __init__(self, repository: IEmpresaRepository):
        self.repository = repository
    
    def execute(self, nit: str) -> Empresa:
        """Ejecutar caso de uso: Obtener empresa"""
        empresa = self.repository.find_by_nit(nit)
        
        if not empresa:
            raise EntityNotFoundError(f"Empresa con NIT {nit} no encontrada")
        
        return empresa


class ListEmpresasUseCase:
    """Caso de uso: Listar empresas"""
    
    def __init__(self, repository: IEmpresaRepository):
        self.repository = repository
    
    def execute(self, limit: int = 100, offset: int = 0, 
                search: Optional[str] = None) -> List[Empresa]:
        """Ejecutar caso de uso: Listar empresas"""
        if search:
            return self.repository.search_by_nombre(search)
        
        return self.repository.find_all(limit=limit, offset=offset)


class UpdateEmpresaUseCase:
    """Caso de uso: Actualizar empresa"""
    
    def __init__(self, repository: IEmpresaRepository):
        self.repository = repository
    
    def execute(self, nit: str, nombre: Optional[str] = None,
                direccion: Optional[str] = None,
                telefono: Optional[str] = None) -> Empresa:
        """Ejecutar caso de uso: Actualizar empresa"""
        # Buscar empresa existente
        empresa = self.repository.find_by_nit(nit)
        if not empresa:
            raise EntityNotFoundError(f"Empresa con NIT {nit} no encontrada")
        
        # Actualizar información usando método de dominio
        telefono_vo = Phone(telefono) if telefono else None
        empresa.update_info(nombre=nombre, direccion=direccion, telefono=telefono_vo)
        
        # Persistir cambios
        return self.repository.save(empresa)


class DeleteEmpresaUseCase:
    """Caso de uso: Eliminar empresa"""
    
    def __init__(self, repository: IEmpresaRepository):
        self.repository = repository
    
    def execute(self, nit: str) -> bool:
        """
        Ejecutar caso de uso: Eliminar empresa
        
        Regla: Verificar si puede ser eliminada según lógica de negocio
        """
        # Buscar empresa
        empresa = self.repository.find_by_nit(nit)
        if not empresa:
            raise EntityNotFoundError(f"Empresa con NIT {nit} no encontrada")
        
        # Verificar regla de negocio
        if not empresa.can_be_deleted():
            raise BusinessRuleViolationError(
                "La empresa no puede ser eliminada (tiene dependencias)"
            )
        
        # Eliminar
        return self.repository.delete(nit)
