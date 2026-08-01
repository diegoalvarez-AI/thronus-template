# Starter: python-fastapi

**Stack:** Python 3.11 · FastAPI · SQLAlchemy 2 (async) · PostgreSQL 16 · Alembic · Uvicorn · Docker Compose

**Quando usar:** APIs RESTful de alta performance, microsserviços, backends desacoplados de frontend SPA.

## Aplicar este starter

```bash
cp -r starters/python-fastapi/. .
sed -i "s/{{PROJECT_NAME}}/<nome-projeto>/g" $(find . -type f -name "*.py" -o -name "*.toml" -o -name "*.yml")
pip install -r requirements-dev.txt
```

## Estrutura gerada

```
src/{{PROJECT_NAME}}/
├── domain/              # Entidades e regras de negócio puras
├── application/
│   ├── ports/           # Protocol interfaces (Port/Adapter)
│   └── services/        # Casos de uso
└── infrastructure/
    ├── config/          # settings.py (pydantic-settings), .env loader
    ├── persistence/     # SQLAlchemy models, Alembic migrations, repositories
    └── api/             # FastAPI routers, schemas Pydantic, dependencies

tests/
├── domain/
├── application/services/
└── infrastructure/
```

## Comandos

```bash
# Testes (SQLite in-memory via pytest-asyncio)
pytest
pytest -m unit           # sem banco
pytest -m integration    # SQLite in-memory

# Desenvolvimento local
uvicorn src.{{PROJECT_NAME}}.infrastructure.api.main:app --reload

# Migrations (Alembic)
alembic upgrade head
alembic revision --autogenerate -m "ms001_descricao"

# Docker
docker compose up --build
```

## Variáveis de ambiente

```
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/db
SECRET_KEY=<gerar com: python -c "import secrets; print(secrets.token_hex(32))">
ENVIRONMENT=development
SENTRY_DSN=          # opcional
```

> Scaffold detalhado será adicionado em versão futura. Por enquanto, use este README como referência de estrutura e adapte manualmente após [ESTADO_ARCHITECTURE].
