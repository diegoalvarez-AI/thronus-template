# AGENTS.md — Thronus Template

> **Arquivo canônico da metodologia.** Vale para qualquer agente de código
> (Claude Code, Codex, Cursor, Gemini CLI, Aider, ou execução humana).
> `CLAUDE.md` apenas importa este arquivo — não duplique conteúdo lá.

Execute `./thronus-init.sh` para inicializar um novo projeto com perfil de complexidade específico.
Após o ADR, execute `./apply-starter.sh <stack>` para aplicar o scaffold tecnológico.

---

# 0. Contrato de Harness

A metodologia TCA é **independente de harness**: nenhuma fase depende de uma ferramenta
proprietária. O pipeline exige apenas as capacidades abaixo. Onde o harness não oferece a
capacidade nativa, use o *fallback* — o resultado do pipeline é o mesmo, só muda o meio.

| ID | Capacidade | Obrigatória | Fallback quando ausente |
|----|-----------|:---:|---|
| **CAP-FS** | Ler e escrever arquivos do repositório | sim | — (sem isso o pipeline não roda) |
| **CAP-SHELL** | Executar comandos de shell (`git`, runner de testes) | sim | — (sem isso o pipeline não roda) |
| **CAP-SEARCH** | Busca dirigida em arquivos grandes, idealmente delegada a um subagente de exploração | não | `grep -n` para localizar o ponto de inserção, depois leitura só da faixa de linhas relevante |
| **CAP-PLAN** | Modo de plano dedicado, que separa planejar de editar | não | Escrever o plano na seção `## Plano` de `context/activeContext.md` e não tocar em nenhum arquivo produtivo até o gate humano |
| **CAP-GATE** | Interromper a execução e aguardar resposta humana | sim | Emitir o bloco `[TCA_INTEGRITY_CHECK]`, **encerrar o turno** e aguardar nova invocação com a aprovação |
| **CAP-SUBAGENT** | Executar trabalho isolado em contexto separado | não | Executar em sequência no mesmo contexto, limpando `activeContext.md` entre etapas |

**Regras de portabilidade — obrigatórias ao editar esta metodologia:**

1. Nenhum skill, documento ou script cita ferramenta de harness pelo nome. Cite a capacidade (`CAP-SEARCH`, `CAP-PLAN`) e deixe o harness escolher como atendê-la.
2. Todo estado do pipeline vive em arquivos versionados — `payload_index.json`, `context/activeContext.md`, `performance_logs.json` — nunca na memória da sessão. Trocar de harness no meio de um projeto é retomar a leitura desses arquivos.
3. Os skills em `docs/ThronusSpec/02_Setup/` são markdown puro, invocados por caminho. Não dependem de registro de plugin, de sistema de skills nem de sintaxe de slash command.
4. Toda automação é shell POSIX-compatível (`thronus-init.sh`, `apply-starter.sh`) e **idempotente**: reexecutar não corrompe estado.

**Registro do arquivo canônico por harness.** `AGENTS.md` é o padrão aberto (lido nativamente pelo Codex, entre outros). Harnesses com nome próprio recebem um arquivo-ponteiro de uma linha, nunca uma cópia:

| Harness | Arquivo | Conteúdo |
|---|---|---|
| Codex / padrão aberto | `AGENTS.md` | este arquivo (canônico) |
| Claude Code | `CLAUDE.md` | `@AGENTS.md` |
| Gemini CLI | `GEMINI.md` | ponteiro para `AGENTS.md` |
| Cursor | `.cursorrules` | ponteiro para `AGENTS.md` |

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
| **agentes** | Agentes de IA, copilotos, automações conversacionais. 3–12 MS | Pipeline completo, com RED/EDGE adaptados (fluxo conversacional, avaliação de LLM, inputs adversariais) + 3 gates |
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
5. **[ESTADO_PLAN]** → `evaluatePlanIntegritySkill.md` (MAX 3 iter.) + **gate humano obrigatório (CAP-GATE)**
6. **[ESTADO_RED]** → Testes BDD com falha limpa comprovada
7. **[ESTADO_GREEN]** → Implementação produtiva, 100% verde
8. **[ESTADO_EDGE]** → `generateEdgeCaseTestsSkill.md` — Limites, payload corrompido, concorrência
9. **[ESTADO_COMMIT]** → Snapshot-diff gate + `monitorEvolutionMetricsSkill.md` + `gitCommitGuardSkill.md`

