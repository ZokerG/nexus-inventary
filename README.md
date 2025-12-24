# 🚀 NEXUS - Sistema de Gestión de Inventario

Sistema completo de gestión de inventario desarrollado con **Django REST Framework** y **React**, con diseño moderno inspirado en dashboards profesionales.

![NEXUS Dashboard](https://img.shields.io/badge/Django-5.0-green) ![React](https://img.shields.io/badge/React-19.2-blue) ![Tailwind](https://img.shields.io/badge/Tailwind-3.4-cyan)

## 📋 Descripción

NEXUS es un sistema de gestión de inventario empresarial que permite administrar empresas, productos e inventario con funcionalidades avanzadas como:

- 🏢 **Gestión de Empresas** - CRUD completo de empresas con validaciones
- 📦 **Catálogo de Productos** - Productos con precios en múltiples monedas (COP, USD, EUR)
- 📊 **Control de Inventario** - Asignación de productos a empresas con seguimiento de stock
- 📄 **Exportación PDF** - Generación de reportes de inventario
- 📧 **Envío de Emails** - Envío automático de reportes por correo
- 📈 **Dashboard Analytics** - Métricas y estadísticas en tiempo real
- 🔐 **Autenticación JWT** - Sistema seguro con roles (Admin/Usuario Externo)
- 📚 **API REST Documentada** - OpenAPI/Swagger integrado

## 🎨 Características del Diseño

- **Tema Oscuro Profesional** - Inspirado en NEXUS con colores #0A0E1A, #161B26
- **Animaciones Suaves** - Hover effects, transiciones y escalado
- **Glassmorphism** - Efectos de transparencia y backdrop blur
- **Icons SVG** - Iconografía moderna sin dependencias
- **Responsive Design** - Adaptable a todos los dispositivos
- **Atomic Design** - Arquitectura de componentes escalable

## 🛠️ Tecnologías

### Backend
- **Django 5.0** - Framework web Python
- **Django REST Framework 3.14** - API REST
- **PostgreSQL** - Base de datos relacional
- **djangorestframework-simplejwt** - Autenticación JWT
- **drf-spectacular** - Documentación OpenAPI/Swagger
- **ReportLab** - Generación de PDFs
- **Django CORS Headers** - Manejo de CORS
- **python-decouple** - Gestión de variables de entorno

### Frontend
- **React 19.2.3** - Biblioteca UI
- **React Router DOM 7.11.0** - Navegación SPA
- **Axios 1.13.2** - Cliente HTTP
- **Tailwind CSS 3.4.1** - Framework CSS utility-first
- **PostCSS & Autoprefixer** - Procesamiento CSS

## 📦 Estructura del Proyecto

```
technical-test/
├── backend/
│   ├── apps/
│   │   ├── authentication/    # Autenticación y usuarios
│   │   ├── empresas/          # Gestión de empresas
│   │   ├── productos/         # Catálogo de productos
│   │   └── inventario/        # Control de inventario
│   ├── core/                  # Configuración Django
│   ├── manage.py
│   └── requirements.txt
│
└── frontend/
    ├── public/
    ├── src/
    │   ├── components/
    │   │   ├── atoms/         # Componentes básicos
    │   │   ├── molecules/     # Componentes compuestos
    │   │   ├── organisms/     # Componentes complejos
    │   │   ├── templates/     # Layouts
    │   │   └── pages/         # Páginas completas
    │   ├── context/           # React Context (Auth)
    │   ├── services/          # Servicios API
    │   └── App.js
    ├── package.json
    └── tailwind.config.js
```

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- npm o yarn

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/technical-test.git
cd technical-test
```

### 2. Configurar Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env
cp .env.example .env
# Editar .env con tus configuraciones:
# DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
# SECRET_KEY, DEBUG, ALLOWED_HOSTS

# Crear base de datos PostgreSQL
createdb nombre_de_tu_base_de_datos

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

El backend estará disponible en: `http://localhost:8000`
API Docs (Swagger): `http://localhost:8000/api/docs/`

### 3. Configurar Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm start
```

El frontend estará disponible en: `http://localhost:3000`

## 👤 Usuarios por Defecto

### Roles del Sistema

1. **ADMIN** - Acceso completo a todas las funcionalidades
   - Dashboard con métricas
   - CRUD Empresas
   - CRUD Productos
   - CRUD Inventario
   - Exportar PDF y enviar emails

2. **EXTERNO** - Acceso limitado
   - Dashboard con métricas
   - Ver Empresas (sin eliminar)

## 📡 Endpoints API Principales

### Autenticación
```
POST   /api/auth/register/          # Registro de usuario
POST   /api/auth/login/             # Login (obtener tokens)
POST   /api/auth/token/refresh/     # Refrescar token
GET    /api/auth/user/              # Obtener usuario actual
```

### Dashboard
```
GET    /api/dashboard/stats/        # Estadísticas generales
```

### Empresas
```
GET    /api/empresas/               # Listar empresas
POST   /api/empresas/               # Crear empresa
GET    /api/empresas/{nit}/         # Obtener empresa
PUT    /api/empresas/{nit}/         # Actualizar empresa
DELETE /api/empresas/{nit}/         # Eliminar empresa (Admin)
```

### Productos
```
GET    /api/productos/              # Listar productos
POST   /api/productos/              # Crear producto
GET    /api/productos/{codigo}/     # Obtener producto
PUT    /api/productos/{codigo}/     # Actualizar producto
DELETE /api/productos/{codigo}/     # Eliminar producto
```

### Inventario
```
GET    /api/inventario/                    # Listar inventario
POST   /api/inventario/                    # Crear registro
GET    /api/inventario/{id}/               # Obtener registro
PUT    /api/inventario/{id}/               # Actualizar registro
DELETE /api/inventario/{id}/               # Eliminar registro
GET    /api/inventario/export_pdf/         # Exportar PDF
POST   /api/inventario/send_email/         # Enviar email
```

## 🎯 Características Principales

### Dashboard
- **4 KPIs principales**: Empresas, Productos, Inventario Total, Valor Total
- **Empresas recientes**: Últimas empresas registradas
- **Productos top**: Productos con mayor stock
- **Inventario por empresa**: Cards con estadísticas
- **Actividad reciente**: Timeline de movimientos

### Empresas
- Búsqueda en tiempo real
- Filtrado y ordenamiento
- Validación de NIT (9-10 dígitos)
- Solo admin puede eliminar

### Productos
- Precios en 3 monedas simultáneas
- Búsqueda por código, nombre o características
- Validación de precios
- CRUD completo

### Inventario
- Asignación producto-empresa
- Indicadores de stock visuales:
  - 🔴 Rojo: Sin stock (0)
  - 🟡 Amarillo: Stock bajo (<10)
  - 🟢 Verde: Stock normal (≥10)
- Exportación a PDF con filtros
- Envío automático por email
- Búsqueda y filtrado avanzado

## 🎨 Paleta de Colores

```css
/* Backgrounds */
--bg-primary: #0F1419
--bg-secondary: #0A0E1A
--bg-card: #161B26

/* Borders */
--border-primary: rgba(148, 163, 184, 0.1)
--border-secondary: rgba(148, 163, 184, 0.05)

/* Text */
--text-primary: #FFFFFF
--text-secondary: #94A3B8
--text-tertiary: #64748B

/* Accent Colors */
--blue: #3B82F6
--green: #10B981
--purple: #8B5CF6
--orange: #F97316
--red: #EF4444
```

## 📝 Scripts Disponibles

### Backend
```bash
python manage.py runserver          # Iniciar servidor
python manage.py migrate            # Aplicar migraciones
python manage.py makemigrations     # Crear migraciones
python manage.py createsuperuser    # Crear admin
python manage.py test               # Ejecutar tests
```

### Frontend
```bash
npm start           # Iniciar desarrollo
npm run build       # Build producción
npm test            # Ejecutar tests
npm run eject       # Eject de CRA
```

## 🔒 Variables de Entorno

### Backend (.env)
```env
# Database
DB_NAME=inventario_db
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=tu_secret_key_segura
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email (opcional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_password_app
```

### Frontend (.env.local)
```env
REACT_APP_API_URL=http://localhost:8000/api
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto fue desarrollado como prueba técnica.

## 👨‍💻 Autor

**Tu Nombre**
- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- LinkedIn: [Tu Perfil](https://linkedin.com/in/tu-perfil)

## 📸 Screenshots

### Login
![Login](docs/screenshots/login.png)

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### Empresas
![Empresas](docs/screenshots/empresas.png)

### Productos
![Productos](docs/screenshots/productos.png)

### Inventario
![Inventario](docs/screenshots/inventario.png)

---

⭐️ Si te gusta este proyecto, no olvides darle una estrella!
