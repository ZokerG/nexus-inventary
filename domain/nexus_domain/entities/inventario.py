"""
Entidad Inventario - Lógica de negocio pura sin dependencias de Django
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from ..value_objects import NIT, ProductCode, Quantity
from ..exceptions import ValidationError, InsufficientStockError


@dataclass
class Inventario:
    """
    Entidad de negocio: Inventario
    
    Reglas de negocio:
    - Combinación única de empresa + producto
    - Cantidad siempre >= 0
    - Movimientos de stock deben validarse
    - No se puede retirar más de lo disponible
    """
    id: Optional[int]
    empresa_nit: NIT
    producto_codigo: ProductCode
    cantidad: Quantity
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validar entidad al crear"""
        self.validate()
    
    def validate(self) -> None:
        """Validar reglas de negocio"""
        # La validación de cantidad >= 0 ya está en Quantity
        pass
    
    def add_stock(self, quantity: Quantity) -> None:
        """
        Regla de negocio: Agregar stock al inventario
        """
        self.cantidad = self.cantidad.add(quantity)
        self.updated_at = datetime.now()
    
    def remove_stock(self, quantity: Quantity) -> None:
        """
        Regla de negocio: Retirar stock del inventario
        
        Raises:
            InsufficientStockError: Si no hay stock suficiente
        """
        if not self.cantidad.is_sufficient(quantity):
            raise InsufficientStockError(
                f"Stock insuficiente. Disponible: {self.cantidad}, Requerido: {quantity}"
            )
        
        self.cantidad = self.cantidad.subtract(quantity)
        self.updated_at = datetime.now()
    
    def update_stock(self, new_quantity: Quantity) -> None:
        """
        Regla de negocio: Actualizar stock directo
        """
        self.cantidad = new_quantity
        self.updated_at = datetime.now()
    
    def is_low_stock(self, threshold: int = 10) -> bool:
        """
        Regla de negocio: Verificar si el stock está bajo
        """
        return int(self.cantidad) < threshold
    
    def is_out_of_stock(self) -> bool:
        """
        Regla de negocio: Verificar si está agotado
        """
        return int(self.cantidad) == 0
    
    def can_fulfill_order(self, required_quantity: Quantity) -> bool:
        """
        Regla de negocio: Verificar si puede cumplir un pedido
        """
        return self.cantidad.is_sufficient(required_quantity)
    
    def get_stock_status(self) -> str:
        """
        Regla de negocio: Obtener estado del stock
        """
        qty = int(self.cantidad)
        if qty == 0:
            return "AGOTADO"
        elif qty < 10:
            return "BAJO"
        elif qty < 50:
            return "MEDIO"
        else:
            return "ALTO"
    
    def to_dict(self) -> dict:
        """Convertir a diccionario para serialización"""
        return {
            'id': self.id,
            'empresa_nit': str(self.empresa_nit),
            'producto_codigo': str(self.producto_codigo),
            'cantidad': int(self.cantidad),
            'stock_status': self.get_stock_status(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __str__(self) -> str:
        return f"Inventario({self.empresa_nit} - {self.producto_codigo}: {self.cantidad})"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Inventario):
            return (self.empresa_nit == other.empresa_nit and 
                    self.producto_codigo == other.producto_codigo)
        return False
    
    def __hash__(self) -> int:
        return hash((self.empresa_nit, self.producto_codigo))
