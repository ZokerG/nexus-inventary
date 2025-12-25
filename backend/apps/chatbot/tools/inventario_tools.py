from apps.inventario.models import Inventario
from apps.inventario.serializers import InventarioSerializer
from apps.productos.models import Producto
from apps.empresas.models import Empresa
from django.contrib.auth import get_user_model

User = get_user_model()


def update_inventario(empresa_nit: str, producto_codigo: str, cantidad: int, user_email: str = "") -> dict:
    """Actualiza o crea un registro de inventario.
    
    Args:
        empresa_nit: NIT de la empresa
        producto_codigo: Código del producto
        cantidad: Cantidad en inventario
        user_email: Email del usuario que ejecuta la acción
        
    Returns:
        Diccionario con el resultado de la operación
    """
    try:
        # Validar permisos
        user = User.objects.get(email=user_email)
        if not user.is_admin:
            return {
                "success": False,
                "error": "Permisos insuficientes",
                "message": "🔒 Solo los administradores pueden actualizar inventario"
            }
        
        # Verificar empresa y producto
        try:
            empresa = Empresa.objects.get(nit=empresa_nit)
            producto = Producto.objects.get(codigo=producto_codigo)
        except Empresa.DoesNotExist:
            return {
                "success": False,
                "error": "Empresa no encontrada",
                "message": f"❌ No existe empresa con NIT {empresa_nit}"
            }
        except Producto.DoesNotExist:
            return {
                "success": False,
                "error": "Producto no encontrado",
                "message": f"❌ No existe producto con código {producto_codigo}"
            }
        
        # Buscar o crear inventario
        inventario, created = Inventario.objects.update_or_create(
            empresa=empresa,
            producto=producto,
            defaults={
                'cantidad': cantidad
            }
        )
        
        action = "registrado" if created else "actualizado"
        
        return {
            "success": True,
            "data": InventarioSerializer(inventario).data,
            "message": f"✅ Inventario {action}: {cantidad} unidades de {producto.nombre} para {empresa.nombre}"
        }
    
    except User.DoesNotExist:
        return {
            "success": False,
            "error": "Usuario no encontrado",
            "message": "❌ Error de autenticación"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"❌ Error al actualizar inventario: {str(e)}"
        }


def get_inventario(empresa_nit: str = "", user_email: str = "") -> dict:
    """Consulta el inventario con filtro opcional por empresa.
    
    Args:
        empresa_nit: NIT de la empresa para filtrar (opcional)
        user_email: Email del usuario que ejecuta la acción
        
    Returns:
        Diccionario con el inventario
    """
    try:
        queryset = Inventario.objects.select_related('empresa', 'producto').all()
        
        if empresa_nit:
            queryset = queryset.filter(empresa__nit=empresa_nit)
        
        inventarios = queryset
        total = queryset.count()
        
        filtro_msg = f" de empresa {empresa_nit}" if empresa_nit else ""
        
        return {
            "success": True,
            "data": InventarioSerializer(inventarios, many=True).data,
            "total": total,
            "message": f"📋 Inventario{filtro_msg}: {total} registros"
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"❌ Error al consultar inventario: {str(e)}"
        }


def delete_inventario(inventario_id: int, user_email: str) -> dict:
    """Elimina un registro de inventario.
    
    Args:
        inventario_id: ID del registro de inventario a eliminar
        user_email: Email del usuario que ejecuta la acción
        
    Returns:
        Diccionario con el resultado de la operación
    """
    try:
        # Validar permisos
        user = User.objects.get(email=user_email)
        if not user.is_admin:
            return {
                "success": False,
                "error": "Permisos insuficientes",
                "message": "🔒 Solo los administradores pueden eliminar registros de inventario"
            }
        
        inventario = Inventario.objects.select_related('empresa', 'producto').get(id=inventario_id)
        empresa = inventario.empresa.nombre
        producto = inventario.producto.nombre
        
        inventario.delete()
        
        return {
            "success": True,
            "message": f"🗑️ Registro de inventario eliminado: {producto} de {empresa}"
        }
    
    except Inventario.DoesNotExist:
        return {
            "success": False,
            "error": "Inventario no encontrado",
            "message": f"❌ No existe registro de inventario con ID {inventario_id}"
        }
    except User.DoesNotExist:
        return {
            "success": False,
            "error": "Usuario no encontrado",
            "message": "❌ Error de autenticación"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"❌ Error al eliminar inventario: {str(e)}"
        }
