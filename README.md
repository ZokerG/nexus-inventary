# 🚀 NEXUS - Sistema de Gestión de Inventario con Clean Architecture

[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-19.2-blue.svg)](https://reactjs.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-yellow.svg)](https://www.python.org/)
[![Clean Architecture](https://img.shields.io/badge/Architecture-Clean-orange.svg)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
[![Tests](https://img.shields.io/badge/Tests-61%20passing-brightgreen.svg)](./domain/tests/)
[![Coverage](https://img.shields.io/badge/Coverage-84%25-green.svg)](./domain/)

Sistema empresarial de gestión de inventario con **Clean Architecture**, desarrollado con Django REST Framework y React. Implementa separación completa de la lógica de negocio usando principios SOLID y arquitectura hexagonal.

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Tecnologías](#️-tecnologías)
- [Instalación](#-instalación-rápida)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Clean Architecture](#-clean-architecture-implementation)

---

## ✨ Características

### Funcionalidades del Sistema

- 🏢 **Gestión de Empresas** - CRUD completo con validaciones de NIT y teléfono
- 📦 **Catálogo de Productos** - Productos con características y precios multi-moneda (COP, USD, EUR, MXN)
- 📊 **Control de Inventario** - Asignación de productos por empresa con seguimiento de stock en tiempo real
- 📄 **Exportación PDF** - Generación de reportes profesionales de inventario
- 📧 **Envío de Emails** - Distribución automática de reportes por correo
- 📈 **Dashboard Analytics** - Métricas y estadísticas empresariales
- 🤖 **Chatbot IA** - Asistente virtual con OpenAI para consultas de inventario
- 🔐 **Autenticación JWT** - Sistema seguro con roles (Admin/Usuario Externo)
- 📚 **API REST Documentada** - OpenAPI/Swagger integrado

### Características Técnicas

- ✅ **Clean Architecture** - Dominio 100% independiente de frameworks
- ✅ **SOLID Principles** - Código mantenible y escalable
- ✅ **Hexagonal Architecture** - Inversión de dependencias
- ✅ **Domain-Driven Design** - Entidades, Value Objects, Use Cases
- ✅ **Repository Pattern** - Abstracción de persistencia
- ✅ **Unit Testing** - 61 tests del dominio con 84% cobertura
- ✅ **Type Hints** - Python tipado estáticamente
- ✅ **Atomic Design** - Componentes React reutilizables

---

## 🏗️ Arquitectura

### Clean Architecture en Capas

```
┌─────────────────────────────────────────────────────────────────┐
│                     CAPA DE PRESENTACIÓN                         │
│              (Django REST Framework + React)                     │
│  • ViewSets con inyección de dependencias                        │
│  • Mapeo de excepciones de dominio → HTTP status codes           │
│  • Serialización con entity.to_dict()                            │
└──────────────────────────────┬──────────────────────────────────┘
                               │ depende de ↓
┌─────────────────────────────────────────────────────────────────┐
│                     CAPA DE APLICACIÓN                           │
│                  (Use Cases - nexus-domain)                      │
│  • CreateEmpresaUseCase, ListEmpresasUseCase                     │
│  • CreateProductoUseCase, UpdateProductoUseCase                  │
│  • AddStockUseCase, RemoveStockUseCase                           │
│  • Orquestación de lógica de negocio                             │
└──────────────────────────────┬──────────────────────────────────┘
                               │ depende de ↓
┌─────────────────────────────────────────────────────────────────┐
│                        CAPA DE DOMINIO                           │
│           (Entidades + Value Objects - Python Puro)              │
│  • EmpresaEntity, ProductoEntity, InventarioEntity               │
│  • NIT, Phone, Money, ProductCode, Quantity                      │
│  • Validaciones de negocio encapsuladas                          │
│  • 0 dependencias de frameworks (100% portable)                  │
└──────────────────────────────┬──────────────────────────────────┘
                               ↑ implementa ↓
┌─────────────────────────────────────────────────────────────────┐
│                    CAPA DE INFRAESTRUCTURA                       │
│              (Repositorios Django + Mappers)                     │
│  • DjangoEmpresaRepository → IEmpresaRepository                  │
│  • Mappers bidireccionales (Entity ↔ ORM)                        │
│  • Django ORM Models (orm_models.py)                             │
└──────────────────────────────┬──────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                       BASE DE DATOS                              │
│                    (PostgreSQL / SQLite)                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tecnologías

### Dominio (Python Puro)
- Python 3.11+ | Pydantic 2.5+ | Poetry | Pytest

### Backend
- Django 5.0 | Django REST Framework | PostgreSQL | JWT | OpenAI API

### Frontend
- React 19.2 | React Router | Axios | Tailwind CSS | Vite

---

## 📦 Instalación Rápida

### Prerrequisitos

- Python 3.11+
- Poetry: `pip install poetry`
- Node.js 18+ y npm
- PostgreSQL (opcional)

### Pasos de Instalación

```bash
# 1. Clonar repositorio
git clone https://github.com/ZokerG/nexus-inventary.git
cd nexus-inventary

# 2. Configurar dominio (Python puro)
cd domain
poetry env use python3.11
poetry install
poetry run pytest  # ✅ 61 passed

# 3. Configurar backend
cd ../backend
python -m venv venv

# Windows:
.\venv\Scripts\Activate.ps1

# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
pip install -e ../domain/

# 4. Configurar base de datos
# Crear archivo .env con:
echo "DEBUG=True
SECRET_KEY=tu-clave-secreta-cambiar
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3" > .env

# 5. Ejecutar migraciones
python manage.py migrate
python manage.py createsuperuser

# 6. Verificar instalación
python manage.py check  # ✅ 0 issues

# 7. Iniciar backend
python manage.py runserver
# ✅ http://127.0.0.1:8000/

# 8. Configurar frontend (nueva terminal)
cd frontend
npm install
npm run dev
# ✅ http://localhost:5173/
```

---

## 💻 Uso

### Acceso al Sistema

- **Frontend**: http://localhost:5173/
- **Backend API**: http://127.0.0.1:8000/api/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Docs**: http://127.0.0.1:8000/api/docs/

### Ejemplo de Uso con cURL

```bash
# 1. Login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# 2. Crear empresa
curl -X POST http://127.0.0.1:8000/api/empresas/ \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "nit": "900123456-1",
    "nombre": "Empresa Demo SA",
    "direccion": "Calle 123",
    "telefono": "+57 300 1234567"
  }'
```

---

## 📁 Estructura del Proyecto

```
nexus-inventary/
│
├── domain/                          # 🔷 DOMINIO (Python Puro)
│   ├── nexus_domain/
│   │   ├── entities/                # Empresa, Producto, Inventario
│   │   ├── value_objects/           # NIT, Phone, Money, etc.
│   │   ├── interfaces/              # IEmpresaRepository, etc.
│   │   ├── use_cases/               # CreateEmpresaUseCase, etc.
│   │   └── exceptions/              # ValidationError, etc.
│   ├── tests/                       # 61 tests (84% coverage)
│   └── pyproject.toml
│
├── backend/                         # 🔷 INFRAESTRUCTURA
│   ├── apps/
│   │   ├── empresas/
│   │   │   ├── orm_models.py        # Django ORM
│   │   │   ├── mappers.py           # Entity ↔ ORM
│   │   │   ├── repositories.py      # DjangoEmpresaRepository
│   │   │   ├── views.py             # ViewSets + Use Cases
│   │   │   └── models.py            # Re-exports
│   │   ├── productos/
│   │   ├── inventario/
│   │   ├── chatbot/
│   │   └── authentication/
│   ├── manage.py
│   └── requirements.txt
│
└── frontend/                        # 🔷 PRESENTACIÓN
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   └── services/
    └── package.json
```

---

## 📚 API Documentation

### Endpoints Principales

```http
# Autenticación
POST   /api/auth/login/
POST   /api/auth/register/

# Empresas
GET    /api/empresas/              # Listar
POST   /api/empresas/              # Crear
GET    /api/empresas/{nit}/        # Detalle
PUT    /api/empresas/{nit}/        # Actualizar
DELETE /api/empresas/{nit}/        # Eliminar

# Productos
GET    /api/productos/
POST   /api/productos/
GET    /api/productos/{codigo}/
PUT    /api/productos/{codigo}/
DELETE /api/productos/{codigo}/

# Inventario
GET    /api/inventario/
POST   /api/inventario/
POST   /api/inventario/add-stock/
POST   /api/inventario/remove-stock/
GET    /api/inventario/export-pdf/
```

**Swagger UI**: http://127.0.0.1:8000/api/docs/

---

## 🧪 Testing

### Tests del Dominio (Unitarios)

```bash
cd domain

# Ejecutar tests
poetry run pytest

# Con cobertura
poetry run pytest --cov=nexus_domain --cov-report=html

# Resultado esperado:
# ======================== 61 passed in 1.82s ========================
# Coverage: 84%
```

### Tests de Integración (Django)

```bash
cd backend
python manage.py test apps.empresas
python manage.py test apps.productos
python manage.py test apps.inventario
```

---

## 🏛️ Clean Architecture Implementation

### Principios Aplicados

#### 1. **Independencia de Frameworks**
```python
# ✅ Dominio sin Django
@dataclass
class Empresa:
    nit: NIT
    nombre: str
    # Sin models.Model
```

#### 2. **Inversión de Dependencias**
```python
# ✅ Dominio define interfaz
class IEmpresaRepository(ABC):
    @abstractmethod
    def save(self, empresa: Empresa) -> Empresa:
        pass

# ✅ Django implementa
class DjangoEmpresaRepository(IEmpresaRepository):
    def save(self, empresa: Empresa) -> Empresa:
        # Django ORM
```

#### 3. **Testabilidad**
```python
# ✅ Tests sin base de datos
mock_repo = MockEmpresaRepository()
use_case = CreateEmpresaUseCase(mock_repo)
# Ejecuta en milisegundos
```

### Comparación

| Aspecto | Antes | Después |
|---------|-------|---------|
| Tests | ~30s (con DB) | <2s (sin DB) |
| Acoplamiento | Alto | Bajo |
| Reutilización | Solo Django | Portable |
| Mantenimiento | Complejo | Simple |

---

## 🤝 Contribución

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE)

---

## 👥 Autores

**NEXUS Team** - [ZokerG](https://github.com/ZokerG)

---

## 🙏 Agradecimientos

- Inspirado en **Clean Architecture** de Robert C. Martin (Uncle Bob)
- Principios de Domain-Driven Design
- Comunidad de Django y React

---

**⭐ Si este proyecto te fue útil, dale una estrella en GitHub!**
