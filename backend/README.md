# Backend - Sistema de Gestión de Inventario

Backend desarrollado con Django REST Framework para la gestión de empresas, productos e inventario.

## Requisitos

- Python 3.10+
- PostgreSQL 14+

## Instalación

1. **Crear entorno virtual:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. **Instalar dependencias:**
```powershell
pip install -r requirements.txt
```

3. **Configurar variables de entorno:**
Copiar `.env.example` a `.env` y configurar:
```env
SECRET_KEY=tu-clave-secreta
DEBUG=True
DB_NAME=technical_test_db
DB_USER=postgres
DB_PASSWORD=tu-password
DB_HOST=localhost
DB_PORT=5432

# Para envío de emails (opcional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-password-app
```

4. **Crear base de datos en PostgreSQL:**
```sql
CREATE DATABASE technical_test_db;
```

5. **Ejecutar migraciones:**
```powershell
python manage.py makemigrations
python manage.py migrate
```

6. **Crear superusuario:**
```powershell
python manage.py createsuperuser
```

7. **Ejecutar servidor:**
```powershell
python manage.py runserver
```

## Endpoints API

### Autenticación
- `POST /api/auth/register/` - Registro de usuario
- `POST /api/auth/login/` - Login (retorna JWT token)
- `GET /api/auth/profile/` - Perfil del usuario autenticado
- `POST /api/auth/token/refresh/` - Refrescar token

### Empresas
- `GET /api/empresas/` - Listar empresas (todos los usuarios)
- `POST /api/empresas/` - Crear empresa (solo admin)
- `GET /api/empresas/{nit}/` - Detalle de empresa
- `PUT /api/empresas/{nit}/` - Actualizar empresa (solo admin)
- `DELETE /api/empresas/{nit}/` - Eliminar empresa (solo admin)

### Productos
- `GET /api/productos/` - Listar productos (solo admin)
- `POST /api/productos/` - Crear producto (solo admin)
- `GET /api/productos/{codigo}/` - Detalle de producto (solo admin)
- `PUT /api/productos/{codigo}/` - Actualizar producto (solo admin)
- `DELETE /api/productos/{codigo}/` - Eliminar producto (solo admin)

### Inventario
- `GET /api/inventario/` - Listar inventario (solo admin)
- `POST /api/inventario/` - Agregar al inventario (solo admin)
- `GET /api/inventario/export_pdf/?empresa={nit}` - Exportar PDF (solo admin)
- `POST /api/inventario/send_email/` - Enviar PDF por email (solo admin)

## Roles de Usuario

- **ADMIN**: Acceso completo (CRUD de empresas, productos e inventario)
- **EXTERNO**: Solo lectura de empresas

## Estructura del Proyecto

```
backend/
├── config/              # Configuración Django
├── apps/
│   ├── authentication/  # Usuarios y autenticación JWT
│   ├── empresas/        # CRUD de empresas
│   ├── productos/       # CRUD de productos con precios multi-moneda
│   └── inventario/      # Gestión de inventario + PDF + Email
├── media/               # Archivos generados (PDFs)
├── requirements.txt
└── manage.py
```

## Ejemplos de Uso

### 1. Registro de Usuario
```bash
POST /api/auth/register/
{
  "email": "admin@example.com",
  "username": "admin",
  "password": "SecurePass123!",
  "role": "ADMIN"
}
```

### 2. Login
```bash
POST /api/auth/login/
{
  "email": "admin@example.com",
  "password": "SecurePass123!"
}
```

### 3. Crear Empresa (con token)
```bash
POST /api/empresas/
Headers: Authorization: Bearer {access_token}
{
  "nit": "900123456",
  "nombre": "Empresa XYZ",
  "direccion": "Calle 123",
  "telefono": "3001234567"
}
```

### 4. Crear Producto con Precios
```bash
POST /api/productos/
Headers: Authorization: Bearer {access_token}
{
  "codigo": "PROD001",
  "nombre": "Laptop Dell",
  "caracteristicas": {
    "ram": "16GB",
    "cpu": "Intel i7"
  },
  "empresa": "900123456",
  "precios": [
    {"moneda": "USD", "precio": 1200.00},
    {"moneda": "COP", "precio": 4800000.00}
  ]
}
```

### 5. Agregar a Inventario
```bash
POST /api/inventario/
Headers: Authorization: Bearer {access_token}
{
  "empresa": "900123456",
  "producto": "PROD001",
  "cantidad": 50
}
```

### 6. Exportar PDF
```bash
GET /api/inventario/export_pdf/?empresa=900123456
Headers: Authorization: Bearer {access_token}
```

### 7. Enviar PDF por Email
```bash
POST /api/inventario/send_email/
Headers: Authorization: Bearer {access_token}
{
  "empresa": "900123456",
  "email": "cliente@example.com"
}
```

## Notas

- Los tokens JWT expiran en 60 minutos (configurable en settings)
- Los PDFs se generan en `/media/pdfs/`
- Para envío de emails, configurar SMTP en `.env`
