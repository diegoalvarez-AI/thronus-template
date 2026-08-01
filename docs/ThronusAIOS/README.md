# Thronus AI OS — Sistema Operacional Inteligente da Empresa

> **"A estrutura que ancora o invisível."**
> O Thronus AI OS é o sistema de governança e execução que encadeia, do primeiro contato comercial ao acompanhamento pós-entrega, todos os processos da Thronus Digital com inteligência artificial, automação e método.

---

## Visão

A maioria das empresas de tecnologia usa IA para acelerar a entrega de projetos dos clientes.
A Thronus vai além: usa IA para **operar a própria empresa** com o mesmo nível de rigor que aplica nas entregas.

O Thronus AI OS não é um produto comercializado. É o sistema nervoso interno da Thronus — a arquitetura que garante que diagnóstico, entrega, governança e crescimento funcionem como um sistema integrado, auditável e escalável.

---

## Princípios AI-First

1. **Diagnóstico antes de tecnologia** — nenhum processo é automatizado sem ser primeiro entendido
2. **Humanos decidem, agentes executam** — IA amplifica julgamento; não o substitui
3. **Tudo que importa é rastreável** — cada decisão tem artefato; cada entrega tem evidência
4. **Governança não é overhead** — é o que permite crescer sem perder qualidade
5. **Integração em cadeia** — cada etapa alimenta a próxima; zero ilha de dados

---

## Arquitetura em 6 Camadas

```
┌─────────────────────────────────────────────────────────────────────┐
│  CAMADA 0 — ACQUISITION ENGINE (Growth + Marketing)                 │
│  Atração → Qualificação → CRM → Diagnóstico agendado               │
├─────────────────────────────────────────────────────────────────────┤
│  CAMADA 1 — DIAGNOSTIC ENGINE (FMO AI-First)                        │
│  Assessment 5D → Maturidade → Recomendação → Proposta disparada     │
├─────────────────────────────────────────────────────────────────────┤
│  CAMADA 2 — COMMERCIAL ENGINE (Proposta + Jurídico)                 │
│  Escopo → Proposta → Contrato → Onboarding                          │
├─────────────────────────────────────────────────────────────────────┤
│  CAMADA 3 — DELIVERY ENGINE (TCA)                                   │
│  DISCOVERY → FUNCTIONAL → ARCHITECTURE → TDD cycle → DEPLOY        │
├─────────────────────────────────────────────────────────────────────┤
│  CAMADA 4 — FINANCIAL ENGINE (FinOps)                               │
│  Tracking de projeto → Faturamento → Receita → P&L por cliente      │
├─────────────────────────────────────────────────────────────────────┤
│  CAMADA 5 — SUSTENTATION ENGINE                                     │
│  SLA → Monitor → Backlog → Radar tecnológico → Expansão             │
└─────────────────────────────────────────────────────────────────────┘
              ↑                                       ↓
              └───── loop de expansão: FMO reavalia ──┘
```

---

## Camada 0 — Acquisition Engine

**Objetivo:** transformar interesse em oportunidade qualificada com contexto de negócio já coletado.

### Fluxo
```
Conteúdo publicado (artigos, whitepapers, cases)
        ↓
Lead entra por canal (site, WhatsApp, indicação, evento)
        ↓
Agente de qualificação inicial (WhatsApp ou formulário inteligente)
  → coleta: segmento, porte, principal dor, urgência
  → classifica: QUENTE / MORNO / FRIO
        ↓
Registro no CRM com contexto coletado
        ↓
Se QUENTE: agenda diagnóstico automaticamente → notifica Bernardo
Se MORNO: sequência de nurturing (conteúdo segmentado por dor)
Se FRIO: mantém em lista de conteúdo, reavalia em 30 dias
```

### Agentes de IA
| Agente | Função | Plataforma sugerida |
|--------|--------|---------------------|
| QualificadorInicial | Triagem de lead por dor e urgência | WhatsApp Business API + LLM |
| NurturingAgent | Sequência de conteúdo personalizado por segmento | n8n + e-mail |
| CRMUpdater | Sincronização automática de dados do lead | Pipedrive/HubSpot API |

### Pontos de decisão humana
- Bernardo revisa leads QUENTES antes de confirmar o diagnóstico
- Leads de alto valor (acima de R$ X) passam por qualificação manual adicional

### Artefatos produzidos
- `lead_context.json` → alimenta o FMO na Camada 1

---

## Camada 1 — Diagnostic Engine (FMO AI-First)

**Objetivo:** gerar mapa objetivo de maturidade operacional do cliente e definir o caminho de transformação.

