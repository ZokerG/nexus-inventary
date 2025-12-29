# NEXUS Domain Layer

Capa de dominio del sistema NEXUS - Clean Architecture

## Descripción

Este paquete contiene la lógica de negocio pura del sistema NEXUS, completamente desacoplada de frameworks e infraestructura.

## Estructura

```
nexus_domain/
├── entities/          # Entidades de negocio
├── value_objects/     # Value Objects inmutables
├── interfaces/        # Contratos/Interfaces abstractas
├── use_cases/         # Casos de uso del negocio
└── exceptions/        # Excepciones del dominio
```

## Principios

- **Sin dependencias de Django**: Solo Python puro
- **Lógica de negocio encapsulada**: Reglas en entidades
- **Inmutabilidad**: Value Objects inmutables
- **Interfaces abstractas**: Desacoplamiento de infraestructura

## Instalación

```bash
poetry install
```

## Testing

```bash
poetry run pytest
poetry run pytest --cov=nexus_domain
```

## Uso desde Backend

```python
from nexus_domain.entities import Empresa
from nexus_domain.use_cases import CreateEmpresaUseCase
from nexus_domain.value_objects import NIT
```
