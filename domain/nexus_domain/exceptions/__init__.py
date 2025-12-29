"""
Excepciones del dominio - Solo para errores de negocio
"""


class DomainException(Exception):
    """Excepción base del dominio"""
    pass


class ValidationError(DomainException):
    """Error de validación de reglas de negocio"""
    pass


class EntityNotFoundError(DomainException):
    """Entidad no encontrada"""
    pass


class DuplicateEntityError(DomainException):
    """Entidad duplicada"""
    pass


class BusinessRuleViolationError(DomainException):
    """Violación de regla de negocio"""
    pass


class InsufficientStockError(DomainException):
    """Stock insuficiente en inventario"""
    pass


class UnauthorizedOperationError(DomainException):
    """Operación no autorizada"""
    pass