### Framework de Maturidade Operacional (FMO)

5 dimensões × 5 níveis → posição e gap por dimensão:

| Dimensão | Nível 1 | Nível 3 | Nível 5 |
|---|---|---|---|
| **Processos** | Tudo manual, caótico | Processos definidos, alguns automatizados | Processos monitorados e otimizados continuamente |
| **Dados** | Planilhas dispersas, sem integração | Dados centralizados, qualidade média | Dados governados, real-time, alimentam decisão |
| **Governança** | Sem responsabilidades definidas | Responsabilidades claras, auditoria básica | Rastreabilidade total, compliance, segurança |
| **Qualificação** | Equipe sem familiaridade com tecnologia | Uso básico de ferramentas digitais | Equipe adota novas tecnologias com autonomia |
| **Receptividade** | Alta resistência à mudança | Abertura moderada com suporte | Alta disposição, cultura de melhoria contínua |

### Fluxo de Diagnóstico
```
Coleta inicial: conversa ou formulário com agente IA
        ↓
Validação humana do contexto operacional (Diego + consultor)
        ↓
Scoring FMO por dimensão
        ↓
Relatório: mapa de maturidade + gargalos + prioridades + etapa recomendada
        ↓
Output: fmo_assessment.json → alimenta Camada 2 (proposta) e Camada 3 (TCA discovery)
```

### Etapa recomendada por scoring médio FMO
| Score médio | Etapa recomendada |
|---|---|
| 1,0 – 1,9 | Etapa 0: organizar antes de automatizar |
| 2,0 – 2,9 | Etapa 1: Automação e Agentes de IA |
| 3,0 – 3,9 | Etapa 2: Operações Inteligentes, ou Etapa 3: Produto Digital |
| 4,0 – 5,0 | Etapa 4: Growth e Mercado; ou expansão/evolução do produto existente |

### Artefatos produzidos
- `fmo_assessment.json` → input obrigatório para `fmoToDiscoveryBridgeSkill`
- `relatorio_diagnostico_[cliente].md` → entregável para o cliente

---

## Camada 2 — Commercial Engine

**Objetivo:** transformar o diagnóstico em proposta formal, contrato e onboarding estruturado.

### Fluxo
```
fmo_assessment.json
        ↓
proposalGeneratorSkill (se projeto similar já foi entregue → reaproveitamento de template)
        ↓
Proposta gerada: escopo, prazo, investimento, garantias de qualidade, SLA
        ↓
Revisão e aprovação: Bernardo (comercial) + Diego (técnico)
        ↓
Contrato: seleção de template jurídico + preenchimento automático
  → NDA (projetos com IP sensível)
  → Contrato de serviço (por tipo de etapa do portfólio)
  → SLA addendum (para projetos com sustentação)
        ↓
E-assinatura → trigger de onboarding
        ↓
Criação do projeto no repositório (thronus-init.sh)
Registro no CRM: oportunidade → cliente ativo
Registro financeiro: contrato → projeto ativo → cronograma de faturamento
```

### Templates jurídicos por tipo de projeto
| Tipo de projeto | Template |
|---|---|
| Agentes de IA (Etapa 1) | Contrato de automação + cláusula de dados e privacidade |
| Produto digital (Etapa 3) | Contrato de desenvolvimento + cláusula de IP e código-fonte |
| Sustentação | Addendum de SLA + definição de tier |
| Diagnóstico apenas | Proposta de consultoria + NDA |

### Cláusulas padrão obrigatórias
- **Propriedade intelectual:** código-fonte entregue ao cliente após quitação integral
- **LGPD:** tratamento de dados pessoais conforme Lei 13.709/2018
- **Confidencialidade:** NDA bilateral em projetos com dados sensíveis do cliente
- **Escopo e variação:** mudanças de escopo documentadas como nova MS, com impacto em prazo e custo

### Artefatos produzidos
- Proposta comercial (PDF)
- Contrato assinado
- Onboarding checklist para o cliente

---

## Camada 3 — Delivery Engine (TCA)

**Objetivo:** entregar o produto com rigor metodológico, rastreabilidade total e evidência de qualidade.

### Referência
Pipeline completo definido em `docs/ThronusSpec/02_Setup/tcaOrchestratorSkill.md`.

