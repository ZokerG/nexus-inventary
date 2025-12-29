"""
Value Objects - Objetos de valor inmutables con validaciones
"""
from dataclasses import dataclass
import re
from ..exceptions import ValidationError


@dataclass(frozen=True)
class NIT:
    """Value Object para NIT - Inmutable"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValidationError("NIT no puede estar vacío")
        
        if len(self.value) < 5:
            raise ValidationError("NIT debe tener al menos 5 caracteres")
        
        # Validación básica de formato (números o números con guión)
        if not re.match(r'^[\d\-]+$', self.value):
            raise ValidationError("NIT debe contener solo números y guiones")
    
    def __str__(self) -> str:
        return self.value
    
    def __eq__(self, other) -> bool:
        if isinstance(other, NIT):
            return self.value == other.value
        return False
    
    def __hash__(self) -> int:
        return hash(self.value)


@dataclass(frozen=True)
class Email:
    """Value Object para Email - Inmutable"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValidationError("Email no puede estar vacío")
        
        # Validación básica de email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, self.value):
            raise ValidationError(f"Email inválido: {self.value}")
    
    def __str__(self) -> str:
        return self.value
    
    def domain(self) -> str:
        """Obtener dominio del email"""
        return self.value.split('@')[1]


@dataclass(frozen=True)
class Phone:
    """Value Object para Teléfono - Inmutable"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValidationError("Teléfono no puede estar vacío")
        
        # Eliminar espacios y guiones para validación
        clean_phone = self.value.replace(' ', '').replace('-', '')
        
        if not clean_phone.isdigit():
            raise ValidationError("Teléfono debe contener solo números")
        
        if len(clean_phone) < 7 or len(clean_phone) > 15:
            raise ValidationError("Teléfono debe tener entre 7 y 15 dígitos")
    
    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class ProductCode:
    """Value Object para Código de Producto - Inmutable"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValidationError("Código de producto no puede estar vacío")
        
        if len(self.value) < 3:
            raise ValidationError("Código debe tener al menos 3 caracteres")
        
        # Validación: alfanumérico con guiones/underscores
        if not re.match(r'^[a-zA-Z0-9_-]+$', self.value):
            raise ValidationError("Código debe ser alfanumérico")
    
    def __str__(self) -> str:
        return self.value
    
    def __eq__(self, other) -> bool:
        if isinstance(other, ProductCode):
            return self.value.upper() == other.value.upper()
        return False
    
    def __hash__(self) -> int:
        return hash(self.value.upper())


@dataclass(frozen=True)
class Quantity:
    """Value Object para Cantidad de Inventario - Inmutable"""
    value: int
    
    def __post_init__(self):
        if self.value < 0:
            raise ValidationError("Cantidad no puede ser negativa")
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __int__(self) -> int:
        return self.value
    
    def add(self, other: 'Quantity') -> 'Quantity':
        """Sumar cantidades"""
        return Quantity(self.value + other.value)
    
    def subtract(self, other: 'Quantity') -> 'Quantity':
        """Restar cantidades"""
        result = self.value - other.value
        if result < 0:
            raise ValidationError("La resta resultaría en cantidad negativa")
        return Quantity(result)
    
    def is_sufficient(self, required: 'Quantity') -> bool:
        """Verificar si la cantidad es suficiente"""
        return self.value >= required.value
