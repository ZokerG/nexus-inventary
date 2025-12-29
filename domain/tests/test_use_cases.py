"""
Tests para Use Cases - Con mocks de repositorios
"""
import pytest
from unittest.mock import Mock
from nexus_domain.entities import Empresa, Producto, Inventario
from nexus_domain.value_objects import NIT, Phone, ProductCode, Quantity
from nexus_domain.exceptions import (
    DuplicateEntityError, 
    EntityNotFoundError,
    InsufficientStockError,
    BusinessRuleViolationError
)
from nexus_domain.use_cases.empresa_use_cases import (
    CreateEmpresaUseCase,
    GetEmpresaUseCase,
    ListEmpresasUseCase,
    UpdateEmpresaUseCase,
    DeleteEmpresaUseCase
)
from nexus_domain.use_cases.producto_use_cases import (
    CreateProductoUseCase,
    GetProductoUseCase
)
from nexus_domain.use_cases.inventario_use_cases import (
    CreateOrUpdateInventarioUseCase,
    AddStockUseCase,
    RemoveStockUseCase,
    GetLowStockItemsUseCase
)


class TestEmpresaUseCases:
    """Tests para use cases de Empresa"""
    
    def test_create_empresa_success(self):
        # Arrange
        mock_repo = Mock()
        mock_repo.exists.return_value = False
        
        # El mock debe devolver la entidad guardada
        def save_side_effect(empresa):
            return empresa
        mock_repo.save.side_effect = save_side_effect
        
        use_case = CreateEmpresaUseCase(mock_repo)
        
        # Act
        empresa = use_case.execute(
            nit="900123456",
            nombre="Empresa Test",
            direccion="Calle 123",
            telefono="3001234567",
            user_id="user-123"
        )
        
        # Assert
        assert empresa.nombre == "Empresa Test"
        mock_repo.exists.assert_called_once()
        mock_repo.save.assert_called_once()
    
    def test_create_empresa_duplicate_raises_error(self):
        # Arrange
        mock_repo = Mock()
        mock_repo.exists.return_value = True
        
        use_case = CreateEmpresaUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(DuplicateEntityError, match="ya existe"):
            use_case.execute(
                nit="900123456",
                nombre="Empresa Test",
                direccion="Calle 123",
                telefono="3001234567",
                user_id="user-123"
            )
    
    def test_get_empresa_found(self):
        # Arrange
        mock_repo = Mock()
        empresa = Empresa(
            nit=NIT("900123456"),
            nombre="Empresa Test",
            direccion="Calle 123",
            telefono=Phone("3001234567"),
            created_by_id="user-123"
        )
        mock_repo.find_by_nit.return_value = empresa
        
        use_case = GetEmpresaUseCase(mock_repo)
        
        # Act
        result = use_case.execute("900123456")
        
        # Assert
        assert result == empresa
        # GetEmpresaUseCase convierte string a NIT dentro del execute
        mock_repo.find_by_nit.assert_called_once()
    
    def test_get_empresa_not_found_raises_error(self):
        # Arrange
        mock_repo = Mock()
        mock_repo.find_by_nit.return_value = None
        
        use_case = GetEmpresaUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(EntityNotFoundError, match="no encontrada"):
            use_case.execute("900123456")
    
    def test_list_empresas(self):
        # Arrange
        mock_repo = Mock()
        empresas = [
            Empresa(
                nit=NIT("900111111"),
                nombre="Empresa 1",
                direccion="Calle 1",
                telefono=Phone("3001111111"),
                created_by_id="user-1"
            ),
            Empresa(
                nit=NIT("900222222"),
                nombre="Empresa 2",
                direccion="Calle 2",
                telefono=Phone("3002222222"),
                created_by_id="user-2"
            )
        ]
        mock_repo.find_all.return_value = empresas
        
        use_case = ListEmpresasUseCase(mock_repo)
        
        # Act
        result = use_case.execute()
        
        # Assert
        assert len(result) == 2
        assert result == empresas
    
    def test_update_empresa_success(self):
        # Arrange
        mock_repo = Mock()
        empresa = Empresa(
            nit=NIT("900123456"),
            nombre="Nombre Original",
            direccion="Direccion Original",
            telefono=Phone("3001234567"),
            created_by_id="user-123"
        )
        mock_repo.find_by_nit.return_value = empresa
        
        # El mock debe devolver la entidad guardada
        def save_side_effect(emp):
            return emp
        mock_repo.save.side_effect = save_side_effect
        
        use_case = UpdateEmpresaUseCase(mock_repo)
        
        # Act
        updated = use_case.execute(
            nit="900123456",
            nombre="Nombre Actualizado"
        )
        
        # Assert
        assert updated.nombre == "Nombre Actualizado"
        mock_repo.save.assert_called_once()
    
    def test_delete_empresa_success(self):
        # Arrange
        mock_repo = Mock()
        empresa = Empresa(
            nit=NIT("900123456"),
            nombre="Empresa Test",
            direccion="Calle 123",
            telefono=Phone("3001234567"),
            created_by_id="user-123"
        )
        mock_repo.find_by_nit.return_value = empresa
        mock_repo.delete.return_value = None
        
        use_case = DeleteEmpresaUseCase(mock_repo)
        
        # Act
        use_case.execute("900123456")
        
        # Assert
        mock_repo.delete.assert_called_once()


