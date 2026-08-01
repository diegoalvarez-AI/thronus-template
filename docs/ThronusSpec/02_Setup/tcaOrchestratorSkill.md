# Skill: tcaOrchestratorSkill (Metodologia TCA v2 — Pipeline Completo)

## 1. Objetivo Operacional
Orquestrar o pipeline completo de desenvolvimento TCA desde a ideia inicial até o commit — cobrindo descoberta de negócio, modelagem funcional, decisão de arquitetura e ciclo TDD. O pipeline se adapta ao perfil de complexidade do projeto (profiles/nano.json, micro.json, standard.json, enterprise.json).

---

## 2. Mapa Completo de Transições de Estado

```
PRÉ-CÓDIGO (independente de tecnologia)
──────────────────────────────────────
[DISCOVERY]    → [FUNCTIONAL]         progressão normal (Standard/Enterprise)
[DISCOVERY]    → [ARCHITECTURE]       progressão Nano/Micro (pula FUNCTIONAL)
[FUNCTIONAL]   → [ARCHITECTURE]       progressão normal
[FUNCTIONAL]   → [DISCOVERY]          ROLLBACK: modelagem revela problema mal definido
[ARCHITECTURE] → [FUNCTIONAL]         ROLLBACK: decisão revela gap no modelo funcional
[ARCHITECTURE] → [SPEC]               progressão (tecnologia decidida, starter aplicado)

MANUTENÇÃO EVOLUTIVA (entrada de novas demandas)
────────────────────────────────────────────────
[TRIAGE]   → [SPEC]        demanda classificada e inserida no backlog → iniciar próximo ciclo

CICLO TDD (tecnologia-dependente a partir daqui)
────────────────────────────────────────────────
[SPEC]    → [PLAN]     progressão normal
[PLAN]    → [RED]      gate humano obrigatório (único ponto de interação mandatória)
[RED]     → [GREEN]    progressão automática após falha limpa confirmada
[GREEN]   → [EDGE]     progressão automática após 100% verde
[EDGE]    → [COMMIT]   progressão automática após EDGE verde
[COMMIT]  → [DEPLOY]   progressão automática se cd_ativo = true
[DEPLOY]  → [MONITOR]  progressão automática após health check OK
[DEPLOY]  → [ABORT]    health check falhou — aguardar intervenção humana

ROLLBACKS
─────────
[PLAN]     → [SPEC]         MAX_ITERATIONS atingido: escalar com humano
[PLAN]     → [FUNCTIONAL]   plano revela lacuna de modelagem funcional
[GREEN]    → [PLAN]         implementação revela impossibilidade arquitetural
[EDGE]     → [GREEN]        bug de lógica corrigível (ajuste fino)
[EDGE]     → [PLAN]         falha arquitetural revelada em edge
[COMMIT]   → [ABORT]        diff-check detecta arquivos não previstos na spec
[MONITOR]  → [TRIAGE]       anomalia detectada → cria MS de bug_fix automaticamente
```

---

## 3. Algoritmo de Execução

### 3.0 — Verificação de Perfil
Ler `payload_index.json` campo `estado_da_trilha.perfil` para identificar o perfil ativo.
Carregar `profiles/<perfil>.json` para determinar quais fases são obrigatórias, recomendadas ou ignoradas.
Se `perfil` não estiver definido: solicitar ao humano antes de prosseguir.

### 3.1 — [ESTADO_DISCOVERY] Descoberta de Negócio
* Verificar se `docs/ThronusSpec/01_Planejamento/discovery.md` existe e está completo.
* Se não: invocar `docs/ThronusSpec/02_Setup/discoverySkill.md`.
* Perfil Nano: usar forma simplificada (apenas problema e critério de sucesso).
* Aguardar `STATUS_DISCOVERY_CONCLUIDO`.
* Transitar para [FUNCTIONAL] (Standard/Enterprise) ou [ARCHITECTURE] (Nano/Micro).

### 3.2 — [ESTADO_FUNCTIONAL] Modelagem Funcional
* Verificar se fase é ativa no perfil (ignorada = Nano; recomendada = Micro; obrigatória = Standard/Enterprise).
* Se ignorada: transitar diretamente para [ARCHITECTURE].
* Invocar `docs/ThronusSpec/02_Setup/functionalModelingSkill.md`.
* Output: `functional_model.md` + backlog de Micro Specs em `payload_index.json`.
* Se modelagem revelar que o problema estava mal definido: **→ ROLLBACK [DISCOVERY]**.
* Gates Standard/Enterprise: aguardar `GATE_FUNCTIONAL_APROVADO` antes de avançar.
* Aguardar `STATUS_FUNCTIONAL_CONCLUIDO`.

### 3.3 — [ESTADO_ARCHITECTURE] Decisão de Arquitetura
* Invocar `docs/ThronusSpec/02_Setup/architectureDecisionSkill.md`.
* Output: `architecture_decision.md` + `payload_index.json` atualizado com stack.
* Se decisão revelar gap no modelo funcional: **→ ROLLBACK [FUNCTIONAL]**.
* Perfil Standard/Enterprise: **gate humano obrigatório** — aguardar aprovação do ADR.
* Após aprovação: aplicar starter tecnológico (`starters/<stack>/`) se existir, ou criar scaffold manualmente.
* Aguardar `STATUS_ARCHITECTURE_CONCLUIDO`. Transitar para [SPEC].

### 3.3-A — [ESTADO_TRIAGE] Triagem de Demanda (entrada de manutenção)
* Ativado quando chega uma demanda nova durante o ciclo de manutenção evolutiva.
* Invocar `docs/ThronusSpec/02_Setup/backlogTriageSkill.md` com o texto da demanda.
* O skill classifica tipo, tamanho, prioridade e dependências automaticamente.
* Se tamanho GG detectado: propor decomposição antes de inserir.
* Após inserção no backlog: aguardar `STATUS_TRIAGE_COMPLETO` e transitar para [SPEC] com a MS recém-criada.