### Conexões com outras camadas
| Evento TCA | Dispara em outra camada |
|---|---|
| `fmoToDiscoveryBridgeSkill` | Lê `fmo_assessment.json` da Camada 1 |
| Gate PLAN aprovado | Registra milestone no financeiro (Camada 4) |
| Gate RELEASE_N | Dispara faturamento de milestone (Camada 4) |
| COMMIT bem-sucedido | Atualiza métricas no CRM (Camada 0) |
| `clientProgressSkill` | Envia relatório ao cliente (loop de confiança) |
| Projeto concluído | `proposalGeneratorSkill` atualiza biblioteca de cases (Camada 0) |
| `productionMonitorSkill` detecta anomalia | Cria MS via `backlogTriageSkill` (Camada 5) |

### Perfis disponíveis
| Perfil | Uso típico na Thronus |
|---|---|
| `nano` | Diagnóstico com entregável simples; script; relatório automatizado |
| `micro` | MicroSaaS; MVP com 5–15 funcionalidades |
| `agentes` | Automação e agentes de IA (Etapa 1) |
| `standard` | Produto digital sob medida (Etapa 3) — caso mais comum |
| `enterprise` | Plataformas complexas, govtech, saúde, financeiro |

---

## Camada 4 — Financial Engine (FinOps)

**Objetivo:** rastrear receita, custo e rentabilidade por projeto; garantir previsibilidade financeira; automatizar o faturamento.

### Modelo de faturamento por tipo de projeto
| Modelo | Quando usar | Trigger de faturamento |
|---|---|---|
| Por milestone | Produto digital (Etapa 3) | Gate TCA (DISCOVERY, MVP, RELEASE) |
| Mensalidade fixa | Sustentação | 1º dia do mês |
| Por entrega | Agentes de IA (Etapa 1) | Go-live confirmado |
| Por hora | Diagnóstico / consultoria pontual | Relatório entregue |

### Estrutura de rastreamento por projeto
```
projeto_financeiro_[cliente].json:
{
  "contrato_valor_total": 0,
  "milestones": [
    { "gate": "DISCOVERY_APROVADO", "valor": 0, "status": "pago|pendente", "data": "..." },
    { "gate": "MVP",                "valor": 0, "status": "pago|pendente", "data": "..." },
    { "gate": "ENCERRAMENTO",       "valor": 0, "status": "pago|pendente", "data": "..." }
  ],
  "custo_estimado_horas": 0,
  "horas_realizadas": 0,
  "margem_percentual": 0
}
```

### Agentes de IA na camada financeira
| Agente | Função |
|---|---|
| BillingTrigger | Detecta gate concluído no TCA → gera boleto/NF automaticamente |
| OverdueAlert | Monitora pagamentos vencidos → notifica Bernardo |
| CashFlowProjector | Projeta receita dos próximos 3 meses com base em projetos ativos |
| MarginAnalyzer | Calcula margem real por projeto ao concluir cada MS |

### Métricas financeiras monitoradas
- Receita recorrente (MRR de sustentação) vs. receita de projeto
- Prazo médio de recebimento (DSO)
- Margem por tipo de projeto (nano vs. standard vs. enterprise)
- Custo de aquisição de cliente (CAC) por canal de entrada

---

## Camada 5 — Sustentation Engine

**Objetivo:** manter produtos em produção com qualidade, evoluir a relação com o cliente e detectar oportunidades de expansão.

### Referência
Ciclos definidos em `docs/ThronusSpec/02_Setup/sustentacaoSkill.md`.

### Loop de Expansão
```
Ciclo anual de sustentação
        ↓
FMO re-assessment: onde o cliente está agora vs. quando começamos?
        ↓
Gap identificado → etapa seguinte do portfólio Thronus
  Ex: cliente evoluiu de Nível 2→4 em Processos
      → Etapa 2 (Operações Inteligentes) agora faz sentido
        ↓
proposalGeneratorSkill: proposta automática para a próxima etapa
        ↓
Bernardo apresenta → negociação → Camada 2 (Commercial Engine)
```

---

## Mapa de Dados entre Camadas

```
lead_context.json          (C0→C1)  contexto inicial do lead
fmo_assessment.json        (C1→C2)  maturidade + etapa recomendada
fmo_assessment.json        (C1→C3)  constraints para TCA discovery
proposta_[cliente].json    (C2→C4)  valor e milestones do contrato
payload_index.json         (C3→C4)  gates concluídos → trigger faturamento
payload_index.json         (C3→C5)  estado do produto → base de sustentação
relatorio_cliente_*.md     (C3→C0)  progresso → material de relacionamento
case_study_*.md            (C3→C0)  case → prospecção de novos clientes
fmo_evolucao_*.md          (C5→C2)  expansão → nova proposta comercial
projeto_financeiro_*.json  (C4→C2)  histórico → precificação de novos projetos
```

