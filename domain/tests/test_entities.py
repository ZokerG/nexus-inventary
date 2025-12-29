"""
Tests para Entities - Sin dependencias de Django
"""
import pytest
from datetime import datetime
from nexus_domain.entities import Empresa, Producto, Inventario
from nexus_domain.value_objects import NIT, Email, Phone, ProductCode, Quantity
from nexus_domain.exceptions import ValidationError, InsufficientStockError


class TestEmpresa:
    """Tests para Entity Empresa"""
    
    def test_empresa_creation_valid(self):
        empresa = Empresa(
            nit=NIT("900123456"),
            nombre="Empresa Test",
            direccion="Calle 123 # 45-67",
            telefono=Phone("3001234567"),
            created_by_id="user-123"
        )
        assert empresa.nombre == "Empresa Test"
        assert str(empresa.nit) == "900123456"
    
    def test_empresa_nombre_too_short_raises_error(self):
        with pytest.raises(ValidationError, match="al menos 3 caracteres"):
            Empresa(
                nit=NIT("900123456"),
                nombre="AB",
                direccion="Calle 123 # 45-67",
                telefono=Phone("3001234567"),
                created_by_id="user-123"
            )
    
    def test_empresa_direccion_too_short_raises_error(self):
        with pytest.raises(ValidationError, match="al menos 5 caracteres"):
            Empresa(
                nit=NIT("900123456"),
                nombre="Empresa Test",
                direccion="Cll",
                telefono=Phone("3001234567"),
                created_by_id="user-123"
            )
    
    def test_empresa_update_info(self):
        empresa = Empresa(
            nit=NIT("900123456"),
            nombre="Nombre Original",
            direccion="Direccion Original",
            telefono=Phone("3001234567"),
            created_by_id="user-123"
        )
        
        empresa.update_info(
            nombre="Nombre Actualizado",
            direccion="Nueva Direccion",
            telefono=Phone("3009876543")
        )
        
        assert empresa.nombre == "Nombre Actualizado"
        assert empresa.direccion == "Nueva Direccion"
        assert str(empresa.telefono) == "3009876543"
    
    def test_empresa_can_be_deleted(self):
        empresa = Empresa(
            nit=NIT("900123456"),
            nombre="Empresa Test",
            direccion="Calle 123",
            telefono=Phone("3001234567"),
            created_by_id="user-123"
        )
        assert empresa.can_be_deleted() is True
    
    def test_empresa_equality_by_nit(self):
        empresa1 = Empresa(
            nit=NIT("900123456"),
            nombre="Empresa A",
            direccion="Calle 1",
            telefono=Phone("3001111111"),
            created_by_id="user-1"
        )
        empresa2 = Empresa(
            nit=NIT("900123456"),
            nombre="Empresa B",
            direccion="Calle 2",
            telefono=Phone("3002222222"),
            created_by_id="user-2"
        )
        assert empresa1 == empresa2  # Same NIT


class TestProducto:
    """Tests para Entity Producto"""
    
    def test_producto_creation_valid(self):
        producto = Producto(
            codigo=ProductCode("PROD-001"),
            nombre="Producto Test",
            empresa_nit=NIT("900123456"),
            caracteristicas="Características del producto",
            created_by_id="user-123"
        )
        assert producto.nombre == "Producto Test"
        assert str(producto.codigo) == "PROD-001"
    
    def test_producto_nombre_too_short_raises_error(self):
        with pytest.raises(ValidationError, match="al menos 2 caracteres"):
            Producto(
                codigo=ProductCode("PROD-001"),
                nombre="A",
                empresa_nit=NIT("900123456"),
                caracteristicas="Test",
                created_by_id="user-123"
            )
    
    def test_producto_update_info(self):
        producto = Producto(
            codigo=ProductCode("PROD-001"),
            nombre="Nombre Original",
            empresa_nit=NIT("900123456"),
            caracteristicas="Original",
            created_by_id="user-123"
        )
        
        producto.update_info(
            nombre="Nombre Nuevo",
            caracteristicas="Nuevas características"
        )
        
        assert producto.nombre == "Nombre Nuevo"
        assert producto.caracteristicas == "Nuevas características"
    
    def test_producto_change_empresa(self):
        producto = Producto(
            codigo=ProductCode("PROD-001"),
            nombre="Producto",
            empresa_nit=NIT("900111111"),
            caracteristicas="Test",
            created_by_id="user-123"
        )
        
        new_nit = NIT("900222222")
        producto.change_empresa(new_nit)
        
        assert str(producto.empresa_nit) == "900222222"
    
    def test_producto_has_caracteristicas(self):
        producto = Producto(
            codigo=ProductCode("PROD-001"),
            nombre="Producto",
            empresa_nit=NIT("900123456"),
            caracteristicas="Algunas características",
            created_by_id="user-123"
        )
        assert producto.has_caracteristicas() is True
        
        producto_sin = Producto(
            codigo=ProductCode("PROD-002"),
            nombre="Producto Sin",
            empresa_nit=NIT("900123456"),
            caracteristicas="",
            created_by_id="user-123"
        )
        assert producto_sin.has_caracteristicas() is False


