"""Declaraciones de funciones para Gemini Function Calling"""
from google.genai import types


# Declaraciones de funciones para Empresas
create_empresa_declaration = types.FunctionDeclaration(
    name="create_empresa",
    description="Crea una nueva empresa en el sistema",
    parameters={
        "type": "OBJECT",
        "properties": {
            "nit": {"type": "STRING", "description": "NIT único de la empresa"},
            "nombre": {"type": "STRING", "description": "Nombre de la empresa"},
            "direccion": {"type": "STRING", "description": "Dirección física de la empresa"},
            "telefono": {"type": "STRING", "description": "Teléfono de contacto"},
            "user_email": {"type": "STRING", "description": "Email del usuario que ejecuta la acción"}
        },
        "required": ["nit", "nombre", "direccion", "telefono", "user_email"]
    }
)

list_empresas_declaration = types.FunctionDeclaration(
    name="list_empresas",
    description="Lista todas las empresas registradas con filtros opcionales",
    parameters={
        "type": "OBJECT",
        "properties": {
            "filtro": {"type": "STRING", "description": "Filtro opcional por nombre"},
            "limit": {"type": "INTEGER", "description": "Límite de resultados (default 10)"},
            "user_email": {"type": "STRING", "description": "Email del usuario"}
        },
        "required": ["user_email"]
    }
)

get_empresa_declaration = types.FunctionDeclaration(
    name="get_empresa",
    description="Obtiene los detalles de una empresa específica por su NIT",
    parameters={
        "type": "OBJECT",
        "properties": {
            "nit": {"type": "STRING", "description": "NIT de la empresa a consultar"},
            "user_email": {"type": "STRING", "description": "Email del usuario"}
        },
        "required": ["nit", "user_email"]
    }
)

update_empresa_declaration = types.FunctionDeclaration(
    name="update_empresa",
    description="Actualiza los datos de una empresa existente",
    parameters={
        "type": "OBJECT",
        "properties": {
            "nit": {"type": "STRING", "description": "NIT de la empresa a actualizar"},
            "nombre": {"type": "STRING", "description": "Nuevo nombre (opcional)"},
            "direccion": {"type": "STRING", "description": "Nueva dirección (opcional)"},
            "telefono": {"type": "STRING", "description": "Nuevo teléfono (opcional)"},
            "user_email": {"type": "STRING", "description": "Email del usuario"}
        },
        "required": ["nit", "user_email"]
    }
)

delete_empresa_declaration = types.FunctionDeclaration(
    name="delete_empresa",
    description="Elimina una empresa del sistema",
    parameters={
        "type": "OBJECT",
        "properties": {
            "nit": {"type": "STRING", "description": "NIT de la empresa a eliminar"},
            "user_email": {"type": "STRING", "description": "Email del usuario"}
        },
        "required": ["nit", "user_email"]
    }
)

# Declaraciones de funciones para Productos
create_producto_declaration = types.FunctionDeclaration(
    name="create_producto",
    description="Crea un nuevo producto asociado a una empresa",
    parameters={
        "type": "OBJECT",
        "properties": {
            "codigo": {"type": "STRING", "description": "Código único del producto"},
            "nombre": {"type": "STRING", "description": "Nombre del producto"},
            "empresa_nit": {"type": "STRING", "description": "NIT de la empresa"},
            "caracteristicas": {"type": "STRING", "description": "Características del producto (opcional)"},
            "user_email": {"type": "STRING", "description": "Email del usuario"}
        },
        "required": ["codigo", "nombre", "empresa_nit", "user_email"]
    }
)

list_productos_declaration = types.FunctionDeclaration(
    name="list_productos",
    description="Lista todos los productos con filtros opcionales",
    parameters={
        "type": "OBJECT",
        "properties": {
            "empresa_nit": {"type": "STRING", "description": "Filtrar por NIT de empresa (opcional)"},
            "nombre_filtro": {"type": "STRING", "description": "Filtrar por nombre (opcional)"},
            "limit": {"type": "INTEGER", "description": "Límite de resultados (default 10)"},
            "user_email": {"type": "STRING", "description": "Email del usuario"}
        },
        "required": ["user_email"]
    }
)

