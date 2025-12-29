"""
Tests para Value Objects - Sin dependencias de Django
"""
import pytest
from nexus_domain.value_objects import NIT, Email, Phone, ProductCode, Quantity
from nexus_domain.exceptions import ValidationError, InsufficientStockError


class TestNIT:
    """Tests para Value Object NIT"""
    
    def test_nit_valid(self):
        nit = NIT("900123456")
        assert str(nit) == "900123456"
    
    def test_nit_with_dash(self):
        nit = NIT("900123456-7")
        assert str(nit) == "900123456-7"
    
    def test_nit_empty_raises_error(self):
        with pytest.raises(ValidationError, match="NIT no puede estar vacío"):
            NIT("")
    
    def test_nit_too_short_raises_error(self):
        with pytest.raises(ValidationError, match="al menos 5 caracteres"):
            NIT("123")
    
    def test_nit_invalid_format_raises_error(self):
        with pytest.raises(ValidationError, match="solo números y guiones"):
            NIT("ABC123")
    
    def test_nit_equality(self):
        nit1 = NIT("900123456")
        nit2 = NIT("900123456")
        assert nit1 == nit2
    
    def test_nit_immutable(self):
        nit = NIT("900123456")
        with pytest.raises(AttributeError):
            nit.value = "999999999"  # type: ignore


class TestEmail:
    """Tests para Value Object Email"""
    
    def test_email_valid(self):
        email = Email("test@example.com")
        assert str(email) == "test@example.com"
    
    def test_email_domain(self):
        email = Email("user@company.com")
        assert email.domain() == "company.com"
    
    def test_email_invalid_raises_error(self):
        with pytest.raises(ValidationError, match="Email inválido"):
            Email("not-an-email")
    
    def test_email_empty_raises_error(self):
        with pytest.raises(ValidationError, match="no puede estar vacío"):
            Email("")


class TestPhone:
    """Tests para Value Object Phone"""
    
    def test_phone_valid(self):
        phone = Phone("3001234567")
        assert str(phone) == "3001234567"
    
    def test_phone_with_spaces(self):
        phone = Phone("300 123 4567")
        assert str(phone) == "300 123 4567"
    
    def test_phone_too_short_raises_error(self):
        with pytest.raises(ValidationError, match="entre 7 y 15 dígitos"):
            Phone("12345")
    
    def test_phone_non_numeric_raises_error(self):
        with pytest.raises(ValidationError, match="solo números"):
            Phone("ABC1234567")


class TestProductCode:
    """Tests para Value Object ProductCode"""
    
    def test_product_code_valid(self):
        code = ProductCode("PROD-001")
        assert str(code) == "PROD-001"
    
    def test_product_code_case_insensitive_equality(self):
        code1 = ProductCode("PROD-001")
        code2 = ProductCode("prod-001")
        assert code1 == code2
    
    def test_product_code_empty_raises_error(self):
        with pytest.raises(ValidationError, match="no puede estar vacío"):
            ProductCode("")
    
    def test_product_code_too_short_raises_error(self):
        with pytest.raises(ValidationError, match="al menos 3 caracteres"):
            ProductCode("AB")


class TestQuantity:
    """Tests para Value Object Quantity"""
    
    def test_quantity_valid(self):
        qty = Quantity(100)
        assert int(qty) == 100
    
    def test_quantity_negative_raises_error(self):
        with pytest.raises(ValidationError, match="no puede ser negativa"):
            Quantity(-1)
    
    def test_quantity_add(self):
        qty1 = Quantity(50)
        qty2 = Quantity(30)
        result = qty1.add(qty2)
        assert int(result) == 80
    
    def test_quantity_subtract(self):
        qty1 = Quantity(50)
        qty2 = Quantity(20)
        result = qty1.subtract(qty2)
        assert int(result) == 30
    
    def test_quantity_subtract_insufficient_raises_error(self):
        qty1 = Quantity(10)
        qty2 = Quantity(20)
        with pytest.raises(ValidationError, match="cantidad negativa"):
            qty1.subtract(qty2)
    
    def test_quantity_is_sufficient(self):
        qty = Quantity(100)
        required = Quantity(50)
        assert qty.is_sufficient(required) is True
        
        insufficient = Quantity(150)
        assert qty.is_sufficient(insufficient) is False
    
    def test_quantity_immutable(self):
        qty = Quantity(100)
        with pytest.raises(AttributeError):
            qty.value = 200  # type: ignore
