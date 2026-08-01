# CLAUDE.md — Thronus Template

Este arquivo é carregado automaticamente em toda sessão Claude Code.
Execute `./thronus-init.sh` para inicializar um novo projeto com perfil de complexidade e stack tecnológico específicos.

---

# Thronus Context Architecture (TCA) — Hard Governance Policy

## 1. Diretriz de Autossuficiência (Zero Interaction Rule)

Este repositório opera sob execução autônoma em pipeline contínuo. O agente está TERMINANTEMENTE PROIBIDO de pausar a execução para solicitar aprovações humanas, exibir menus interativos ou exigir comandos manuais intermediários — **exceto pelos gates humanos explicitamente marcados no pipeline** (aprovação do ADR em Standard/Enterprise e gate único antes de escrever código em todo perfil).

## 2. Perfis de Complexidade

O pipeline TCA se adapta ao perfil do projeto. O perfil ativo está em `payload_index.json → estado_da_trilha.perfil` e seu detalhamento em `profiles/<perfil>.json`.

| Perfil | Escopo | Fases ativas |
|--------|--------|--------------|
| **nano** | Script, automação, POC. ≤5 MS | DISCOVERY (simplificado) → ARCHITECTURE (1 parágrafo) → SPEC → RED → GREEN → COMMIT |
| **micro** | API, MVP, portal simples. 5–15 MS | DISCOVERY → FUNCTIONAL (recomendado) → ARCHITECTURE → SPEC → PLAN → RED → GREEN → EDGE → COMMIT |
| **standard** | Sistema de gestão, SaaS, plataforma. 15–50 MS | Pipeline completo + 5 gates intermediários |
| **enterprise** | Sistema crítico, reescrita, contrato gov. 50+ MS | Pipeline completo + 7 gates + LGPD/compliance |

## 3. Pipeline TCA (Estado por Estado)

Toda solicitação de desenvolvimento deve acionar `docs/ThronusSpec/02_Setup/tcaOrchestratorSkill.md`.

**Fases Pré-Código (independentes de tecnologia):**
1. **[ESTADO_DISCOVERY]** → `discoverySkill.md` — Problema canônico, stakeholders, critérios de sucesso
2. **[ESTADO_FUNCTIONAL]** → `functionalModelingSkill.md` — Glossário, entidades, casos de uso, backlog de MSs
3. **[ESTADO_ARCHITECTURE]** → `architectureDecisionSkill.md` — ADR com score 4-dimensões, stack decidido por camada

**Ciclo TDD (após decisão de arquitetura):**
4. **[ESTADO_SPEC]** → `loadProjectPayloadSkill.md` — Carrega contexto e gera spec da MS ativa
5. **[ESTADO_PLAN]** → `evaluatePlanIntegritySkill.md` (MAX 3 iter.) + **gate humano obrigatório**
6. **[ESTADO_RED]** → Testes BDD com falha limpa comprovada
7. **[ESTADO_GREEN]** → Implementação produtiva, 100% verde
8. **[ESTADO_EDGE]** → `generateEdgeCaseTestsSkill.md` — Limites, payload corrompido, concorrência
9. **[ESTADO_COMMIT]** → Snapshot-diff gate + `monitorEvolutionMetricsSkill.md` + `gitCommitGuardSkill.md`

Rollbacks: PLAN→SPEC, GREEN→PLAN, EDGE→GREEN, EDGE→PLAN, COMMIT→ABORT.
Rollbacks pré-código: FUNCTIONAL→DISCOVERY, ARCHITECTURE→FUNCTIONAL.

---

# Projeto: {{PROJECT_NAME}} — {{CLIENT_NAME}}

**Descrição:** (preencher ao inicializar)
**Perfil de complexidade:** {{PERFIL}}
**Stack:** (definido após [ESTADO_ARCHITECTURE] — ver `docs/ThronusSpec/01_Planejamento/architecture_decision.md`)
**Estado da trilha:** Pendente | Próximo gate: `GATE_DISCOVERY`

---

## Comandos

```bash
# Os comandos abaixo são preenchidos após a decisão de arquitetura.
# Consulte docs/ThronusSpec/01_Planejamento/architecture_decision.md
# e o starter aplicado em starters/<stack>/.

# Testes (adaptar ao framework do projeto)
# pytest / jest / go test / cargo test / etc.

# Desenvolvimento local
# Consultar README.md gerado pelo starter tecnológico

# CI/CD
# Ver .github/workflows/ci.yml gerado pelo starter
```

---

## Arquitetura

> Preenchido após [ESTADO_ARCHITECTURE]. Os campos abaixo são exemplos; a estrutura real depende do stack decidido no ADR.

### Estrutura de camadas

```
src/{{PROJECT_NAME}}/
├── domain/          # Entidades e regras de negócio puras (sem dependências externas)
├── application/     # Casos de uso, ports (Protocol/Interface), serviços
│   ├── ports/       # Contratos das dependências externas (Port/Adapter)
│   └── services/    # Orquestração de casos de uso
└── infrastructure/  # Implementações concretas (DB, HTTP, email, etc.)
```

### Port/Adapter Pattern

Serviços de aplicação dependem de interfaces/contratos (em `application/ports/`), nunca de implementações concretas de infraestrutura. Isso permite testes unitários sem banco de dados ou rede.

### Invariantes críticos

- **Conventional Commits**: `type(scope): description [MS-NNN]` em todo commit.
- **Port/Adapter**: serviços nunca importam camada de infraestrutura diretamente.
- **EventoAuditoria (se aplicável)**: append-only — nunca modificar ou deletar registros existentes.

### Testes

Espelhamento estrutural obrigatório: `domain/ → tests/domain/`, `application/ → tests/application/`, `infrastructure/ → tests/infrastructure/`.

- `test_bdd_ms<NNN>_<descricao>` — cenários BDD (CT-01..CT-XX)
- `test_unit_ms<NNN>_<descricao>` — testes unitários puros (sem infraestrutura)
- `test_edge_ms<NNN>_<descricao>` — casos extremos (EDGE-01..STRESS-XX)

Cobertura mínima por perfil: nano=60% · micro=75% · standard=85% · enterprise=90%.

### Variáveis de ambiente

(Preenchido após decisão de arquitetura — adaptar ao stack escolhido.)
