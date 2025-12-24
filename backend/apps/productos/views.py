from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from apps.authentication.permissions import IsAdminUser
from .models import Producto
from .serializers import ProductoSerializer


@extend_schema(tags=['Productos'])
class ProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD en Productos
    
    Solo administradores pueden crear, editar y eliminar productos
    """
    queryset = Producto.objects.all().select_related('empresa').prefetch_related('precios')
    serializer_class = ProductoSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['empresa', 'codigo']
    search_fields = ['nombre', 'codigo']
    ordering_fields = ['nombre', 'created_at']
    
    @extend_schema(
        summary="Listar productos",
        description="Obtener lista de todos los productos (solo administradores)",
        parameters=[
            OpenApiParameter(name='empresa', description='Filtrar por NIT de empresa', type=OpenApiTypes.STR),
            OpenApiParameter(name='search', description='Buscar por nombre o código', type=OpenApiTypes.STR),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Crear producto",
        description="Crear un nuevo producto con precios en múltiples monedas (solo administradores)"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary="Obtener producto",
        description="Obtener detalles de un producto específico por código"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Actualizar producto",
        description="Actualizar completamente un producto (solo administradores)"
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Actualizar producto parcialmente",
        description="Actualizar parcialmente un producto (solo administradores)"
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Eliminar producto",
        description="Eliminar un producto (solo administradores)"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        """Asignar el usuario actual como creador"""
        serializer.save(created_by=self.request.user)
