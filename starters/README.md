# Starters Tecnológicos — Thronus Template

Starters são scaffolds tecnológicos aplicados **após** a fase `[ESTADO_ARCHITECTURE]`, uma vez que o ADR foi aprovado e a stack decidida. Nunca aplicar um starter antes de concluir a decisão arquitetural.

## Quando aplicar

1. Concluir `[ESTADO_ARCHITECTURE]` e ter o ADR aprovado.
2. Identificar qual starter corresponde ao stack decidido.
3. Copiar o conteúdo do starter sobre a raiz do projeto, complementando (não substituindo) a estrutura existente.
4. Ajustar os placeholders `{{PROJECT_NAME}}`, `{{CLIENT_NAME}}` se houver no starter.
5. Commitar: `chore: aplica starter <stack> conforme ADR-001`.

## Starters disponíveis

| Starter | Stack | Quando usar |
|---------|-------|-------------|
| `python-django/` | Python 3.11 + Django 5.1 + PostgreSQL | Sistemas de gestão, plataformas com admin, BI educacional |
| `python-fastapi/` | Python 3.11 + FastAPI + SQLAlchemy/PostgreSQL | APIs RESTful de alta performance, microsserviços |
| `node-express/` | Node.js 20 + Express + TypeScript | APIs REST leves, BFFs, integrações, webhooks |

## Criar um novo starter

Um starter mínimo precisa de:
```
starters/<nome>/
├── README.md            — instruções específicas do starter
├── .env.example         — variáveis de ambiente necessárias
├── pytest.ini / jest.config.ts / etc. — configuração de testes
├── .github/workflows/ci.yml — pipeline CI adaptado ao stack
└── src/{{PROJECT_NAME}}/ — scaffold inicial do código
```

Starters não incluem código de negócio — apenas infraestrutura, configuração e estrutura de pastas. A lógica de domínio é construída pelo pipeline TCA.

## Starters não listados

Se o stack decidido no ADR não tem starter correspondente, construir o scaffold manualmente durante `[ESTADO_ARCHITECTURE]` e opcionalmente criar um novo starter ao final do projeto para reutilização futura.
