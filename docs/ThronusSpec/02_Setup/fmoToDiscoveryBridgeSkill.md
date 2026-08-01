# Skill: fmoToDiscoveryBridgeSkill (Metodologia TCA v2 — Integração Thronus AI OS)

## 1. Objetivo Operacional
Transformar o output do **FMO AI-First** (Framework de Maturidade Operacional da Thronus) em um `discovery.md` pré-populado para o ciclo TCA, eliminando a quebra de contexto entre a fase de diagnóstico e a fase de entrega. Garante que tudo que o cliente revelou no diagnóstico seja reaproveitado — e não redescoberto — no início do projeto.

**Ativação:** Invocado quando existe um `fmo_assessment.json` gerado pelo Diagnóstico AI-First, no lugar ou antes de `[ESTADO_DISCOVERY]`. Se não houver FMO prévio, o agente segue o fluxo normal de `discoverySkill.md`.

---

## 2. Protocolo de Bridge

### Passo 2.1: Leitura do FMO Assessment
Ler `docs/ThronusSpec/01_Planejamento/fmo_assessment.json` (gerado pelo Diagnóstico AI-First).

Estrutura esperada do FMO:
```json
{
  "cliente": "...",
  "data_diagnostico": "...",
  "dimensoes": {
    "processos":     { "nivel": 1, "obs": "..." },
    "dados":         { "nivel": 2, "obs": "..." },
    "governanca":    { "nivel": 3, "obs": "..." },
    "qualificacao":  { "nivel": 2, "obs": "..." },
    "receptividade": { "nivel": 4, "obs": "..." }
  },
  "gargalos_prioritarios": ["...", "..."],
  "etapa_recomendada": "produto_digital",
  "observacoes_consultor": "..."
}
```

### Passo 2.2: Mapeamento FMO → Artefatos TCA

| Dimensão FMO | Nível | Impacto em TCA |
|---|---|---|
| **Processos** | 1–2 | Backlog prioritário: MSs de automação de processo existente |
| **Dados** | 1–2 | MS crítica de migração/organização de dados no backlog; risco alto em PLAN |
| **Dados** | 3–5 | Dados organizados → foco em análise e BI |
| **Governança** | 1–2 | Adicionar MSs de auditoria, permissões e rastreabilidade ao backlog |
| **Qualificação** | 1–2 | Restrição no ADR: UI deve ser simples, sem jargão técnico; incluir MS de onboarding |
| **Qualificação** | 4–5 | ADR pode considerar integração mais complexa e dashboards avançados |
| **Receptividade** | 1–2 | Adicionar MS de change management / adoção ao backlog; validar com stakeholder antes do GATE |
| **Receptividade** | 4–5 | Alta disposição → pipeline pode avançar mais rápido |

### Passo 2.3: Geração do `discovery.md` Pré-populado

Usar o mapeamento acima para preencher automaticamente:

```markdown
## Enunciado Canônico (derivado dos gargalos prioritários do FMO)
[construído a partir de fmo.gargalos_prioritarios + dimensao processos]

## Contexto de Maturidade (FMO AI-First — [data_diagnostico])
| Dimensão        | Nível FMO | Observação                  |
|-----------------|-----------|-----------------------------|
| Processos       | [N]/5     | [obs]                       |
| Dados           | [N]/5     | [obs]                       |
| Governança      | [N]/5     | [obs]                       |
| Qualificação    | [N]/5     | [obs]                       |
| Receptividade   | [N]/5     | [obs]                       |

## Mapa de Stakeholders
[derivado das informações coletadas no diagnóstico]

## Restrições Identificadas no FMO
- [qualificacao <= 2]: UI obrigatoriamente simples; incluir MS de treinamento de usuários
- [dados <= 2]: migration de dados como MS de alta prioridade; risco de qualidade de dados
- [receptividade <= 2]: validação humana obrigatória em todos os gates

## Métricas de Sucesso
[derivadas do contraste entre nível atual e nível-alvo por dimensão]

## Riscos (do FMO para o TCA)
[mapeados automaticamente a partir das dimensões com gap]
```

### Passo 2.4: Gerar Restrições para o ADR
Produzir um bloco `fmo_constraints_for_adr.md` em `01_Planejamento/`:
```markdown
## Restrições do FMO para Decisão de Arquitetura
- Qualificação [N]/5: [implicação na complexidade da UX/UI]
- Dados [N]/5: [implicação na necessidade de ETL, migration, qualidade]
- Governança [N]/5: [implicação em auditoria, RBAC, logs]
- Receptividade [N]/5: [implicação na velocidade de rollout, gates de validação]
```

---

## 3. Saída Esperada no Terminal

```
[TCA_FMO_BRIDGE_OK] CONTEXTO DO DIAGNÓSTICO INTEGRADO
  FMO Assessment   : [data_diagnostico]
  Dimensões lidas  : processos · dados · governança · qualificação · receptividade
  Restrições ADR   : [N] restrições derivadas
  MSs adicionais   : [lista de MSs sugeridas pelo mapeamento FMO]
  Arquivos gerados :
    - docs/ThronusSpec/01_Planejamento/discovery.md (pré-populado)
    - docs/ThronusSpec/01_Planejamento/fmo_constraints_for_adr.md
  Próximo estado   : [FUNCTIONAL] ou [ARCHITECTURE] conforme perfil
```
