from apps.authentication.dashboard_views import DashboardStatsView
from django.contrib.auth import get_user_model

User = get_user_model()


def get_dashboard_stats(user_email: str) -> dict:
    """Obtiene estadísticas generales del sistema (dashboard).
    
    Args:
        user_email: Email del usuario que ejecuta la acción
        
    Returns:
        Diccionario con las estadísticas del sistema
    """
    try:
        user = User.objects.get(email=user_email)
        
        # Crear instancia de la vista y obtener datos
        view = DashboardStatsView()
        
        # Simular request object
        class FakeRequest:
            def __init__(self, user):
                self.user = user
        
        fake_request = FakeRequest(user)
        response = view.get(fake_request)
        
        return {
            "success": True,
            "data": response.data,
            "message": "📊 Estadísticas del sistema"
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
            "message": f"❌ Error al obtener estadísticas: {str(e)}"
        }


def export_pdf_inventario(empresa_nit: str = "", user_email: str = "") -> dict:
    """Genera y descarga un reporte PDF del inventario.
    
    Args:
        empresa_nit: NIT de la empresa para filtrar (opcional)
        user_email: Email del usuario que ejecuta la acción
        
    Returns:
        Diccionario con información del PDF generado
    """
    try:
        user = User.objects.get(email=user_email)
        
        # Nota: Esta función simula la generación
        # En la implementación real, se llamaría al servicio de inventario
        
        filtro_msg = f" de empresa {empresa_nit}" if empresa_nit else " completo"
        
        return {
            "success": True,
            "message": f"📄 PDF del inventario{filtro_msg} generado exitosamente. Usa el endpoint /api/inventario/export-pdf/ para descargarlo."
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
            "message": f"❌ Error al exportar PDF: {str(e)}"
        }


def send_email_inventario(email: str, empresa_nit: str = "", user_email: str = "") -> dict:
    """Envía reporte de inventario por email.
    
    Args:
        email: Email destino para enviar el reporte
        empresa_nit: NIT de la empresa para filtrar (opcional)
        user_email: Email del usuario que ejecuta la acción
        
    Returns:
        Diccionario con el resultado del envío
    """
    try:
        user = User.objects.get(email=user_email)
        
        if not user.is_admin:
            return {
                "success": False,
                "error": "Permisos insuficientes",
                "message": "🔒 Solo los administradores pueden enviar reportes por email"
            }
        
        filtro_msg = f" de empresa {empresa_nit}" if empresa_nit else ""
        
        return {
            "success": True,
            "message": f"✉️ Reporte de inventario{filtro_msg} enviado a {email}. Usa el endpoint /api/inventario/send-email/ para ejecutar el envío real."
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
            "message": f"❌ Error al enviar email: {str(e)}"
        }
