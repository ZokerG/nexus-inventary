"""
Entidad Empresa - Lógica de negocio pura sin dependencias de Django
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from ..value_objects import NIT, Phone
from ..exceptions import ValidationError


@dataclass
class Empresa:
    """
    Entidad de negocio: Empresa
    
    Reglas de negocio:
    - NIT único e inmutable
    - Nombre requerido (mínimo 3 caracteres)
    - Dirección requerida
    - Teléfono válido
    """
    nit: NIT
    nombre: str
    direccion: str
    telefono: Phone
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by_id: Optional[str] = None
    
    def __post_init__(self):
        """Validar entidad al crear"""
        self.validate()
    
    def validate(self) -> None:
        """Validar reglas de negocio"""
        if not self.nombre or len(self.nombre.strip()) < 3:
            raise ValidationError("Nombre de empresa debe tener al menos 3 caracteres")
        
        if not self.direccion or len(self.direccion.strip()) < 5:
            raise ValidationError("Dirección debe tener al menos 5 caracteres")
        
        # Normalizar nombre
        self.nombre = self.nombre.strip()
        self.direccion = self.direccion.strip()
    
    def update_info(self, nombre: Optional[str] = None, 
                    direccion: Optional[str] = None, 
                    telefono: Optional[Phone] = None) -> None:
        """
        Actualizar información de la empresa
        
        Regla de negocio: Al actualizar, validar y actualizar timestamp
        """
        if nombre is not None:
            self.nombre = nombre
        
        if direccion is not None:
            self.direccion = direccion
        
        if telefono is not None:
            self.telefono = telefono
        
        self.updated_at = datetime.now()
        self.validate()
    
    def can_be_deleted(self) -> bool:
        """
        Regla de negocio: Verificar si la empresa puede ser eliminada
        Por ahora siempre True, pero puede incluir lógica adicional
        """
        return True
    
    def to_dict(self) -> dict:
        """Convertir a diccionario para serialización"""
        return {
            'nit': str(self.nit),
            'nombre': self.nombre,
            'direccion': self.direccion,
            'telefono': str(self.telefono),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'created_by_id': self.created_by_id
        }
    
    def __str__(self) -> str:
        return f"Empresa({self.nombre} - {self.nit})"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Empresa):
            return self.nit == other.nit
        return False
    
    def __hash__(self) -> int:
        return hash(self.nit)
