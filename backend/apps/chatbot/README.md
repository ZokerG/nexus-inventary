# 🤖 Chatbot AI con Gemini

Sistema de chatbot inteligente que permite gestionar el inventario mediante lenguaje natural usando **Gemini 2.5 Flash** con **Function Calling automático**.

## 📋 Características

### ✨ Capacidades del Chatbot

- **Multi-turn Conversations**: Mantiene contexto entre mensajes
- **Function Calling Automático**: Gemini ejecuta funciones Python automáticamente
- **Context Caching**: Reduce costos en 75% usando caché de 1 hora
- **Sistema Multi-modal**: Soporta texto, imágenes (futuro)
- **Permisos por Rol**: Admin (CRUD completo) vs Usuario Externo (solo lectura)

### 🛠️ Funciones Disponibles

#### Empresas (5 funciones)
- `create_empresa`: Crear nueva empresa (Admin)
- `list_empresas`: Listar empresas con filtros
- `get_empresa`: Obtener detalles de empresa
- `update_empresa`: Actualizar empresa (Admin)
- `delete_empresa`: Eliminar empresa (Admin)

#### Productos (4 funciones)
- `create_producto`: Crear producto con precios (Admin)
- `list_productos`: Listar productos con filtros
- `get_producto`: Obtener detalles de producto
- `delete_producto`: Eliminar producto (Admin)

#### Inventario (3 funciones)
- `update_inventario`: Crear/actualizar inventario (Admin)
- `get_inventario`: Consultar inventario
- `delete_inventario`: Eliminar registro de inventario (Admin)

#### Analytics (3 funciones)
- `get_dashboard_stats`: Obtener estadísticas del dashboard
- `export_pdf_inventario`: Exportar inventario a PDF
- `send_email_inventario`: Enviar reporte por email (Admin)

## 🚀 Configuración

### 1. Variables de Entorno

Agregar a tu archivo `.env`:

```env
GEMINI_API_KEY=tu_api_key_de_google_ai_studio
```

**Obtener API Key**: https://aistudio.google.com/apikey

### 2. Ejecutar Migraciones

```bash
python manage.py makemigrations chatbot
python manage.py migrate
```

## 📡 Endpoints API

### POST `/api/chatbot/message/`
Enviar mensaje al chatbot

**Request:**
```json
{
  "message": "Lista todas las empresas",
  "session_id": 1  // Opcional, se crea automáticamente
}
```

**Response:**
```json
{
  "session_id": 1,
  "message": "✅ Aquí están las empresas registradas:\n\n1. **TechCorp** (NIT: 123456789)\n...",
  "tool_calls": [
    {
      "function": "list_empresas",
      "arguments": {"user_email": "admin@example.com"}
    }
  ],
  "created_at": "2025-01-15T10:30:00Z"
}
```

### GET `/api/chatbot/history/?session_id=1`
Obtener historial de una sesión

### GET `/api/chatbot/sessions/`
Listar todas las sesiones del usuario

### DELETE `/api/chatbot/sessions/delete/?session_id=1`
Eliminar una sesión

## 💡 Ejemplos de Uso

### Usuario Admin
```
Usuario: "Crea una empresa llamada TechCorp con NIT 123456789"
Bot: ✅ Empresa TechCorp creada exitosamente

Usuario: "Agrega un producto Laptop Dell al inventario de TechCorp"
Bot: ✅ Producto creado con código PROD-001

Usuario: "Actualiza el inventario a 50 unidades en bodega principal"
Bot: ✅ Inventario actualizado: 50 unidades en bodega principal
```

### Usuario Externo
```
Usuario: "¿Cuántas empresas hay registradas?"
Bot: 📊 Hay 5 empresas registradas en el sistema

Usuario: "¿Qué productos tiene TechCorp?"
Bot: 📦 TechCorp tiene 3 productos:
1. Laptop Dell - $1200
2. Mouse Logitech - $25
3. Teclado Mecánico - $80

Usuario: "Elimina la empresa TechCorp"
Bot: 🔒 No tienes permisos para eliminar empresas. Solo usuarios administradores pueden realizar esta acción.
```

## 🏗️ Arquitectura

```
apps/chatbot/
├── models.py                    # ChatSession, ChatMessage
├── serializers.py               # API serializers
├── views.py                     # API endpoints
├── admin.py                     # Django admin
├── services/
│   └── gemini_service.py        # Integración con Gemini SDK
└── tools/
    ├── registry.py              # Registro de funciones
    ├── empresa_tools.py         # Funciones de empresas
    ├── producto_tools.py        # Funciones de productos
    ├── inventario_tools.py      # Funciones de inventario
    └── analytics_tools.py       # Funciones de analytics
```

## 💰 Optimización de Costos

### Context Caching
- **Ahorro**: 75% en tokens repetidos
- **TTL**: 1 hora (renovable automáticamente)
- **Qué se cachea**: System instructions + contexto del usuario

### Precios Gemini 2.5 Flash
- **Input**: $0.00001875 / 1K tokens (sin caché)
- **Cached Input**: $0.000004688 / 1K tokens (75% descuento)
- **Output**: $0.000075 / 1K tokens

**Ejemplo de ahorro:**
- Sin caché: 100 mensajes × 2000 tokens = $3.75
- Con caché: 100 mensajes × 2000 tokens = $1.09
- **Ahorro: $2.66 (71%)**

## 🔐 Sistema de Permisos

### Admin (`is_admin=True`)
- ✅ Crear, editar, eliminar empresas
- ✅ Crear, editar, eliminar productos
- ✅ Actualizar y eliminar inventario
- ✅ Enviar emails con reportes
- ✅ Todas las funciones de lectura

### Usuario Externo (`is_admin=False`)
- ✅ Listar empresas y productos
- ✅ Consultar inventario
- ✅ Ver estadísticas
- ✅ Exportar PDFs
- ❌ Crear, editar o eliminar

## 🧪 Testing

### Probar desde Swagger UI
1. Ir a `http://localhost:8000/api/docs/`
2. Autenticarse con JWT token
3. POST a `/api/chatbot/message/`
4. Enviar mensaje: `"Lista las empresas"`

### Probar desde cURL
```bash
curl -X POST http://localhost:8000/api/chatbot/message/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Lista todas las empresas"}'
```

## 📊 Modelos de Base de Datos

### ChatSession
- `user`: Usuario propietario
- `gemini_cache_name`: Nombre del caché en Gemini
- `cache_expires_at`: Fecha de expiración del caché
- `is_active`: Si la sesión está activa
- `created_at`, `updated_at`: Timestamps

### ChatMessage
- `session`: Sesión a la que pertenece
- `role`: `user`, `model`, o `tool`
- `content`: Contenido del mensaje
- `tool_calls`: JSON con llamadas a funciones (opcional)
- `created_at`: Timestamp

## 🔍 Troubleshooting

### Error: "GEMINI_API_KEY not configured"
- Asegúrate de tener `GEMINI_API_KEY` en tu `.env`
- Verifica que el valor no esté vacío

### Error: "User does not have permission"
- El usuario necesita `is_admin=True` para acciones de escritura
- Verifica el rol del usuario en Django admin

### Caché expirado
- El caché se renueva automáticamente si faltan < 15 minutos
- Si hay error, se crea nuevo caché automáticamente

## 📚 Referencias

- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Function Calling Guide](https://ai.google.dev/gemini-api/docs/function-calling)
- [Context Caching](https://ai.google.dev/gemini-api/docs/caching)
- [Google AI Python SDK](https://github.com/googleapis/python-genai)
