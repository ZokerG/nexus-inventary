from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.http import FileResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers as s
from apps.authentication.permissions import IsAdminUser
from .models import Inventario
from .serializers import InventarioSerializer
import os


@extend_schema(tags=['Inventario'])
class InventarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD en Inventario
    
    Solo administradores pueden gestionar inventario
    """
    queryset = Inventario.objects.all().select_related('empresa', 'producto')
    serializer_class = InventarioSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['empresa', 'producto']
    search_fields = ['empresa__nombre', 'producto__nombre']
    ordering_fields = ['fecha_registro', 'cantidad']
    
    @extend_schema(
        summary="Listar inventario",
        description="Obtener lista de todo el inventario (solo administradores)",
        parameters=[
            OpenApiParameter(name='empresa', description='Filtrar por NIT de empresa', type=OpenApiTypes.STR),
            OpenApiParameter(name='producto', description='Filtrar por código de producto', type=OpenApiTypes.STR),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Crear registro de inventario",
        description="Agregar un producto al inventario de una empresa (solo administradores)"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary="Obtener registro de inventario",
        description="Obtener detalles de un registro específico de inventario"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Actualizar inventario",
        description="Actualizar completamente un registro de inventario (solo administradores)"
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Actualizar inventario parcialmente",
        description="Actualizar parcialmente un registro de inventario (solo administradores)"
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Eliminar registro de inventario",
        description="Eliminar un registro de inventario (solo administradores)"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
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
