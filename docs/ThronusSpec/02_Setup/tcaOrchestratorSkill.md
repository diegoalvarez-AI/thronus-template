# Skill: tcaOrchestratorSkill (Metodologia TCA v2)

## 1. Objetivo Operacional
Orquestrar o pipeline de desenvolvimento TCA com transições de estado explícitas, rollback definido e enforcement de qualidade em cada fase. O pipeline é autônomo na execução, mas requer um gate humano após o planejamento antes de escrever código.

---

## 2. Mapa de Transições de Estado

```
[SPEC]  → [PLAN]    progressão normal
[PLAN]  → [RED]     gate humano obrigatório (ver §3.2)
[RED]   → [GREEN]   progressão automática após falha limpa confirmada
[GREEN] → [EDGE]    progressão automática após 100% verde
[EDGE]  → [COMMIT]  progressão automática após EDGE verde

ROLLBACKS:
[PLAN]   → [SPEC]    se MAX_ITERATIONS atingido: escalar com humano antes de continuar
[GREEN]  → [PLAN]    se implementação revelar impossibilidade arquitetural
[EDGE]   → [GREEN]   se edge case revelar bug de lógica (ajuste fino)
[EDGE]   → [PLAN]    se edge case revelar falha arquitetural (revisão maior)
[COMMIT] → [ABORT]   se diff-check detectar arquivos não previstos na spec
```

---

## 3. Algoritmo de Execução

### 3.1 — [ESTADO_SPEC] Inicialização
* Executar `docs/ThronusSpec/02_Setup/loadProjectPayloadSkill.md`.
* Aguardar `STATUS_DOCUMENTACAO_LIBERADA`.
* Transitar automaticamente para `[ESTADO_PLAN]`.

### 3.2 — [ESTADO_PLAN] Arquitetura e Auditoria
* Ler `context/activeContext.md`, entrar em EnterPlanMode e estruturar a estratégia técnica completa.
* Invocar `docs/ThronusSpec/02_Setup/evaluatePlanIntegritySkill.md`.
  * Se REJEITADO: reescrever em loop síncrono (MAX_ITERATIONS=3 dentro do evaluatePlanIntegritySkill).
  * Se MAX_ITERATIONS atingido sem aprovação: emitir `STATUS_PLANO_REQUER_REVISAO_HUMANA` e aguardar instrução. **→ ROLLBACK [SPEC]**
  * Se APROVADO: emitir o sumário `[TCA_INTEGRITY_CHECK]` e **aguardar confirmação humana** (uma linha de OK) antes de avançar. Este é o único ponto de interação humana obrigatória no pipeline.
* Após confirmação: transitar para `[ESTADO_RED]`.

### 3.3 — [ESTADO_RED] TDD Red
* Escrever os arquivos de teste cobrindo todos os cenários CT-XX do `activeContext.md`.
* Executar `pytest` e verificar que os testes falham por **ImportError ou AttributeError** (não por AssertionError), confirmando que não há código produtivo que satisfaça os testes por acidente.
* Transitar automaticamente para `[ESTADO_GREEN]`.

### 3.4 — [ESTADO_GREEN] Implementação Produtiva
* Criar ou refatorar os arquivos produtivos conforme o plano validado.
* Implementar em conformidade com a lista de arquivos a criar/modificar em `activeContext.md`.
* Executar `pytest` em loop até 100% verde.
* Se a implementação revelar impossibilidade arquitetural não prevista no plano: emitir diagnóstico e **→ ROLLBACK [PLAN]**.
* Transitar automaticamente para `[ESTADO_EDGE]`.

### 3.5 — [ESTADO_EDGE] Testes de Estresse
* Invocar `docs/ThronusSpec/02_Setup/generateEdgeCaseTestsSkill.md`.
* Se edge case revelar bug de lógica corrigível sem mudança de modelo: corrigir e **→ retornar ao final de [GREEN]**.
* Se edge case revelar falha arquitetural (mudança de schema, invariante violada): emitir diagnóstico e **→ ROLLBACK [PLAN]**.
* Transitar automaticamente para `[ESTADO_COMMIT]`.

### 3.6 — [ESTADO_COMMIT] Fechamento e Commit
* **Snapshot-diff gate:** executar `git diff --name-only HEAD` e comparar contra a lista "Arquivos a criar/modificar" em `activeContext.md`. Se houver arquivos não previstos: emitir aviso, listar os arquivos inesperados e aguardar instrução antes de commitar. **→ [ABORT] se confirmado como erro**.
* Invocar `docs/ThronusSpec/02_Setup/monitorEvolutionMetricsSkill.md`:
  * Atualizar `payload_index.json` (campo `estado_da_trilha` e novo contrato no index `_archive.keys`).
  * Criar `payload_archive/<ms_NNN>.json` com os contratos da MS entregue.
  * Registrar métricas em `05_Monitoramento/performance_logs.json` (obrigatório).
  * Limpar `context/activeContext.md` (marcador de sessão limpa).
* Invocar `docs/ThronusSpec/02_Setup/gitCommitGuardSkill.md`.
  * Gerar mensagem Conventional Commits com MS-ID.
  * Executar `git add <arquivos_previstos_na_spec>` (lista explícita, não `git add .`).
  * Executar `git commit -m "[MENSAGEM_GERADA]"`.

---

## 4. Resposta Final do Terminal

```
════════════════════════════════════════════════════════════
[TCA_PIPELINE_SUCCESS] ENTREGA EFETUADA COM SUCESSO
  - Micro Spec Concluída : [ID e Nome]
  - Iterações PLAN       : [N ciclos de auditoria]
  - Rollbacks executados : [nenhum | lista de rollbacks]
  - Arquivos commitados  : [lista explícita]
  - Commit Consolidado   : [Mensagem do Git Commit]
  - Estado da RAM        : LIMPA E VAZIA ✓
  - Status               : PIPELINE_ENCERRADO.
════════════════════════════════════════════════════════════
```