class TestInventario:
    """Tests para Entity Inventario"""
    
    def test_inventario_creation_valid(self):
        inventario = Inventario(
            id="inv-123",
            empresa_nit=NIT("900123456"),
            producto_codigo=ProductCode("PROD-001"),
            cantidad=Quantity(100)
        )
        assert int(inventario.cantidad) == 100
    
    def test_inventario_add_stock(self):
        inventario = Inventario(
            id="inv-123",
            empresa_nit=NIT("900123456"),
            producto_codigo=ProductCode("PROD-001"),
            cantidad=Quantity(50)
        )
        
        inventario.add_stock(Quantity(30))
        assert int(inventario.cantidad) == 80
    
    def test_inventario_remove_stock_success(self):
        inventario = Inventario(
            id="inv-123",
            empresa_nit=NIT("900123456"),
            producto_codigo=ProductCode("PROD-001"),
            cantidad=Quantity(100)
        )
        
        inventario.remove_stock(Quantity(40))
        assert int(inventario.cantidad) == 60
    
    def test_inventario_remove_stock_insufficient_raises_error(self):
        inventario = Inventario(
            id="inv-123",
            empresa_nit=NIT("900123456"),
            producto_codigo=ProductCode("PROD-001"),
            cantidad=Quantity(20)
        )
        
        with pytest.raises(InsufficientStockError, match="Stock insuficiente"):
            inventario.remove_stock(Quantity(50))
    
    def test_inventario_update_stock(self):
        inventario = Inventario(
            id="inv-123",
            empresa_nit=NIT("900123456"),
            producto_codigo=ProductCode("PROD-001"),
            cantidad=Quantity(100)
        )
        
        inventario.update_stock(Quantity(200))
        assert int(inventario.cantidad) == 200
    
    def test_inventario_is_low_stock(self):
        inventario_low = Inventario(
            id="inv-123",
            empresa_nit=NIT("900123456"),
            producto_codigo=ProductCode("PROD-001"),
            cantidad=Quantity(5)
        )
        assert inventario_low.is_low_stock() is True
        
        inventario_ok = Inventario(
            id="inv-124",
            empresa_nit=NIT("900123456"),
            producto_codigo=ProductCode("PROD-002"),
            cantidad=Quantity(50)
        )
        assert inventario_ok.is_low_stock() is False
    
    def test_inventario_is_out_of_stock(self):
        inventario_out = Inventario(
            id="inv-123",
            empresa_nit=NIT("900123456"),
            producto_codigo=ProductCode("PROD-001"),
            cantidad=Quantity(0)
        )
        assert inventario_out.is_out_of_stock() is True
    
    def test_inventario_can_fulfill_order(self):
        inventario = Inventario(
            id="inv-123",
            empresa_nit=NIT("900123456"),
            producto_codigo=ProductCode("PROD-001"),
            cantidad=Quantity(100)
        )
        
        assert inventario.can_fulfill_order(Quantity(50)) is True
        assert inventario.can_fulfill_order(Quantity(150)) is False
    
    def test_inventario_get_stock_status(self):
        inv_agotado = Inventario(
            id="inv-1",
            empresa_nit=NIT("900123456"),
            producto_codigo=ProductCode("PROD-001"),
            cantidad=Quantity(0)
        )
        assert inv_agotado.get_stock_status() == "AGOTADO"
        
        inv_bajo = Inventario(
            id="inv-2",
            empresa_nit=NIT("900123456"),
            producto_codigo=ProductCode("PROD-002"),
            cantidad=Quantity(5)
        )
        assert inv_bajo.get_stock_status() == "BAJO"
        
        inv_medio = Inventario(
            id="inv-3",
            empresa_nit=NIT("900123456"),
            producto_codigo=ProductCode("PROD-003"),
            cantidad=Quantity(30)
        )
        assert inv_medio.get_stock_status() == "MEDIO"
        
        inv_alto = Inventario(
            id="inv-4",
            empresa_nit=NIT("900123456"),
            producto_codigo=ProductCode("PROD-004"),
            cantidad=Quantity(100)
        )
        assert inv_alto.get_stock_status() == "ALTO"
