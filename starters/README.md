# Starters Tecnológicos — Thronus Template

Starters são scaffolds tecnológicos aplicados **após** a fase `[ESTADO_ARCHITECTURE]`, uma vez que o ADR foi aprovado e a stack decidida. Nunca aplicar um starter antes de concluir a decisão arquitetural.

A raiz do template é deliberadamente agnóstica de stack: não traz dependências, runner de testes, `.env.example` nem CI de build. Tudo isso mora aqui dentro. Na raiz fica apenas `.github/workflows/governance.yml`, com checagens válidas para qualquer linguagem.

## Como aplicar

```bash
./apply-starter.sh python-django
```

O script:

1. valida que o ADR existe em `docs/ThronusSpec/01_Planejamento/architecture_decision.md`;
2. copia `starters/<stack>/` sobre a raiz, complementando a estrutura existente;
3. renomeia os diretórios `{{PACKAGE_NAME}}` para o slug real do projeto;
4. substitui `{{PROJECT_NAME}}`, `{{PACKAGE_NAME}}`, `{{CLIENT_NAME}}`, `{{PERFIL}}` e `{{DATA_INICIO}}` no conteúdo dos arquivos;
5. registra o starter aplicado em `.thronus-template-version`;
6. instala os hooks de `pre-commit`, se o starter trouxer configuração.

Depois: `git add -A && git commit -m "chore: aplica starter <stack> conforme ADR-001"`.

> **Placeholders dentro de `starters/` são preservados por `thronus-init.sh`.** Um starter é um template dentro do template — só `apply-starter.sh` os resolve.

## Starters disponíveis

| Starter | Stack | Situação | Quando usar |
|---------|-------|----------|-------------|
| `python-django/` | Python 3.11 + Django 5.1 + PostgreSQL | **Scaffold completo** — aplicável via `apply-starter.sh` | Sistemas de gestão, plataformas com admin, BI educacional |
| `python-fastapi/` | Python 3.11 + FastAPI + SQLAlchemy/PostgreSQL | **Somente referência** — README com estrutura; scaffold manual | APIs RESTful de alta performance, microsserviços |
| `node-express/` | Node.js 20 + Express + TypeScript | **Somente referência** — README com estrutura; scaffold manual | APIs REST leves, BFFs, integrações, webhooks |

Starters marcados como *somente referência* não têm código: `apply-starter.sh` detecta a ausência de `src/`, avisa e encerra sem alterar nada. Use o README do starter como guia para montar o scaffold manualmente durante `[ESTADO_ARCHITECTURE]`.

## Nomes: `{{PROJECT_NAME}}` vs `{{PACKAGE_NAME}}`

| Placeholder | Exemplo | Onde usar |
|---|---|---|
| `{{PROJECT_NAME}}` | `migrador-dados` | nome do repositório, títulos, documentação, descrições |
| `{{PACKAGE_NAME}}` | `migrador_dados` | diretórios de código (`src/`), imports, módulos de settings |

Nome de projeto aceita hífen; identificador de pacote não — Python, Go e Java rejeitam. `thronus-init.sh` deriva `{{PACKAGE_NAME}}` trocando `-` por `_`.

## Criar um novo starter

Um starter mínimo precisa de:

```
starters/<nome>/
├── README.md                    — stack, comandos, variáveis de ambiente
├── .env.example                 — variáveis necessárias
├── <config de testes>           — pytest.ini / jest.config.ts / etc.
├── <manifesto de dependências>  — requirements.txt / package.json / go.mod
├── .github/workflows/ci.yml     — build, lint e testes do stack
└── src/{{PACKAGE_NAME}}/        — scaffold inicial (use o placeholder no nome do diretório)
```

Regras:

- Use `{{PACKAGE_NAME}}` no **nome** do diretório de código — `apply-starter.sh` o renomeia.
- Não inclua `.github/workflows/governance.yml`: ele é da raiz e vale para toda stack. Nomear o workflow do starter como `ci.yml` evita sobrescrevê-lo.
- Starters não incluem código de negócio — apenas infraestrutura, configuração e estrutura de pastas. A lógica de domínio é construída pelo pipeline TCA.

Ao terminar, acrescente a linha na tabela acima com a situação real do starter.
