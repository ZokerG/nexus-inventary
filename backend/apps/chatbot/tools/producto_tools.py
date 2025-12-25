from apps.productos.models import Producto, PrecioMoneda
from apps.productos.serializers import ProductoSerializer
from apps.empresas.models import Empresa
from django.contrib.auth import get_user_model

User = get_user_model()


def create_producto(codigo: str, nombre: str, empresa_nit: str, caracteristicas: str = "", user_email: str = "") -> dict:
    """Crea un nuevo producto asociado a una empresa.
    
    Args:
        codigo: Código único del producto
        nombre: Nombre del producto
        empresa_nit: NIT de la empresa a la que pertenece
        caracteristicas: Características del producto (opcional)
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
                "message": "🔒 Solo los administradores pueden crear productos"
            }
        
        # Verificar que la empresa existe
        try:
            empresa = Empresa.objects.get(nit=empresa_nit)
        except Empresa.DoesNotExist:
            return {
                "success": False,
                "error": "Empresa no encontrada",
                "message": f"❌ No existe empresa con NIT {empresa_nit}. Créala primero."
            }
        
        # Verificar si el producto ya existe
        if Producto.objects.filter(codigo=codigo).exists():
            return {
                "success": False,
                "error": "Producto ya existe",
                "message": f"❌ Ya existe un producto con código {codigo}"
            }
        
        # Crear producto
        producto = Producto.objects.create(
            codigo=codigo,
            nombre=nombre,
            caracteristicas=caracteristicas or "",
            empresa=empresa,
            created_by=user
        )
        
        # Crear precio por defecto en COP
        PrecioMoneda.objects.create(
            producto=producto,
            moneda='COP',
            precio=0  # El usuario puede actualizarlo después
        )
        
        return {
            "success": True,
            "data": ProductoSerializer(producto).data,
            "message": f"✅ Producto {nombre} creado exitosamente con código {codigo}"
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
            "message": f"❌ Error al crear producto: {str(e)}"
        }


def list_productos(empresa_nit: str = "", nombre_filtro: str = "", limit: int = 10, user_email: str = "") -> dict:
    """Lista productos del sistema con filtros opcionales.
    
    Args:
        empresa_nit: Filtrar por NIT de empresa (opcional)
        nombre_filtro: Filtrar por nombre de producto (opcional)
        limit: Número máximo de resultados
        user_email: Email del usuario que ejecuta la acción
        
    Returns:
        Diccionario con la lista de productos
    """
    try:
        queryset = Producto.objects.select_related('empresa').prefetch_related('precios')
        
        if empresa_nit:
            queryset = queryset.filter(empresa__nit=empresa_nit)
        
        if nombre_filtro:
            queryset = queryset.filter(nombre__icontains=nombre_filtro)
        
        productos = queryset[:limit]
        total = queryset.count()
        
        filtros_msg = []
        if empresa_nit:
            filtros_msg.append(f"empresa {empresa_nit}")
        if nombre_filtro:
            filtros_msg.append(f"nombre '{nombre_filtro}'")
        
        filtros_texto = " con " + " y ".join(filtros_msg) if filtros_msg else ""
        
        return {
            "success": True,
            "data": ProductoSerializer(productos, many=True).data,
            "total": total,
            "message": f"📦 Encontrados {len(productos)} productos{filtros_texto}"
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"❌ Error al listar productos: {str(e)}"
        }


def get_producto(codigo: str, user_email: str) -> dict:
    """Obtiene los detalles de un producto específico.
    
    Args:
        codigo: Código del producto a consultar
        user_email: Email del usuario que ejecuta la acción
        
    Returns:
        Diccionario con los detalles del producto
    """
    try:
        producto = Producto.objects.select_related('empresa').prefetch_related('precios').get(codigo=codigo)
        
        return {
            "success": True,
            "data": ProductoSerializer(producto).data,
            "message": f"📋 Detalles de {producto.nombre}"
        }
    
    except Producto.DoesNotExist:
        return {
            "success": False,
            "error": "Producto no encontrado",
            "message": f"❌ No existe producto con código {codigo}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"❌ Error al obtener producto: {str(e)}"
        }


def delete_producto(codigo: str, user_email: str) -> dict:
    """Elimina un producto del sistema.
    
    Args:
        codigo: Código del producto a eliminar
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
                "message": "🔒 Solo los administradores pueden eliminar productos"
            }
        
        producto = Producto.objects.get(codigo=codigo)
        nombre = producto.nombre
        producto.delete()
        
        return {
            "success": True,
            "message": f"🗑️ Producto {nombre} (código: {codigo}) eliminado exitosamente"
        }
    
    except Producto.DoesNotExist:
        return {
            "success": False,
            "error": "Producto no encontrado",
            "message": f"❌ No existe producto con código {codigo}"
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
            "message": f"❌ Error al eliminar producto: {str(e)}"
        }
