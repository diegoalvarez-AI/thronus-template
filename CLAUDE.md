# CLAUDE.md — Thronus Template

Este arquivo é carregado automaticamente em toda sessão Claude Code.
Substitua `{{PROJECT_NAME}}` e `{{CLIENT_NAME}}` ao inicializar um novo projeto
(ou execute `./thronus-init.sh <nome-projeto> <nome-cliente>`).

---

# Thronus Context Architecture (TCA) — Hard Governance Policy

## 1. Diretriz de Autossuficiência (Zero Interaction Rule)

Este repositório opera sob execução autônoma em pipeline contínuo. O agente está TERMINANTEMENTE PROIBIDO de pausar a execução para solicitar aprovações humanas, exibir menus interativos ou exigir comandos manuais intermediários — **exceto pelo gate único de aprovação humana após o ESTADO_PLAN**, que é obrigatório antes de escrever qualquer código produtivo.

## 2. Automação do Fluxo de Codificação (TDA State Machine v2)

Toda solicitação de desenvolvimento de Micro Spec deve acionar obrigatoriamente o Skill Central `docs/ThronusSpec/02_Setup/tcaOrchestratorSkill.md`. O agente processa as fases de forma síncrona, com rollbacks definidos:

1. **[ESTADO_SPEC]** → Invoca `loadProjectPayloadSkill.md` (carrega payload_index.json + spec da MS ativa).
2. **[ESTADO_PLAN]** → Gera estratégia técnica, auto-audita via `evaluatePlanIntegritySkill.md` (MAX 3 iterações). **Gate humano obrigatório antes de avançar.**
3. **[ESTADO_RED]** → Escreve testes BDD e comprova falha limpa (ImportError/AttributeError).
4. **[ESTADO_GREEN]** → Implementa código produtivo, roda suíte até 100% verde.
5. **[ESTADO_EDGE]** → Invoca `generateEdgeCaseTestsSkill.md`. Testes de limite, payload corrompido, concorrência, permissão.
6. **[ESTADO_COMMIT]** → Snapshot-diff gate + `monitorEvolutionMetricsSkill.md` + `gitCommitGuardSkill.md` + commit.

Rollbacks: PLAN→SPEC (max iterations), GREEN→PLAN (impossibilidade arquitetural), EDGE→GREEN (bug de lógica), EDGE→PLAN (falha arquitetural), COMMIT→ABORT (diff inesperado).

---

# Projeto: {{PROJECT_NAME}} — {{CLIENT_NAME}}

**Descrição:** (preencher ao inicializar)

**Stack:** Python 3.11 · Django 5.1 · PostgreSQL 16 (psycopg3) · Gunicorn · Nginx · Docker Compose
**Estado da trilha:** MS-001 pendente | Próximo gate: `GATE_001_SETUP`

---

## Comandos

```bash
# Testes (SQLite in-memory, sem PostgreSQL)
pytest                                   # suíte completa
pytest -k "CT-01"                        # filtro por cenário
pytest -m unit                           # apenas testes unitários (sem banco)
pytest -m integration                    # testes de integração (SQLite in-memory)

# Django
python src/app/infrastructure/manage.py migrate
python src/app/infrastructure/manage.py createsuperuser

# Docker
docker compose up --build
docker compose exec web python src/app/infrastructure/manage.py migrate
```

A variável `DJANGO_SETTINGS_MODULE` nos testes é definida via `pytest.ini` como `app.infrastructure.config.settings_test`.

---

## Arquitetura

### Estrutura de camadas (DDD)

```
src/app/
├── domain/              # Entidades puras, sem Django (@pytest.mark.unit)
├── application/         # Serviços de caso de uso, sem HTTP/ORM direto
│   ├── ports/           # Protocol interfaces (Port/Adapter)
│   ├── services/        # XxxService.metodo() → dataclass Resultado
│   └── validators/
└── infrastructure/
    ├── config/          # settings.py, settings_test.py, urls.py
    └── persistence/     # ÚNICO app Django registrado ("persistence")
        ├── models.py
        ├── admin.py
        ├── repositories.py  # Adapters Django para os Ports
        └── management/commands/
```

### Único app Django

Um único app Django com `app_label = "persistence"`. Todos os modelos, migrações e admin centralizados. O `INSTALLED_APPS` registra `"persistence.apps.PersistenceConfig"`.

O `pythonpath` no `pytest.ini` inclui `src` e `src/app/infrastructure`.

### Port/Adapter Pattern

Serviços de aplicação dependem de Protocols (em `application/ports/`), não do ORM diretamente. A infraestrutura fornece adaptadores Django em `persistence/repositories.py`. Isso permite testes `@pytest.mark.unit` sem banco de dados.

### Invariantes críticos

- **EventoAuditoria append-only**: `save()` com pk existente e `delete()` levantam `ValidationError`.
- **Port/Adapter**: services nunca importam `persistence.models` — usam apenas interfaces definidas em `application/ports/`.
- **Convencional Commits**: `type(scope): description [MS-NNN]` em todo commit.

### Testes

Espelhamento estrutural obrigatório: `domain/ → tests/domain/`, `application/services/ → tests/application/services/`, `infrastructure/ → tests/infrastructure/`.

- `test_bdd_ms<NNN>_<descricao>.py` — cenários BDD (CT-01..CT-XX)
- `test_unit_ms<NNN>_<descricao>.py` — testes unitários puros (`@pytest.mark.unit`, sem banco)
- `test_edge_ms<NNN>_<descricao>.py` — casos extremos (EDGE-01..STRESS-XX)

### Variáveis de ambiente (produção)

Obrigatórias: `SECRET_KEY`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `ALLOWED_HOSTS`.
Opcionais: `POSTGRES_PORT` (5432), `SENTRY_DSN`, `APP_RELEASE`, `DJANGO_DEBUG` (false).