class TestProductoUseCases:
    """Tests para use cases de Producto"""
    
    def test_create_producto_success(self):
        # Arrange
        mock_producto_repo = Mock()
        mock_empresa_repo = Mock()
        
        mock_producto_repo.exists.return_value = False
        mock_empresa_repo.exists.return_value = True
        
        # El mock debe devolver la entidad guardada
        def save_side_effect(producto):
            return producto
        mock_producto_repo.save.side_effect = save_side_effect
        
        use_case = CreateProductoUseCase(mock_producto_repo, mock_empresa_repo)
        
        # Act
        producto = use_case.execute(
            codigo="PROD-001",
            nombre="Producto Test",
            empresa_nit="900123456",
            caracteristicas="Test",
            user_id="user-123"
        )
        
        # Assert
        assert producto.nombre == "Producto Test"
        mock_producto_repo.save.assert_called_once()
    
    def test_create_producto_empresa_not_exists_raises_error(self):
        # Arrange
        mock_producto_repo = Mock()
        mock_empresa_repo = Mock()
        
        # La empresa no existe, pero el producto tampoco
        mock_producto_repo.exists.return_value = False
        mock_empresa_repo.exists.return_value = False
        
        use_case = CreateProductoUseCase(mock_producto_repo, mock_empresa_repo)
        
        # Act & Assert
        with pytest.raises(EntityNotFoundError, match="Empresa .* no encontrada"):
            use_case.execute(
                codigo="PROD-001",
                nombre="Producto Test",
                empresa_nit="900999999",
                caracteristicas="Test",
                user_id="user-123"
            )
    
    def test_get_producto_found(self):
        # Arrange
        mock_repo = Mock()
        producto = Producto(
            codigo=ProductCode("PROD-001"),
            nombre="Producto Test",
            empresa_nit=NIT("900123456"),
            caracteristicas="Test",
            created_by_id="user-123"
        )
        mock_repo.find_by_codigo.return_value = producto
        
        use_case = GetProductoUseCase(mock_repo)
        
        # Act
        result = use_case.execute("PROD-001")
        
        # Assert
        assert result == producto


class TestInventarioUseCases:
    """Tests para use cases de Inventario"""
    
    def test_create_inventario_success(self):
        # Arrange
        mock_inventario_repo = Mock()
        mock_empresa_repo = Mock()
        mock_producto_repo = Mock()
        
        mock_empresa_repo.exists.return_value = True
        mock_producto_repo.exists.return_value = True
        mock_inventario_repo.find_by_empresa_and_producto.return_value = None
        
        # El mock debe devolver la entidad guardada
        def save_side_effect(inventario):
            return inventario
        mock_inventario_repo.save.side_effect = save_side_effect
        
        use_case = CreateOrUpdateInventarioUseCase(
            mock_inventario_repo,
            mock_empresa_repo,
            mock_producto_repo
        )
        
        # Act
        inventario = use_case.execute(
            empresa_nit="900123456",
            producto_codigo="PROD-001",
            cantidad=100
        )
        
        # Assert
        assert int(inventario.cantidad) == 100
        mock_inventario_repo.save.assert_called_once()
    
    def test_add_stock_success(self):
        # Arrange
        mock_repo = Mock()
        inventario = Inventario(
            id="inv-123",
            empresa_nit=NIT("900123456"),
            producto_codigo=ProductCode("PROD-001"),
            cantidad=Quantity(50)
        )
        mock_repo.find_by_id.return_value = inventario
        
        # El mock debe devolver la entidad guardada
        def save_side_effect(inv):
            return inv
        mock_repo.save.side_effect = save_side_effect
        
        use_case = AddStockUseCase(mock_repo)
        
        # Act
        updated = use_case.execute("inv-123", 30)
        
        # Assert
        assert int(updated.cantidad) == 80
        mock_repo.save.assert_called_once()
    
    def test_remove_stock_success(self):
        # Arrange
        mock_repo = Mock()
        inventario = Inventario(
            id="inv-123",
            empresa_nit=NIT("900123456"),
            producto_codigo=ProductCode("PROD-001"),
            cantidad=Quantity(100)
        )
        mock_repo.find_by_id.return_value = inventario
        
        # El mock debe devolver la entidad guardada
        def save_side_effect(inv):
            return inv
        mock_repo.save.side_effect = save_side_effect
        
        use_case = RemoveStockUseCase(mock_repo)
        
        # Act
        updated = use_case.execute("inv-123", 40)
        
        # Assert
        assert int(updated.cantidad) == 60
        mock_repo.save.assert_called_once()
    
    def test_remove_stock_insufficient_raises_error(self):
        # Arrange
        mock_repo = Mock()
        inventario = Inventario(
            id="inv-123",
            empresa_nit=NIT("900123456"),
            producto_codigo=ProductCode("PROD-001"),
            cantidad=Quantity(20)
        )
        mock_repo.find_by_id.return_value = inventario
        
        use_case = RemoveStockUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(InsufficientStockError):
            use_case.execute("inv-123", 50)
    
    def test_get_low_stock_items(self):
        # Arrange
        mock_repo = Mock()
        low_stock_items = [
            Inventario(
                id="inv-1",
                empresa_nit=NIT("900123456"),
                producto_codigo=ProductCode("PROD-001"),
                cantidad=Quantity(5)
            ),
            Inventario(
                id="inv-2",
                empresa_nit=NIT("900123456"),
                producto_codigo=ProductCode("PROD-002"),
                cantidad=Quantity(8)
            )
        ]
        mock_repo.find_low_stock.return_value = low_stock_items
        
        use_case = GetLowStockItemsUseCase(mock_repo)
        
        # Act
        result = use_case.execute(threshold=10)
        
        # Assert
        assert len(result) == 2
        mock_repo.find_low_stock.assert_called_once_with(threshold=10)
