"""
Entidad Producto - Lógica de negocio pura sin dependencias de Django
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from ..value_objects import ProductCode, NIT
from ..exceptions import ValidationError


@dataclass
class Producto:
    """
    Entidad de negocio: Producto
    
    Reglas de negocio:
    - Código único e inmutable
    - Nombre requerido (mínimo 2 caracteres)
    - Debe estar asociado a una empresa
    - Características opcionales
    """
    codigo: ProductCode
    nombre: str
    empresa_nit: NIT
    caracteristicas: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by_id: Optional[str] = None
    
    def __post_init__(self):
        """Validar entidad al crear"""
        self.validate()
    
    def validate(self) -> None:
        """Validar reglas de negocio"""
        if not self.nombre or len(self.nombre.strip()) < 2:
            raise ValidationError("Nombre de producto debe tener al menos 2 caracteres")
        
        # Normalizar nombre
        self.nombre = self.nombre.strip()
        
        if self.caracteristicas:
            self.caracteristicas = self.caracteristicas.strip()
    
    def update_info(self, nombre: Optional[str] = None,
                    caracteristicas: Optional[str] = None,
                    empresa_nit: Optional[NIT] = None) -> None:
        """
        Actualizar información del producto
        
        Regla de negocio: Al actualizar, validar y actualizar timestamp
        """
        if nombre is not None:
            self.nombre = nombre
        
        if caracteristicas is not None:
            self.caracteristicas = caracteristicas
        
        if empresa_nit is not None:
            self.empresa_nit = empresa_nit
        
        self.updated_at = datetime.now()
        self.validate()
    
    def change_empresa(self, new_empresa_nit: NIT) -> None:
        """
        Regla de negocio: Cambiar la empresa del producto
        """
        self.empresa_nit = new_empresa_nit
        self.updated_at = datetime.now()
    
    def has_caracteristicas(self) -> bool:
        """Verificar si tiene características definidas"""
        return self.caracteristicas is not None and len(self.caracteristicas) > 0
    
    def to_dict(self) -> dict:
        """Convertir a diccionario para serialización"""
        return {
            'codigo': str(self.codigo),
            'nombre': self.nombre,
            'empresa_nit': str(self.empresa_nit),
            'caracteristicas': self.caracteristicas,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'created_by_id': self.created_by_id
        }
    
    def __str__(self) -> str:
        return f"Producto({self.nombre} - {self.codigo})"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Producto):
            return self.codigo == other.codigo
        return False
    
    def __hash__(self) -> int:
        return hash(self.codigo)