Rollbacks: PLAN→SPEC, GREEN→PLAN, EDGE→GREEN, EDGE→PLAN, COMMIT→ABORT.
Rollbacks pré-código: FUNCTIONAL→DISCOVERY, ARCHITECTURE→FUNCTIONAL.

## 4. Retomada e Idempotência

O pipeline é retomável a partir dos arquivos de estado, em qualquer harness, a qualquer momento:

1. Ler `payload_index.json → estado_da_trilha.fase_atual` — é a fase corrente, não a memória da sessão.
2. Ler `context/activeContext.md` — se estiver vazio, não há MS ativa; recomeçar em [ESTADO_SPEC].
3. Carregar `profiles/<perfil>.json` para saber quais fases valem para este projeto.
4. Reexecutar a fase corrente. **Toda fase é idempotente**: reexecutar produz o mesmo artefato, nunca duplica entradas em `payload_index.json` nem em `performance_logs.json`.

Antes de acrescentar qualquer registro a um artefato de estado, verifique se ele já existe pela chave (`ms_id`, `adr_id`). Existindo, atualize em vez de acrescentar.

---

# Projeto: {{PROJECT_NAME}} — {{CLIENT_NAME}}

**Descrição:** (preencher ao inicializar)
**Pacote de código:** `src/{{PACKAGE_NAME}}/` — slug de `{{PROJECT_NAME}}` com hífens trocados por `_`
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
# .github/workflows/governance.yml — checagens TCA, válidas em qualquer stack
# .github/workflows/ci.yml         — testes e lint, trazidos pelo starter
```

### Aplicar o starter tecnológico

Após o ADR aprovado em [ESTADO_ARCHITECTURE]:

```bash
./apply-starter.sh <stack>    # ex.: ./apply-starter.sh python-django
```

O script copia `starters/<stack>/` sobre a raiz, renomeia os diretórios
`{{PACKAGE_NAME}}` e resolve os placeholders. Antes disso a raiz é
deliberadamente agnóstica: sem dependências, sem runner de testes, sem `.env`.

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

### Port/Adapter Pattern

Serviços de aplicação dependem de interfaces/contratos (em `application/ports/`), nunca de implementações concretas de infraestrutura. Isso permite testes unitários sem banco de dados ou rede.

### Invariantes críticos

- **Conventional Commits**: `type(scope): description [MS-NNN]` em todo commit.
- **Port/Adapter**: serviços nunca importam camada de infraestrutura diretamente.
- **EventoAuditoria (se aplicável)**: append-only — nunca modificar ou deletar registros existentes.
- **Raiz agnóstica de stack**: nada específico de linguagem ou framework vive na raiz do template. Se for específico de stack, o lugar é `starters/<stack>/`.
- **Independência de harness**: nenhum artefato cita ferramenta de harness pelo nome — apenas as capacidades do Contrato de Harness (seção 0).

### Testes

Espelhamento estrutural obrigatório: `domain/ → tests/domain/`, `application/ → tests/application/`, `infrastructure/ → tests/infrastructure/`.

- `test_bdd_ms<NNN>_<descricao>` — cenários BDD (CT-01..CT-XX)
- `test_unit_ms<NNN>_<descricao>` — testes unitários puros (sem infraestrutura)
- `test_edge_ms<NNN>_<descricao>` — casos extremos (EDGE-01..STRESS-XX)

Cobertura mínima por perfil: nano=60% · micro=75% · agentes=70% · standard=85% · enterprise=90%.

### Variáveis de ambiente

(Preenchido após decisão de arquitetura — adaptar ao stack escolhido.)
