from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.http import FileResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers as s
import os

# Domain imports
from nexus_domain.use_cases.inventario_use_cases import (
    CreateOrUpdateInventarioUseCase,
    GetInventarioUseCase,
    AddStockUseCase,
    RemoveStockUseCase,
    DeleteInventarioUseCase,
    GetLowStockItemsUseCase
)
from nexus_domain.exceptions import (
    DomainException,
    ValidationError,
    EntityNotFoundError,
    DuplicateEntityError,
    BusinessRuleViolationError,
    InsufficientStockError
)

from apps.authentication.permissions import IsAdminUser
from apps.empresas.repositories import DjangoEmpresaRepository
from apps.productos.repositories import DjangoProductoRepository
from .orm_models import Inventario
from .repositories import DjangoInventarioRepository


@extend_schema(tags=['Inventario'])
class InventarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD en Inventario usando Clean Architecture
    
    Solo administradores pueden gestionar inventario
    """
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['empresa', 'producto']
    search_fields = ['empresa__nombre', 'producto__nombre']
    ordering_fields = ['fecha_registro', 'cantidad']
    
    def _get_repositories(self):
        """Obtener instancias de los repositorios"""
        return (
            DjangoInventarioRepository(),
            DjangoEmpresaRepository(),
            DjangoProductoRepository()
        )
    
    def _handle_domain_exception(self, exception: DomainException) -> Response:
        """Mapear excepciones de dominio a respuestas HTTP"""
        error_map = {
            ValidationError: status.HTTP_400_BAD_REQUEST,
            DuplicateEntityError: status.HTTP_409_CONFLICT,
            EntityNotFoundError: status.HTTP_404_NOT_FOUND,
            BusinessRuleViolationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
            InsufficientStockError: status.HTTP_400_BAD_REQUEST,
        }
        
        status_code = error_map.get(type(exception), status.HTTP_400_BAD_REQUEST)
        return Response(
            {'error': str(exception), 'type': type(exception).__name__},
            status=status_code
        )
    
    @extend_schema(
        summary="Listar inventario",
        description="Obtener lista de todo el inventario (solo administradores)",
        parameters=[
            OpenApiParameter(name='empresa', description='Filtrar por NIT de empresa', type=OpenApiTypes.STR),
            OpenApiParameter(name='producto', description='Filtrar por código de producto', type=OpenApiTypes.STR),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Listar inventario usando caso de uso"""
        try:
            inventario_repo, _, _ = self._get_repositories()
            use_case = GetInventarioUseCase(inventario_repo)
            
            # Obtener parámetros
            empresa_nit = request.query_params.get('empresa')
            
            # GetInventarioUseCase solo acepta empresa_nit, no paginación
            if empresa_nit:
                inventarios = use_case.execute(empresa_nit=empresa_nit)
            else:
                inventarios = use_case.execute()
            
            data = [inv.to_dict() for inv in inventarios]
            return Response(data, status=status.HTTP_200_OK)
            
        except DomainException as e:
            return self._handle_domain_exception(e)
    
    @extend_schema(
        summary="Crear registro de inventario",
        description="Agregar un producto al inventario de una empresa (solo administradores)"
    )
    def create(self, request, *args, **kwargs):
        """Crear inventario usando caso de uso"""
        try:
            inventario_repo, empresa_repo, producto_repo = self._get_repositories()
            use_case = CreateOrUpdateInventarioUseCase(inventario_repo, empresa_repo, producto_repo)
            
            inventario = use_case.execute(
                empresa_nit=request.data.get('empresa'),
                producto_codigo=request.data.get('producto'),
                cantidad=int(request.data.get('cantidad', 0))
            )
            
            return Response(inventario.to_dict(), status=status.HTTP_201_CREATED)
            
        except DomainException as e:
            return self._handle_domain_exception(e)
    
    @extend_schema(
        summary="Obtener registro de inventario",
        description="Obtener detalles de un registro específico de inventario"
    )
    def retrieve(self, request, *args, **kwargs):
        """Obtener inventario usando ORM directo (mantener compatibilidad con IDs)"""
        try:
            inventario_id = kwargs.get('pk')
            orm_obj = Inventario.objects.select_related('empresa', 'producto').get(id=inventario_id)
            
            # Convertir a formato compatible
            data = {
                'id': orm_obj.id,
                'empresa': orm_obj.empresa.nit,
                'producto': orm_obj.producto.codigo,
                'cantidad': orm_obj.cantidad,
                'fecha_registro': orm_obj.fecha_registro,
                'updated_at': orm_obj.updated_at
            }
            
            return Response(data, status=status.HTTP_200_OK)
            
        except Inventario.DoesNotExist:
            return Response(
                {'error': f'Inventario con ID {inventario_id} no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @extend_schema(
        summary="Actualizar inventario",
        description="Actualizar completamente un registro de inventario (solo administradores)"
    )
    def update(self, request, *args, **kwargs):
        """Actualizar inventario usando caso de uso"""
        try:
            inventario_repo, empresa_repo, producto_repo = self._get_repositories()
            use_case = CreateOrUpdateInventarioUseCase(inventario_repo, empresa_repo, producto_repo)
            
            inventario = use_case.execute(
                empresa_nit=request.data.get('empresa'),
                producto_codigo=request.data.get('producto'),
                cantidad=int(request.data.get('cantidad', 0))
            )
            
            return Response(inventario.to_dict(), status=status.HTTP_200_OK)
            
        except DomainException as e:
            return self._handle_domain_exception(e)
    
    @extend_schema(
        summary="Actualizar inventario parcialmente",
        description="Actualizar parcialmente un registro de inventario (solo administradores)"
    )
    def partial_update(self, request, *args, **kwargs):
        """Actualizar parcialmente inventario"""
        # Para actualización parcial, usamos ORM directo por simplicidad
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Eliminar registro de inventario",
        description="Eliminar un registro de inventario (solo administradores)"
    )
    def destroy(self, request, *args, **kwargs):
        """Eliminar inventario usando caso de uso"""
        try:
            inventario_repo, _, _ = self._get_repositories()
            use_case = DeleteInventarioUseCase(inventario_repo)
            
            inventario_id = kwargs.get('pk')
            use_case.execute(inventario_id)
            
            return Response(
                {'message': f'Inventario con ID {inventario_id} eliminado exitosamente'},
                status=status.HTTP_204_NO_CONTENT
            )
            
        except DomainException as e:
            return self._handle_domain_exception(e)
    
    @extend_schema(
        summary="Exportar inventario a PDF",
        description="Generar y descargar un PDF con el inventario. Se puede filtrar por empresa.",
        parameters=[
            OpenApiParameter(
                name='empresa',
                description='NIT de la empresa para filtrar (opcional)',
                required=False,
                type=OpenApiTypes.STR
            ),
        ],
        responses={
            200: OpenApiTypes.BINARY,
            500: inline_serializer(
                name='ErrorResponse',
                fields={'error': s.CharField()}
            )
        }
    )
    @action(detail=False, methods=['get'])
    def export_pdf(self, request):
        """
        Exportar inventario a PDF
        Query params: empresa (opcional) - filtrar por empresa
        """
        empresa_nit = request.query_params.get('empresa', None)
        
        try:
            from .services.pdf_generator import generate_inventory_pdf
            
            # Generar PDF
            pdf_path = generate_inventory_pdf(empresa_nit)
            
            # Verificar que el archivo existe
            if not os.path.exists(pdf_path):
                return Response(
                    {'error': 'Error al generar el PDF'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Retornar archivo PDF
            return FileResponse(
                open(pdf_path, 'rb'),
                as_attachment=True,
                filename=os.path.basename(pdf_path),
                content_type='application/pdf'
            )
        
        except Exception as e:
            return Response(
                {'error': f'Error al generar PDF: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @extend_schema(
        summary="Enviar PDF de inventario por email",
        description="Generar PDF del inventario y enviarlo por correo electrónico",
        request=inline_serializer(
            name='SendEmailRequest',
            fields={
                'email': s.EmailField(help_text='Email del destinatario'),
                'empresa': s.CharField(required=False, help_text='NIT de la empresa (opcional)')
            }
        ),
        responses={
            200: inline_serializer(
                name='SendEmailSuccess',
                fields={'message': s.CharField()}
            ),
            400: inline_serializer(
                name='SendEmailError',
                fields={'error': s.CharField()}
            )
        }
    )
    @action(detail=False, methods=['post'])
    def send_email(self, request):
        """
        Enviar PDF de inventario por email
        Body: {
            "empresa": "nit_empresa" (opcional),
            "email": "destinatario@example.com"
        }
        """
        email = request.data.get('email')
        empresa_nit = request.data.get('empresa', None)
        
        if not email:
            return Response(
                {'error': 'El campo email es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from .services.pdf_generator import generate_inventory_pdf
            from .services.email_service import send_pdf_via_email
            
            # Generar PDF
            pdf_path = generate_inventory_pdf(empresa_nit)
            
            # Enviar por email
            result = send_pdf_via_email(pdf_path, email)
            
            if result['success']:
                return Response({
                    'message': f'PDF enviado exitosamente a {email}'
                })
            else:
                return Response(
                    {'error': result['error']},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        except Exception as e:
            return Response(
                {'error': f'Error al enviar email: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
