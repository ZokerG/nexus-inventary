"""
Configuración de pytest para el dominio
"""
import pytest


@pytest.fixture
def sample_nit():
    """Fixture para NIT de prueba"""
    return "900123456"


@pytest.fixture
def sample_email():
    """Fixture para email de prueba"""
    return "test@example.com"


@pytest.fixture
def sample_phone():
    """Fixture para teléfono de prueba"""
    return "3001234567"


@pytest.fixture
def sample_product_code():
    """Fixture para código de producto de prueba"""
    return "PROD-001"


@pytest.fixture
def sample_user_id():
    """Fixture para ID de usuario de prueba"""
    return "user-123"
