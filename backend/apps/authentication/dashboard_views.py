from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum, Avg
from drf_spectacular.utils import extend_schema
from apps.empresas.models import Empresa
from apps.productos.models import Producto, PrecioMoneda
from apps.inventario.models import Inventario


@extend_schema(tags=['Dashboard'])
class DashboardStatsView(APIView):
    """
    Obtener estadísticas generales del sistema
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Estadísticas del dashboard",
        description="Obtener métricas generales: empresas, productos, inventario, valores, etc."
    )
    def get(self, request):
        user = request.user

        # Estadísticas básicas
        total_empresas = Empresa.objects.count()
        total_productos = Producto.objects.count()
        total_inventario = Inventario.objects.aggregate(total=Sum('cantidad'))['total'] or 0

        # Empresas recientes
        empresas_recientes = Empresa.objects.order_by('-created_at')[:5].values(
            'nit', 'nombre', 'telefono', 'created_at'
        )

        # Productos más registrados en inventario
        productos_top = Inventario.objects.values(
            'producto__codigo',
            'producto__nombre',
            'producto__empresa__nombre'
        ).annotate(
            total_cantidad=Sum('cantidad')
        ).order_by('-total_cantidad')[:5]

        # Inventario por empresa
        inventario_por_empresa = Inventario.objects.values(
            'empresa__nit',
            'empresa__nombre'
        ).annotate(
            total_productos=Count('producto'),
            total_cantidad=Sum('cantidad')
        ).order_by('-total_cantidad')[:5]

        # Valor total estimado (precios en COP)
        valor_total = 0
        inventarios = Inventario.objects.select_related('producto').prefetch_related('producto__precios')
        for inv in inventarios:
            precio_cop = inv.producto.precios.filter(moneda='COP').first()
            if precio_cop:
                valor_total += float(precio_cop.precio) * inv.cantidad

        # Distribución de productos por empresa
        productos_por_empresa = Producto.objects.values(
            'empresa__nombre'
        ).annotate(
            total=Count('codigo')
        ).order_by('-total')[:5]

        # Estadísticas de usuario
        user_stats = {
            'nombre': f"{user.first_name} {user.last_name}",
            'email': user.email,
            'rol': user.get_role_display(),
            'es_admin': user.is_admin
        }

        # Actividad reciente (últimos registros)
        actividad_reciente = []
        
        # Últimas empresas
        for emp in Empresa.objects.order_by('-created_at')[:3]:
            actividad_reciente.append({
                'tipo': 'empresa',
                'descripcion': f'Empresa "{emp.nombre}" registrada',
                'fecha': emp.created_at
            })
        
        # Últimos productos
        for prod in Producto.objects.order_by('-created_at')[:3]:
            actividad_reciente.append({
                'tipo': 'producto',
                'descripcion': f'Producto "{prod.nombre}" creado',
                'fecha': prod.created_at
            })

        # Ordenar por fecha
        actividad_reciente.sort(key=lambda x: x['fecha'], reverse=True)
        actividad_reciente = actividad_reciente[:5]

        data = {
            'resumen': {
                'total_empresas': total_empresas,
                'total_productos': total_productos,
                'total_inventario': total_inventario,
                'valor_total_cop': round(valor_total, 2)
            },
            'empresas_recientes': list(empresas_recientes),
            'productos_top': list(productos_top),
            'inventario_por_empresa': list(inventario_por_empresa),
            'productos_por_empresa': list(productos_por_empresa),
            'usuario': user_stats,
            'actividad_reciente': actividad_reciente
        }

        return Response(data)