---

## Pontos de Decisão Humana

O Thronus AI OS é AI-first, não AI-only. Estes são os pontos onde humanos decidem obrigatoriamente:

| Camada | Ponto de decisão | Quem decide |
|---|---|---|
| C0 | Lead QUENTE vai para diagnóstico? | Bernardo |
| C1 | Validação do FMO com o cliente | Diego + cliente |
| C2 | Aprovação da proposta e assinatura | Diego + Bernardo + cliente |
| C3 | Gate PLAN: estratégia técnica aprovada? | Diego (gate único TCA) |
| C3 | Rollback identificado pelo agente | Diego avalia diagnóstico |
| C4 | Margem abaixo do threshold? Renegociar escopo | Diego + Bernardo |
| C5 | FMO re-assessment: nova etapa recomendada | Diego apresenta a Bernardo |

---

## Stack de Ferramentas Recomendada

| Camada | Função | Ferramenta sugerida |
|---|---|---|
| C0 | CRM | Pipedrive ou HubSpot |
| C0 | WhatsApp Business | Meta Cloud API |
| C0 | Automação de marketing | n8n (self-hosted) ou Make |
| C1 | Coleta FMO | Typeform + agente IA ou formulário customizado |
| C2 | Proposta | Notion ou documento PDF gerado por template |
| C2 | E-assinatura | DocuSign ou Clicksign |
| C3 | Repositório + CI/CD | GitHub + GitHub Actions |
| C3 | Monitoramento de erros | Sentry |
| C4 | Financeiro | Conta Azul ou Omie (emissão NF) |
| C4 | Projeção financeira | Planilha estruturada ou Conta Azul |
| C5 | Health check | Endpoint `/health/` + cron job |
| Transversal | Orquestração de agentes | n8n (self-hosted) |
| Transversal | LLM | Claude (Anthropic API) |
| Transversal | Documentação interna | Notion ou Obsidian |

---

## Governança do AI OS

### Quem mantém cada camada
| Camada | Responsável principal | Responsável de suporte |
|---|---|---|
| C0 Acquisition | Bernardo | Diego (conteúdo técnico) |
| C1 Diagnostic | Diego | Bernardo (relação com cliente) |
| C2 Commercial | Bernardo + Diego | — |
| C3 Delivery | Diego | — |
| C4 Financial | Bernardo | Diego (milestones técnicos) |
| C5 Sustentation | Diego | Bernardo (expansão) |

### Auditoria do OS
- **Mensal:** revisão de métricas por camada (leads, FMOs, projetos ativos, MRR, SLA cumprido)
- **Trimestral:** revisão dos templates jurídicos e de proposta
- **Semestral:** revisão do radar tecnológico da Thronus (não apenas dos clientes)
- **Anual:** revisão dos perfis TCA, skills e do próprio AI OS

---

## Roadmap de Implementação

### Fase 1 — Fundação (já executado)
- [x] TCA v2 completo (9 estados, skills, perfis nano/micro/standard/enterprise)
- [x] CI/CD no qualiedu (GitHub Actions)
- [x] `productionMonitorSkill` + `backlogTriageSkill` + `deploySkill`
- [x] `clientProgressSkill`, `fmoToDiscoveryBridgeSkill`, `sustentacaoSkill`
- [x] `proposalGeneratorSkill`, perfil `agentes`

### Fase 2 — Camadas Comerciais (próximo)
- [ ] Template `fmo_assessment.json` + guia de aplicação do FMO
- [ ] Templates de proposta por tipo de projeto (nano, agentes, standard)
- [ ] Templates jurídicos (NDA, contrato de desenvolvimento, SLA addendum)
- [ ] Integração CRM: registro automático de milestone TCA

### Fase 3 — Operações Inteligentes Internas
- [ ] BillingTrigger: gate TCA → geração de cobrança automática
- [ ] CashFlowProjector: projeção de receita com base em pipeline ativo
- [ ] QualificadorInicial: agente de triagem de leads no WhatsApp
- [ ] Dashboard interno: visão consolidada de todas as camadas

### Fase 4 — Loop de Crescimento
- [ ] NurturingAgent: sequência de conteúdo por segmento de lead
- [ ] OverdueAlert: inadimplência → alerta automático
- [ ] FMO re-assessment anual automatizado
- [ ] Expansion trigger: proposta automática baseada em gap FMO

---

*Thronus AI OS v1.0 — Agosto 2026*
*Documento interno — não divulgar sem autorização.*
