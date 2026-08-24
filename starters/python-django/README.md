# Starter: python-django

**Stack:** Python 3.11 · Django 5.1 · PostgreSQL 16 · Gunicorn · WhiteNoise · pytest-django · ruff

**Quando usar:** sistemas de gestão, plataformas com área administrativa, BI educacional — projetos que se beneficiam do Django Admin e de um ORM maduro.

## Aplicar este starter

```bash
./apply-starter.sh python-django
```

O script renomeia `src/{{PACKAGE_NAME}}/` para o slug real do projeto e resolve os placeholders. Não copie o diretório manualmente: o nome do pacote não seria substituído.

## Estrutura gerada

```
src/{{PACKAGE_NAME}}/
├── domain/                       # Entidades e regras de negócio puras (sem Django)
├── application/
│   ├── ports/                    # Protocols — contratos das dependências externas
│   └── services/                 # Casos de uso, dependem só de ports
└── infrastructure/
    ├── config/                   # settings.py, settings_test.py, urls.py
    └── persistence/              # models.py, repositories.py (adapters), admin.py

tests/
├── domain/
├── application/services/
└── infrastructure/
```

`pythonpath` em `pytest.ini` inclui `src/{{PACKAGE_NAME}}/infrastructure`, o que torna `config` e `persistence` importáveis como pacotes de topo — é o que `ROOT_URLCONF = "config.urls"` e `INSTALLED_APPS = ["persistence.apps.PersistenceConfig"]` esperam.

## Comandos

```bash
# Testes (SQLite in-memory)
pytest
pytest -m unit           # sem banco
pytest -m integration    # com SQLite in-memory

# Lint
ruff check src/ tests/ --select F541,F811

# Desenvolvimento local
python -m django runserver --settings={{PACKAGE_NAME}}.infrastructure.config.settings

# Migrations
python -m django makemigrations persistence --settings={{PACKAGE_NAME}}.infrastructure.config.settings
python -m django migrate --settings={{PACKAGE_NAME}}.infrastructure.config.settings
```

## Variáveis de ambiente

Copie `.env.example` para `.env`. Em produção, `SECRET_KEY`, `ALLOWED_HOSTS` e todas as `POSTGRES_*` são obrigatórias — `settings.py` levanta `ImproperlyConfigured` se faltarem.

## O que vem junto

| Arquivo | Papel |
|---|---|
| `requirements.txt` / `requirements-dev.txt` | dependências de produção e de desenvolvimento |
| `pytest.ini` / `conftest.py` | configuração da suíte e fixtures globais |
| `pyproject.toml` | configuração do ruff |
| `.pre-commit-config.yaml` | hook de lint |
| `.github/workflows/ci.yml` | lint + suíte completa (complementa `governance.yml` da raiz) |
| `.env.example` | variáveis necessárias |

## Invariante já implementado

`EventoAuditoria` (`persistence/models.py`) é append-only: `save()` com pk existente e `delete()` levantam exceção, e o admin bloqueia adicionar, alterar e excluir.
