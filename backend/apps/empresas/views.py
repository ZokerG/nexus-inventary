from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from apps.authentication.permissions import IsExternoOrReadOnly
from .models import Empresa
from .serializers import EmpresaSerializer


@extend_schema(tags=['Empresas'])
class EmpresaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD en Empresas
    
    - GET: Todos los usuarios autenticados pueden ver
    - POST/PUT/DELETE: Solo administradores
    """
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsExternoOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nit']
    search_fields = ['nombre', 'nit']
    ordering_fields = ['nombre', 'created_at']
    
    @extend_schema(
        summary="Listar empresas",
        description="Obtener lista de todas las empresas registradas",
        parameters=[
            OpenApiParameter(name='search', description='Buscar por nombre o NIT', type=OpenApiTypes.STR),
            OpenApiParameter(name='ordering', description='Ordenar por campo (nombre, created_at)', type=OpenApiTypes.STR),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Crear empresa",
        description="Crear una nueva empresa (solo administradores)"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary="Obtener empresa",
        description="Obtener detalles de una empresa específica por NIT"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Actualizar empresa",
        description="Actualizar completamente una empresa (solo administradores)"
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Actualizar empresa parcialmente",
        description="Actualizar parcialmente una empresa (solo administradores)"
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Eliminar empresa",
        description="Eliminar una empresa (solo administradores)"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        """Asignar el usuario actual como creador"""
        serializer.save(created_by=self.request.user)