### 3.4 — [ESTADO_SPEC] Especificação de Micro Spec
* Executar `docs/ThronusSpec/02_Setup/loadProjectPayloadSkill.md` (carrega payload_index.json + contexto relevante via Scout subagent).
* Selecionar a próxima MS pendente do backlog em `payload_index.json`.
* Gerar spec completa em `context/activeContext.md` (cenários CT-XX, arquivos a criar/modificar, contratos).
* Aguardar `STATUS_DOCUMENTACAO_LIBERADA`. Transitar para [PLAN].

### 3.5 — [ESTADO_PLAN] Planejamento Técnico
* Ler `context/activeContext.md`, entrar em EnterPlanMode, estruturar estratégia técnica completa.
* Invocar `docs/ThronusSpec/02_Setup/evaluatePlanIntegritySkill.md` (MAX_ITERATIONS=3).
  * Se MAX_ITERATIONS atingido sem aprovação: emitir `STATUS_PLANO_REQUER_REVISAO_HUMANA` → **ROLLBACK [SPEC]** ou **ROLLBACK [FUNCTIONAL]** se lacuna de modelagem identificada.
  * Se APROVADO: emitir sumário `[TCA_INTEGRITY_CHECK]` e **aguardar confirmação humana (uma linha de OK)**. Este é o único ponto de interação mandatória no ciclo TDD.
* Após confirmação: transitar para [RED].

### 3.6 — [ESTADO_RED] TDD Red
* Escrever arquivos de teste cobrindo todos os cenários CT-XX do `activeContext.md`.
* Executar suíte de testes e verificar falha limpa (ImportError ou ausência de estrutura — não AssertionError acidental).
* Transitar automaticamente para [GREEN].

### 3.7 — [ESTADO_GREEN] Implementação Produtiva
* Criar ou refatorar arquivos produtivos conforme plano validado.
* Executar suíte em loop até 100% verde.
* Se impossibilidade arquitetural descoberta: emitir diagnóstico e **→ ROLLBACK [PLAN]**.
* Transitar automaticamente para [EDGE].

### 3.8 — [ESTADO_EDGE] Testes de Estresse
* Invocar `docs/ThronusSpec/02_Setup/generateEdgeCaseTestsSkill.md`.
* Bug de lógica corrigível: corrigir e **→ retornar ao final de [GREEN]**.
* Falha arquitetural (mudança de schema, invariante violada): **→ ROLLBACK [PLAN]**.
* Transitar automaticamente para [COMMIT].

### 3.9 — [ESTADO_COMMIT] Fechamento
* **Snapshot-diff gate**: `git diff --name-only HEAD` vs lista de arquivos em `activeContext.md`. Arquivos inesperados: listar, aguardar instrução, **→ [ABORT] se confirmado erro**.
* Invocar `docs/ThronusSpec/02_Setup/monitorEvolutionMetricsSkill.md`:
  * Atualizar `payload_index.json` (estado_da_trilha + _archive.keys).
  * Criar `payload_archive/<ms_NNN>.json` com contratos da MS entregue.
  * Registrar métricas em `05_Monitoramento/performance_logs.json`.
  * Limpar `context/activeContext.md`.
* Invocar `docs/ThronusSpec/02_Setup/gitCommitGuardSkill.md`:
  * Gerar mensagem Conventional Commits com MS-ID.
  * Executar `git add <arquivos_previstos>` (lista explícita — nunca `git add .`).
  * Executar `git commit -m "[MENSAGEM_GERADA]"`.
* Verificar `payload_index.json → estado_da_trilha.cd_ativo`:
  * Se `true`: transitar automaticamente para [DEPLOY].
  * Se `false` ou ausente: encerrar em COMMIT. Deploy permanece manual.

### 3.10 — [ESTADO_DEPLOY] Deploy Contínuo
* Invocar `docs/ThronusSpec/02_Setup/deploySkill.md`.
* O skill detecta o padrão de infra (`payload_index.json → arquitetura_e_padroes.infra`) e executa o procedimento adequado.
* Health check pós-deploy: HTTP 200 em `/health/` (ou endpoint configurado).
* Se health check OK: transitar automaticamente para [MONITOR].
* Se health check falhou: emitir `STATUS_DEPLOY_FALHOU` → **[ABORT_DEPLOY]** (commit não é revertido — problema é de ambiente).

### 3.11 — [ESTADO_MONITOR] Monitoramento Pós-Deploy
* Invocar `docs/ThronusSpec/02_Setup/productionMonitorSkill.md`.
* O skill verifica infra, integridade de dados de negócio e logs de erro.
* Se tudo saudável: pipeline concluído com sucesso.
* Se anomalia detectada: invocar `backlogTriageSkill.md` automaticamente → nova MS inserida no backlog com prioridade adequada.

---

## 4. Resposta Final do Terminal

```
════════════════════════════════════════════════════════════
[TCA_PIPELINE_SUCCESS] ENTREGA EFETUADA COM SUCESSO
  Fase concluída     : [PRE-CODE:ARCHITECTURE | TDD:MS-NNN]
  Micro Spec         : [ID e Nome, se aplicável]
  Iterações PLAN     : [N ciclos de auditoria]
  Rollbacks          : [nenhum | lista]
  Arquivos commitados: [lista explícita]
  Commit             : [mensagem]
  Deploy             : [ok | não configurado | falhou]
  Monitor            : [saudável | anomalias detectadas → MS-NNN criada]
  RAM                : LIMPA E VAZIA ✓
════════════════════════════════════════════════════════════
```
