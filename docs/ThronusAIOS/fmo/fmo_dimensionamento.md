# FMO — Dimensionamento de Escopo e Custo para Discovery

**Uso:** Após o Tier 1 ou Tier 2, traduzir scores em estimativa de escopo e custo do Discovery.  
**Quem usa:** Consultor Thronus na elaboração da proposta de Discovery.

---

## 1. Mapeamento Score → Perfil TCA

| Score médio FMO | Perfil TCA     | Micro Specs estimadas | Prazo Discovery | Complexidade esperada |
|-----------------|----------------|-----------------------|-----------------|----------------------|
| 1.0–1.5         | `micro`        | 5–8                   | 2–3 semanas     | Pré-condições: organização de dados e processos antes de automação |
| 1.5–2.5         | `agentes`      | 6–12                  | 2–4 semanas     | Automação de processos + agentes de canal |
| 2.5–3.5         | `standard`     | 8–18                  | 3–5 semanas     | Produto digital ou operações inteligentes |
| 3.5–5.0         | `enterprise`   | 12–30+                | 4–8 semanas     | Sistemas complexos, múltiplas integrações, growth |

---

## 2. Fatores de Ajuste do Escopo

### Aumentam o escopo (+MSs)
- **Dados fragmentados (Dados ≤ L2):** adicionar 2–4 MSs de organização e migração de dados
- **Integração de sistemas legados:** cada integração = +1–2 MSs de mapeamento e adaptação
- **Dependência de pessoas-chave (Processos ≤ L2):** adicionar MS de documentação de processos críticos
- **Qualificação baixa (Qualificação ≤ L2):** adicionar MS de treinamento e onboarding da equipe
- **Múltiplos canais de atendimento:** cada canal adicional = +1–2 MSs de integração

### Reduzem o escopo (−MSs)
- **Sistema central já existente:** -1–2 MSs (integração mais simples que construção do zero)
- **Time com champions tecnológicos (Qualificação ≥ L3):** -1 MS de treinamento
- **Processo comercial documentado (Processos ≥ L3):** -1 MS de mapeamento

---

## 3. Mapeamento de Dimensões → MSs Típicas

### Processos ≤ L2 → MSs prováveis
- `MS-001` Mapeamento e documentação de processos críticos
- `MS-002` Definição de responsáveis e RACI básico

### Dados ≤ L2 → MSs prováveis
- `MS-003` Auditoria e centralização de dados de clientes (CRM)
- `MS-004` Migração de dados de fontes fragmentadas
- `MS-005` Dashboard básico de indicadores

### Governança ≤ L2 → MSs prováveis
- `MS-006` Definição de política de acesso a dados
- `MS-007` Template de contrato e checklist LGPD básico

### Qualificação ≤ L2 → MSs prováveis
- `MS-008` Treinamento e onboarding para ferramentas novas
- `MS-009` Criação de material de referência (guias internos)

### Receptividade ≤ L2 → atenção de processo, não MS
- Adicionar gate de validação humana obrigatório em todo PLAN
- Adicionar milestone de comunicação interna antes de deploy
- Reduzir tamanho de cada MS (menos mudança por entrega = menos resistência)

---

## 4. Regra de Sequenciamento

A ordem de entrega das MSs deve respeitar a pirâmide de dependências:

```
L5 → Escala e Growth          (só quando os outros estão estáveis)
L4 → Automação e IA           (só quando dados e processos estão mínimos)
L3 → Estrutura e Controle     (organização de dados + processos)
L2 → Fundação                 (CRM básico + papéis definidos + processos documentados)
L1 → Pré-condição             (diagnóstico completo + quick wins imediatos)
```

**Regra prática:** nunca propor MS de automação antes de MS de organização de dados quando Dados ≤ L2. Automatizar caos gera caos automatizado.

---

## 5. Estimativa de Custo Discovery

O Discovery tem custo fixo baseado no perfil TCA, não no número de MSs (que serão definidos *dentro* do Discovery):

| Perfil TCA   | Escopo do Discovery                                              | Prazo  |
|--------------|------------------------------------------------------------------|--------|
| `micro`      | Mapeamento de processos + definição de 5–8 MSs priorizados      | 2 sem  |
| `agentes`    | Fluxos conversacionais + intenções + ADR de canais + 6–12 MSs   | 3 sem  |
| `standard`   | Functional modeling completo + ADR + backlog priorizado 8–18 MSs| 4 sem  |
| `enterprise` | Discovery completo com stakeholders múltiplos + 12–30+ MSs      | 6–8 sem|

*Valores específicos: a precificar por Diego e Bernardo por cliente — usar este documento para dimensionar o esforço, não para comunicar preço diretamente.*

---

## 6. Constraints TCA Derivadas do FMO

O campo `constraints_tca` no `fmo_assessment.json` é lido pelo `fmoToDiscoveryBridgeSkill` e gera automaticamente:

| Constraint              | Consequência no TCA                                           |
|-------------------------|---------------------------------------------------------------|
| `qualificacao_le_2: true` | UI obrigatoriamente simples; MS de treinamento no backlog   |
| `dados_le_2: true`       | MS de migração como alta prioridade; risco de dados no PLAN  |
| `receptividade_le_2: true` | Gate de validação humana em cada PLAN; MSs menores         |
| `processos_le_2: true`   | MS de documentação de processos antes de automação           |
