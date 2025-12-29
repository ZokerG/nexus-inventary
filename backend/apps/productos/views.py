from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

# Domain imports
from nexus_domain.use_cases.producto_use_cases import (
    CreateProductoUseCase,
    GetProductoUseCase,
    ListProductosUseCase,
    UpdateProductoUseCase,
    DeleteProductoUseCase
)
from nexus_domain.exceptions import (
    DomainException,
    ValidationError,
    EntityNotFoundError,
    DuplicateEntityError,
    BusinessRuleViolationError
)

from apps.authentication.permissions import IsAdminUser
from apps.empresas.repositories import DjangoEmpresaRepository
from .repositories import DjangoProductoRepository


@extend_schema(tags=['Productos'])
class ProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD en Productos usando Clean Architecture
    
    Solo administradores pueden crear, editar y eliminar productos
    """
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['empresa', 'codigo']
    search_fields = ['nombre', 'codigo']
    ordering_fields = ['nombre', 'created_at']
    
    def _get_repositories(self):
        """Obtener instancias de los repositorios"""
        return DjangoProductoRepository(), DjangoEmpresaRepository()
    
    def _handle_domain_exception(self, exception: DomainException) -> Response:
        """Mapear excepciones de dominio a respuestas HTTP"""
        error_map = {
            ValidationError: status.HTTP_400_BAD_REQUEST,
            DuplicateEntityError: status.HTTP_409_CONFLICT,
            EntityNotFoundError: status.HTTP_404_NOT_FOUND,
            BusinessRuleViolationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
        }
        
        status_code = error_map.get(type(exception), status.HTTP_400_BAD_REQUEST)
        return Response(
            {'error': str(exception), 'type': type(exception).__name__},
            status=status_code
        )
    
    @extend_schema(
        summary="Listar productos",
        description="Obtener lista de todos los productos (solo administradores)",
        parameters=[
            OpenApiParameter(name='empresa', description='Filtrar por NIT de empresa', type=OpenApiTypes.STR),
            OpenApiParameter(name='search', description='Buscar por nombre o código', type=OpenApiTypes.STR),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Listar productos usando caso de uso"""
        try:
            producto_repo, empresa_repo = self._get_repositories()
            use_case = ListProductosUseCase(producto_repo)
            
            # Obtener parámetros
            empresa_nit = request.query_params.get('empresa')
            search = request.query_params.get('search', '')
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 100))
            offset = (page - 1) * page_size
            
            if empresa_nit:
                productos = use_case.execute(limit=page_size, offset=offset, empresa_nit=empresa_nit)
            elif search:
                productos = use_case.execute(limit=page_size, offset=offset, search=search)
            else:
                productos = use_case.execute(limit=page_size, offset=offset)
            
            data = [producto.to_dict() for producto in productos]
            return Response(data, status=status.HTTP_200_OK)
            
        except DomainException as e:
            return self._handle_domain_exception(e)
    
    @extend_schema(
        summary="Crear producto",
        description="Crear un nuevo producto con precios en múltiples monedas (solo administradores)"
    )
    def create(self, request, *args, **kwargs):
        """Crear producto usando caso de uso"""
        try:
            producto_repo, empresa_repo = self._get_repositories()
            use_case = CreateProductoUseCase(producto_repo, empresa_repo)
            
            # Convertir caracteristicas dict a string JSON si es necesario
            import json
            caracteristicas = request.data.get('caracteristicas', {})
            if isinstance(caracteristicas, dict):
                caracteristicas_str = json.dumps(caracteristicas)
            else:
                caracteristicas_str = caracteristicas
            
            producto = use_case.execute(
                codigo=request.data.get('codigo'),
                nombre=request.data.get('nombre'),
                empresa_nit=request.data.get('empresa'),
                caracteristicas=caracteristicas_str,
                user_id=str(request.user.id)
            )
            
            return Response(producto.to_dict(), status=status.HTTP_201_CREATED)
            
        except DomainException as e:
            return self._handle_domain_exception(e)
    
    @extend_schema(
        summary="Obtener producto",
        description="Obtener detalles de un producto específico por código"
    )
    def retrieve(self, request, *args, **kwargs):
        """Obtener producto usando caso de uso"""
        try:
            producto_repo, _ = self._get_repositories()
            use_case = GetProductoUseCase(producto_repo)
            
            codigo = kwargs.get('pk')
            producto = use_case.execute(codigo)
            
            return Response(producto.to_dict(), status=status.HTTP_200_OK)
            
        except DomainException as e:
            return self._handle_domain_exception(e)
    
    @extend_schema(
        summary="Actualizar producto",
        description="Actualizar completamente un producto (solo administradores)"
    )
    def update(self, request, *args, **kwargs):
        """Actualizar producto usando caso de uso"""
        try:
            producto_repo, _ = self._get_repositories()
            use_case = UpdateProductoUseCase(producto_repo)
            
            codigo = kwargs.get('pk')
            
            # Convertir caracteristicas
            import json
            caracteristicas = request.data.get('caracteristicas', {})
            if isinstance(caracteristicas, dict):
                caracteristicas_str = json.dumps(caracteristicas)
            else:
                caracteristicas_str = caracteristicas
            
            producto = use_case.execute(
                codigo=codigo,
                nombre=request.data.get('nombre'),
                caracteristicas=caracteristicas_str
            )
            
            return Response(producto.to_dict(), status=status.HTTP_200_OK)
            
        except DomainException as e:
            return self._handle_domain_exception(e)
    
    @extend_schema(
        summary="Actualizar producto parcialmente",
        description="Actualizar parcialmente un producto (solo administradores)"
    )
    def partial_update(self, request, *args, **kwargs):
        """Actualizar parcialmente producto usando caso de uso"""
        try:
            producto_repo, _ = self._get_repositories()
            use_case = UpdateProductoUseCase(producto_repo)
            
            codigo = kwargs.get('pk')
            kwargs_update = {'codigo': codigo}
            
            if 'nombre' in request.data:
                kwargs_update['nombre'] = request.data['nombre']
            if 'caracteristicas' in request.data:
                import json
                caracteristicas = request.data['caracteristicas']
                if isinstance(caracteristicas, dict):
                    kwargs_update['caracteristicas'] = json.dumps(caracteristicas)
                else:
                    kwargs_update['caracteristicas'] = caracteristicas
            
            producto = use_case.execute(**kwargs_update)
            
            return Response(producto.to_dict(), status=status.HTTP_200_OK)
            
        except DomainException as e:
            return self._handle_domain_exception(e)
    
    @extend_schema(
        summary="Eliminar producto",
        description="Eliminar un producto (solo administradores)"
    )
    def destroy(self, request, *args, **kwargs):
        """Eliminar producto usando caso de uso"""
        try:
            producto_repo, _ = self._get_repositories()
            use_case = DeleteProductoUseCase(producto_repo)
            
            codigo = kwargs.get('pk')
            use_case.execute(codigo)
            
            return Response(
                {'message': f'Producto con código {codigo} eliminado exitosamente'},
                status=status.HTTP_204_NO_CONTENT
            )
            
        except DomainException as e:
            return self._handle_domain_exception(e)
