# Skill: monitorEvolutionMetricsSkill (Metodologia TCA v2)

## 1. Objetivo Operacional
Executar o fechamento de ciclo após 100% da suíte verde no estado GREEN/EDGE. Atualiza o payload de contexto, registra métricas de evolução e limpa a RAM da sessão para o próximo ciclo.

---

## 2. Protocolo de Consolidação (Passo a Passo)

### Passo 2.1: Verificação Final da Suíte
* Confirmar que 100% dos testes do ciclo atual passaram — incluindo os EDGE cases.
* Confirmar ausência de regressão no código legado (nenhum teste previamente verde voltou a falhar).
* Registrar contagem total de testes e cobertura em `docs/ThronusSpec/05_Monitoramento/performance_logs.json`.

### Passo 2.2: Auditoria de Impacto de Infraestrutura
* Inspecionar migrações, schemas ou mudanças de estrutura de dados gerados no ciclo.
* Documentar em `05_Monitoramento/`: novos índices, constraints, relacionamentos e projeção de crescimento de volume com base nos requisitos da MS.
* Se o projeto não usa banco de dados relacional, adaptar o registro ao tipo de persistência em uso (ex: collections NoSQL, S3 buckets, event store).

### Passo 2.3: Atualização do Payload de Contexto
* Ler `docs/ThronusSpec/03_Desenvolvimento/payload_index.json` e aplicar incremento síncrono:
  * Atualizar `estado_da_trilha.ultima_micro_spec_concluida` com o ID/nome da MS encerrada.
  * Atualizar `estado_da_trilha.status_modulo_percentual` com o novo percentual de progresso.
  * Atualizar `estado_da_trilha.micro_spec_ativa` para `null`.
  * Adicionar a chave da MS ao array `_archive.keys`.
* Criar `docs/ThronusSpec/03_Desenvolvimento/payload_archive/<ms_NNN>.json` com os contratos estáveis da MS entregue (serviços, interfaces, modelos, regras de negócio que outras MSs poderão reutilizar).

### Passo 2.4: Liberação da RAM de Sessão
* Abrir `context/activeContext.md` e substituir o conteúdo pelo marcador de sessão limpa:
  ```
  # Active Context — TCA Session RAM
  **Fase atual:** SPEC
  **MS ativa:** —
  **Arquivos a criar/modificar:** —
  **Cenários BDD:** —
  ```
* Este marcador previne que contextos desatualizados contaminem a próxima sessão cold start.

---

## 3. Saída Esperada no Terminal

```
[TCA_CYCLE_CLOSED] SUCESSO NA CONSOLIDAÇÃO
  Spec concluída    : [ID e Nome da MS]
  Testes            : [N passed, M skipped]
  Payload atualizado: [campos alterados em payload_index.json]
  Archive criado    : payload_archive/<ms_NNN>.json
  Impacto infra     : [índices/constraints/schemas adicionados, ou "nenhum"]
  Status            : CICLO_CONCLUIDO_RAM_LIMPA ✓
```
