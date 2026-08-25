<!--
  GERADO por `tca agents --write` — não edite este arquivo.

  Metodologia : tca/METODOLOGIA.md   (canônica, verificada por tca canon)
  Projeto     : PROJETO.md           (editável, específico deste projeto)

  Editar aqui é perda garantida na próxima geração.
-->

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

### Snapshot-diff bidirecional

O `activeContext.md` declara os arquivos que a Micro Spec vai criar ou modificar:

```
**Arquivos a criar/modificar:** src/dominio/turma.py, tests/domain/test_turma.py
```

ou, em lista:

```
**Arquivos a criar/modificar:**
- src/dominio/turma.py
- tests/domain/test_turma.py
```

Travessão (`—`) significa nenhum arquivo. **Campo ausente é lacuna, não permissão.**

`tca diff` compara essa lista com o que foi de fato tocado e reprova nos dois sentidos:
arquivo fora da spec e **arquivo previsto que não foi entregue**. O segundo é a assinatura
da entrega parcial, e é o que um gate unidirecional deixa passar em silêncio.

### Auto-verificação do pipeline

`tca selfcheck` pergunta se a própria verificação está de pé: o contrato de execução
existe, a contagem de testes não caiu em relação à última medição desta máquina, e a
última execução da suíte não terminou em erro.

Existe porque uma suíte que não executa é indistinguível de uma suíte que passa, para
quem só lê o resultado agregado.

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

---

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
