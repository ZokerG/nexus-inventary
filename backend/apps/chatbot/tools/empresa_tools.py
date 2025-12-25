from apps.empresas.models import Empresa
from apps.empresas.serializers import EmpresaSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


def create_empresa(nit: str, nombre: str, direccion: str, telefono: str, user_email: str) -> dict:
    """Crea una nueva empresa en el sistema.
    
    Args:
        nit: NIT de la empresa (9-10 dígitos)
        nombre: Nombre de la empresa
        direccion: Dirección física de la empresa
        telefono: Teléfono de contacto (7-10 dígitos)
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
                "error": "Solo los administradores pueden crear empresas",
                "message": "🔒 No tienes permisos para crear empresas. Esta acción requiere rol de administrador."
            }
        
        # Verificar si ya existe
        if Empresa.objects.filter(nit=nit).exists():
            return {
                "success": False,
                "error": "Empresa ya existe",
                "message": f"❌ Ya existe una empresa con NIT {nit}"
            }
        
        # Crear empresa
        empresa = Empresa.objects.create(
            nit=nit,
            nombre=nombre,
            direccion=direccion,
            telefono=telefono
        )
        
        return {
            "success": True,
            "data": EmpresaSerializer(empresa).data,
            "message": f"✅ Empresa {nombre} creada exitosamente con NIT {nit}"
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
            "message": f"❌ Error al crear empresa: {str(e)}"
        }


def list_empresas(filtro: str = "", limit: int = 10, user_email: str = "") -> dict:
    """Lista las empresas del sistema con filtro opcional.
    
    Args:
        filtro: Filtro por nombre de empresa (opcional)
        limit: Número máximo de resultados
        user_email: Email del usuario que ejecuta la acción
        
    Returns:
        Diccionario con la lista de empresas
    """
    try:
        queryset = Empresa.objects.all()
        
        if filtro:
            queryset = queryset.filter(nombre__icontains=filtro)
        
        empresas = queryset[:limit]
        total = queryset.count()
        
        return {
            "success": True,
            "data": EmpresaSerializer(empresas, many=True).data,
            "total": total,
            "message": f"📊 Encontradas {len(empresas)} empresas" + (f" que coinciden con '{filtro}'" if filtro else "")
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"❌ Error al listar empresas: {str(e)}"
        }


def get_empresa(nit: str, user_email: str) -> dict:
    """Obtiene los detalles de una empresa específica.
    
    Args:
        nit: NIT de la empresa a consultar
        user_email: Email del usuario que ejecuta la acción
        
    Returns:
        Diccionario con los detalles de la empresa
    """
    try:
        empresa = Empresa.objects.get(nit=nit)
        
        return {
            "success": True,
            "data": EmpresaSerializer(empresa).data,
            "message": f"📋 Detalles de {empresa.nombre}"
        }
    
    except Empresa.DoesNotExist:
        return {
            "success": False,
            "error": "Empresa no encontrada",
            "message": f"❌ No existe empresa con NIT {nit}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"❌ Error al obtener empresa: {str(e)}"
        }


def update_empresa(nit: str, nombre: str = None, direccion: str = None, telefono: str = None, user_email: str = "") -> dict:
    """Actualiza los datos de una empresa existente.
    
    Args:
        nit: NIT de la empresa a actualizar
        nombre: Nuevo nombre (opcional)
        direccion: Nueva dirección (opcional)
        telefono: Nuevo teléfono (opcional)
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
                "message": "🔒 Solo los administradores pueden editar empresas"
            }
        
        empresa = Empresa.objects.get(nit=nit)
        
        if nombre:
            empresa.nombre = nombre
        if direccion:
            empresa.direccion = direccion
        if telefono:
            empresa.telefono = telefono
        
        empresa.save()
        
        return {
            "success": True,
            "data": EmpresaSerializer(empresa).data,
            "message": f"✅ Empresa {empresa.nombre} actualizada exitosamente"
        }
    
    except Empresa.DoesNotExist:
        return {
            "success": False,
            "error": "Empresa no encontrada",
            "message": f"❌ No existe empresa con NIT {nit}"
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
            "message": f"❌ Error al actualizar empresa: {str(e)}"
        }


def delete_empresa(nit: str, user_email: str) -> dict:
    """Elimina una empresa del sistema.
    
    Args:
        nit: NIT de la empresa a eliminar
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
                "message": "🔒 Solo los administradores pueden eliminar empresas"
            }
        
        empresa = Empresa.objects.get(nit=nit)
        nombre = empresa.nombre
        empresa.delete()
        
        return {
            "success": True,
            "message": f"🗑️ Empresa {nombre} (NIT: {nit}) eliminada exitosamente"
        }
    
    except Empresa.DoesNotExist:
        return {
            "success": False,
            "error": "Empresa no encontrada",
            "message": f"❌ No existe empresa con NIT {nit}"
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
            "message": f"❌ Error al eliminar empresa: {str(e)}"
        }