get_producto_declaration = types.FunctionDeclaration(
    name="get_producto",
    description="Obtiene los detalles de un producto específico por su código",
    parameters={
        "type": "OBJECT",
        "properties": {
            "codigo": {"type": "STRING", "description": "Código del producto"},
            "user_email": {"type": "STRING", "description": "Email del usuario"}
        },
        "required": ["codigo", "user_email"]
    }
)

delete_producto_declaration = types.FunctionDeclaration(
    name="delete_producto",
    description="Elimina un producto del sistema",
    parameters={
        "type": "OBJECT",
        "properties": {
            "codigo": {"type": "STRING", "description": "Código del producto a eliminar"},
            "user_email": {"type": "STRING", "description": "Email del usuario"}
        },
        "required": ["codigo", "user_email"]
    }
)

# Declaraciones para Inventario
update_inventario_declaration = types.FunctionDeclaration(
    name="update_inventario",
    description="Actualiza o crea un registro de inventario",
    parameters={
        "type": "OBJECT",
        "properties": {
            "empresa_nit": {"type": "STRING", "description": "NIT de la empresa"},
            "producto_codigo": {"type": "STRING", "description": "Código del producto"},
            "cantidad": {"type": "INTEGER", "description": "Cantidad en inventario"},
            "user_email": {"type": "STRING", "description": "Email del usuario"}
        },
        "required": ["empresa_nit", "producto_codigo", "cantidad", "user_email"]
    }
)

get_inventario_declaration = types.FunctionDeclaration(
    name="get_inventario",
    description="Consulta el inventario completo o filtrado por empresa",
    parameters={
        "type": "OBJECT",
        "properties": {
            "empresa_nit": {"type": "STRING", "description": "Filtrar por NIT de empresa (opcional)"},
            "user_email": {"type": "STRING", "description": "Email del usuario"}
        },
        "required": ["user_email"]
    }
)

delete_inventario_declaration = types.FunctionDeclaration(
    name="delete_inventario",
    description="Elimina un registro de inventario por su ID",
    parameters={
        "type": "OBJECT",
        "properties": {
            "inventario_id": {"type": "INTEGER", "description": "ID del registro de inventario"},
            "user_email": {"type": "STRING", "description": "Email del usuario"}
        },
        "required": ["inventario_id", "user_email"]
    }
)

# Declaraciones para Analytics
get_dashboard_stats_declaration = types.FunctionDeclaration(
    name="get_dashboard_stats",
    description="Obtiene estadísticas generales del sistema (empresas, productos, inventario)",
    parameters={
        "type": "OBJECT",
        "properties": {
            "user_email": {"type": "STRING", "description": "Email del usuario"}
        },
        "required": ["user_email"]
    }
)

export_pdf_inventario_declaration = types.FunctionDeclaration(
    name="export_pdf_inventario",
    description="Genera un reporte PDF del inventario",
    parameters={
        "type": "OBJECT",
        "properties": {
            "empresa_nit": {"type": "STRING", "description": "NIT de la empresa (opcional)"},
            "user_email": {"type": "STRING", "description": "Email del usuario"}
        },
        "required": ["user_email"]
    }
)

send_email_inventario_declaration = types.FunctionDeclaration(
    name="send_email_inventario",
    description="Envía un reporte de inventario por email",
    parameters={
        "type": "OBJECT",
        "properties": {
            "email": {"type": "STRING", "description": "Email destino"},
            "empresa_nit": {"type": "STRING", "description": "NIT de la empresa (opcional)"},
            "user_email": {"type": "STRING", "description": "Email del usuario que ejecuta"}
        },
        "required": ["email", "user_email"]
    }
)


def get_all_function_declarations():
    """Retorna todas las declaraciones de funciones para Gemini"""
    return [
        create_empresa_declaration,
        list_empresas_declaration,
        get_empresa_declaration,
        update_empresa_declaration,
        delete_empresa_declaration,
        create_producto_declaration,
        list_productos_declaration,
        get_producto_declaration,
        delete_producto_declaration,
        update_inventario_declaration,
        get_inventario_declaration,
        delete_inventario_declaration,
        get_dashboard_stats_declaration,
        export_pdf_inventario_declaration,
        send_email_inventario_declaration,
    ]
