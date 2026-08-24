# Projeto: {{PROJECT_NAME}} — {{CLIENT_NAME}}

> Parte do `AGENTS.md` que pertence a **este projeto**. É aqui que se edita nome,
> stack, comandos e estado. A metodologia fica em `tca/METODOLOGIA.md` e é canônica.
>
> Depois de editar, rode `tca agents --write` para regenerar o `AGENTS.md`.

**Descrição:** (preencher ao inicializar)
**Pacote de código:** `src/{{PACKAGE_NAME}}/` — slug de `{{PROJECT_NAME}}` com hífens trocados por `_`
**Perfil de complexidade:** {{PERFIL}}
**Stack:** (definido após [ESTADO_ARCHITECTURE] — ver `docs/ThronusSpec/01_Planejamento/architecture_decision.md`)
**Estado da trilha:** Pendente | Próximo gate: `GATE_DISCOVERY`

---

## Comandos

```bash
# Metodologia — disponíveis desde o início, em qualquer stack
tca verify                  # coerência dos artefatos de controle
tca doctor                  # divergência entre este projeto e o canon da TCA
tca close-ms MS-NNN --testes N

# Os comandos abaixo são preenchidos após a decisão de arquitetura.
# Consulte docs/ThronusSpec/01_Planejamento/architecture_decision.md
# e o starter aplicado em starters/<stack>/.

# Testes (adaptar ao framework do projeto)
# pytest / jest / go test / cargo test / etc.

# Desenvolvimento local
# Consultar README.md gerado pelo starter tecnológico

# CI/CD
# .github/workflows/governance.yml — checagens TCA, válidas em qualquer stack
# .github/workflows/ci.yml         — testes e lint, trazidos pelo starter
```

---

## Arquitetura

> Preenchido após [ESTADO_ARCHITECTURE]. Os campos abaixo são exemplos; a estrutura real depende do stack decidido no ADR.

### Estrutura de camadas

```
src/{{PACKAGE_NAME}}/
├── domain/          # Entidades e regras de negócio puras (sem dependências externas)
├── application/     # Casos de uso, ports (Protocol/Interface), serviços
│   ├── ports/       # Contratos das dependências externas (Port/Adapter)
│   └── services/    # Orquestração de casos de uso
└── infrastructure/  # Implementações concretas (DB, HTTP, email, etc.)
```

### Variáveis de ambiente

(Preenchido após decisão de arquitetura — adaptar ao stack escolhido.)

### Decisões e desvios deste projeto

Divergências deliberadas em relação à metodologia canônica são declaradas em
`tca-overrides.json`, com arquivo, motivo e responsável nomeado. Divergência não
declarada aparece no `tca doctor` e, em `--strict`, reprova.
