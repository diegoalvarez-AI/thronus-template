# Thronus Context Architecture (TCA)

> **Conteúdo canônico da metodologia.** Vale para qualquer agente de código
> (Codex, Claude Code, Cursor, Gemini CLI, Aider, ou execução humana) e para
> qualquer projeto. Sem placeholders, sem conteúdo de projeto: o que muda por
> projeto vive em `PROJETO.md`.
>
> Integridade verificada por `tca canon`. Alterar este arquivo sem atualizar
> `tca/CANON.sha256` reprova no `tca doctor` de todo projeto derivado.

Execute `./thronus-init.sh` para inicializar um novo projeto com perfil de complexidade específico.
Após o ADR, execute `./apply-starter.sh <stack>` para aplicar o scaffold tecnológico.

---

## 0. Contrato de Harness

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
4. Toda automação é shell POSIX-compatível ou Python 3 da biblioteca padrão, e **idempotente**: reexecutar não corrompe estado.

**Registro do arquivo canônico por harness.** `AGENTS.md` é o padrão aberto, e é gerado
por `tca agents` a partir deste arquivo mais o `PROJETO.md`. Harnesses com nome próprio
recebem um arquivo-ponteiro de uma linha, nunca uma cópia:

| Harness | Arquivo | Conteúdo |
|---|---|---|
| Codex / padrão aberto | `AGENTS.md` | gerado — metodologia + projeto |
| Claude Code | `CLAUDE.md` | `@AGENTS.md` |
| Gemini CLI | `GEMINI.md` | ponteiro para `AGENTS.md` |
| Cursor | `.cursorrules` | ponteiro para `AGENTS.md` |

---

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

## 5. Fechamento de ciclo

O fechamento de uma Micro Spec é executado pelo comando, não redigido pelo agente:

```bash
tca close-ms <MS-ID> --testes <N>
```

O comando cria o registro de archive, atualiza o índice e o log de performance, e limpa o
`activeContext.md` numa operação idempotente. O portão `commit-msg` reprova commit que
declare `[MS-NNN]` sem trazer essa atualização — o fechamento deixa de depender de
disciplina.

Antes de abrir trabalho novo, `tca verify` confere a coerência dos artefatos de controle e
`tca doctor` reporta divergência entre a metodologia deste projeto e o canon declarado.

## 6. Port/Adapter Pattern

Serviços de aplicação dependem de interfaces/contratos (em `application/ports/`), nunca de implementações concretas de infraestrutura. Isso permite testes unitários sem banco de dados ou rede.

## 7. Invariantes críticos

- **Conventional Commits**: `type(scope): description [MS-NNN]` em todo commit.
- **Port/Adapter**: serviços nunca importam camada de infraestrutura diretamente.
- **EventoAuditoria (se aplicável)**: append-only — nunca modificar ou deletar registros existentes.
- **Raiz agnóstica de stack**: nada específico de linguagem ou framework vive na raiz do template. Se for específico de stack, o lugar é `starters/<stack>/`.
- **Independência de harness**: nenhum artefato cita ferramenta de harness pelo nome — apenas as capacidades do Contrato de Harness (seção 0).
- **Conteúdo gerado não se edita**: arquivo com marcador de geração é reescrito na próxima execução do comando que o produz.

## 8. Convenção de testes

Espelhamento estrutural obrigatório: `domain/ → tests/domain/`, `application/ → tests/application/`, `infrastructure/ → tests/infrastructure/`.

- `test_bdd_ms<NNN>_<descricao>` — cenários BDD (CT-01..CT-XX)
- `test_unit_ms<NNN>_<descricao>` — testes unitários puros (sem infraestrutura)
- `test_edge_ms<NNN>_<descricao>` — casos extremos (EDGE-01..STRESS-XX)

Cobertura mínima por perfil: nano=60% · micro=75% · agentes=70% · standard=85% · enterprise=90%.

## 9. Aplicar o starter tecnológico

Após o ADR aprovado em [ESTADO_ARCHITECTURE]:

```bash
./apply-starter.sh <stack>    # ex.: ./apply-starter.sh python-django
```

O script copia `starters/<stack>/` sobre a raiz, renomeia os diretórios do pacote e
resolve os placeholders. Antes disso a raiz é deliberadamente agnóstica: sem dependências,
sem runner de testes, sem `.env`.
