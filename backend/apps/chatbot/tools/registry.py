from .empresa_tools import (
    create_empresa,
    list_empresas,
    get_empresa,
    update_empresa,
    delete_empresa
)
from .producto_tools import (
    create_producto,
    list_productos,
    get_producto,
    delete_producto
)
from .inventario_tools import (
    update_inventario,
    get_inventario,
    delete_inventario
)
from .analytics_tools import (
    get_dashboard_stats,
    export_pdf_inventario,
    send_email_inventario
)
from .function_declarations import get_all_function_declarations


def get_all_tools():
    """Retorna todas las declaraciones de funciones para Gemini"""
    return get_all_function_declarations()


def get_function_map():
    """Retorna un diccionario que mapea nombres de funciones a las funciones reales"""
    return {
        # Empresas
        'create_empresa': create_empresa,
        'list_empresas': list_empresas,
        'get_empresa': get_empresa,
        'update_empresa': update_empresa,
        'delete_empresa': delete_empresa,
        
        # Productos
        'create_producto': create_producto,
        'list_productos': list_productos,
        'get_producto': get_producto,
        'delete_producto': delete_producto,
        
        # Inventario
        'update_inventario': update_inventario,
        'get_inventario': get_inventario,
        'delete_inventario': delete_inventario,
        
        # Analytics
        'get_dashboard_stats': get_dashboard_stats,
        'export_pdf_inventario': export_pdf_inventario,
        'send_email_inventario': send_email_inventario
    }
