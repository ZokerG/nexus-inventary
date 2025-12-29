from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

# Domain imports
from nexus_domain.use_cases.empresa_use_cases import (
    CreateEmpresaUseCase,
    GetEmpresaUseCase,
    ListEmpresasUseCase,
    UpdateEmpresaUseCase,
    DeleteEmpresaUseCase
)
from nexus_domain.exceptions import (
    DomainException,
    ValidationError,
    EntityNotFoundError,
    DuplicateEntityError,
    BusinessRuleViolationError
)

from apps.authentication.permissions import IsExternoOrReadOnly
from .repositories import DjangoEmpresaRepository


@extend_schema(tags=['Empresas'])
class EmpresaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD en Empresas usando Clean Architecture
    
    - GET: Todos los usuarios autenticados pueden ver
    - POST/PUT/DELETE: Solo administradores
    """
    permission_classes = [IsExternoOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nit']
    search_fields = ['nombre', 'nit']
    ordering_fields = ['nombre', 'created_at']
    
    def _get_repository(self):
        """Obtener instancia del repositorio"""
        return DjangoEmpresaRepository()
    
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
        summary="Listar empresas",
        description="Obtener lista de todas las empresas registradas",
        parameters=[
            OpenApiParameter(name='search', description='Buscar por nombre o NIT', type=OpenApiTypes.STR),
            OpenApiParameter(name='ordering', description='Ordenar por campo (nombre, created_at)', type=OpenApiTypes.STR),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Listar empresas usando caso de uso"""
        try:
            repository = self._get_repository()
            use_case = ListEmpresasUseCase(repository)
            
            # Obtener parámetros de búsqueda
            search = request.query_params.get('search', '')
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 100))
            offset = (page - 1) * page_size
            
            if search:
                empresas = use_case.execute(limit=page_size, offset=offset, search=search)
            else:
                empresas = use_case.execute(limit=page_size, offset=offset)
            
            # Convertir entidades a diccionarios
            data = [empresa.to_dict() for empresa in empresas]
            return Response(data, status=status.HTTP_200_OK)
            
        except DomainException as e:
            return self._handle_domain_exception(e)
    
    @extend_schema(
        summary="Crear empresa",
        description="Crear una nueva empresa (solo administradores)"
    )
    def create(self, request, *args, **kwargs):
        """Crear empresa usando caso de uso"""
        try:
            repository = self._get_repository()
            use_case = CreateEmpresaUseCase(repository)
            
            empresa = use_case.execute(
                nit=request.data.get('nit'),
                nombre=request.data.get('nombre'),
                direccion=request.data.get('direccion'),
                telefono=request.data.get('telefono'),
                user_id=str(request.user.id)
            )
            
            return Response(empresa.to_dict(), status=status.HTTP_201_CREATED)
            
        except DomainException as e:
            return self._handle_domain_exception(e)
    
    @extend_schema(
        summary="Obtener empresa",
        description="Obtener detalles de una empresa específica por NIT"
    )
    def retrieve(self, request, *args, **kwargs):
        """Obtener empresa usando caso de uso"""
        try:
            repository = self._get_repository()
            use_case = GetEmpresaUseCase(repository)
            
            nit = kwargs.get('pk')
            empresa = use_case.execute(nit)
            
            return Response(empresa.to_dict(), status=status.HTTP_200_OK)
            
        except DomainException as e:
            return self._handle_domain_exception(e)
    
    @extend_schema(
        summary="Actualizar empresa",
        description="Actualizar completamente una empresa (solo administradores)"
    )
    def update(self, request, *args, **kwargs):
        """Actualizar empresa usando caso de uso"""
        try:
            repository = self._get_repository()
            use_case = UpdateEmpresaUseCase(repository)
            
            nit = kwargs.get('pk')
            empresa = use_case.execute(
                nit=nit,
                nombre=request.data.get('nombre'),
                direccion=request.data.get('direccion'),
                telefono=request.data.get('telefono')
            )
            
            return Response(empresa.to_dict(), status=status.HTTP_200_OK)
            
        except DomainException as e:
            return self._handle_domain_exception(e)
    
    @extend_schema(
        summary="Actualizar empresa parcialmente",
        description="Actualizar parcialmente una empresa (solo administradores)"
    )
    def partial_update(self, request, *args, **kwargs):
        """Actualizar parcialmente empresa usando caso de uso"""
        try:
            repository = self._get_repository()
            use_case = UpdateEmpresaUseCase(repository)
            
            nit = kwargs.get('pk')
            
            # Solo actualizar campos presentes en request.data
            kwargs_update = {'nit': nit}
            if 'nombre' in request.data:
                kwargs_update['nombre'] = request.data['nombre']
            if 'direccion' in request.data:
                kwargs_update['direccion'] = request.data['direccion']
            if 'telefono' in request.data:
                kwargs_update['telefono'] = request.data['telefono']
            
            empresa = use_case.execute(**kwargs_update)
            
            return Response(empresa.to_dict(), status=status.HTTP_200_OK)
            
        except DomainException as e:
            return self._handle_domain_exception(e)
    
    @extend_schema(
        summary="Eliminar empresa",
        description="Eliminar una empresa (solo administradores)"
    )
    def destroy(self, request, *args, **kwargs):
        """Eliminar empresa usando caso de uso"""
        try:
            repository = self._get_repository()
            use_case = DeleteEmpresaUseCase(repository)
            
            nit = kwargs.get('pk')
            use_case.execute(nit)
            
            return Response(
                {'message': f'Empresa con NIT {nit} eliminada exitosamente'},
                status=status.HTTP_204_NO_CONTENT
            )
            
        except DomainException as e:
            return self._handle_domain_exception(e)
