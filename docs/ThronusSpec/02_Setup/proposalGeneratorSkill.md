# Skill: proposalGeneratorSkill (Metodologia TCA v2 — Inteligência Comercial)

## 1. Objetivo Operacional
Transformar os artefatos de entrega do TCA em material comercial reutilizável: case study anonimizável, template de proposta para projetos similares e boilerplate de escopo técnico. Fecha o loop entre a capacidade de entrega (Diego) e o desenvolvimento de mercado (Bernardo).

**Ativação:** Invocado ao término de um projeto (`generateProductHandoverSkill.md` concluído) ou sob demanda: "Gere proposta para projeto similar a [MS-range]."

---

## 2. Protocolo de Geração

### Passo 2.1: Leitura dos Artefatos de Entrega
* `docs/ThronusSpec/01_Planejamento/discovery.md` — problema, stakeholders, métricas de sucesso
* `docs/ThronusSpec/01_Planejamento/functional_model.md` — escopo e casos de uso
* `docs/ThronusSpec/01_Planejamento/architecture_decision.md` — ADR e decisões de stack
* `payload_index.json → estado_da_trilha` — MSs concluídas, cobertura, tempo total
* `payload_archive/*.json` — contratos entregues (para extrair complexidade)
* `05_Monitoramento/performance_logs.json` — métricas de qualidade e velocidade

### Passo 2.2: Geração do Case Study

Produzir em `docs/ThronusSpec/05_Monitoramento/case_study_[ANO].md`:

```markdown
# Case Study — [Categoria do Projeto] | Thronus Digital

## Contexto
**Setor:** [setor do cliente — anonimizável]
**Porte:** [MPE / Média / Grande]
**Problema:** [enunciado canônico do discovery.md]
**Situação inicial (FMO):** [níveis das dimensões relevantes]

## Solução construída
[Descrição não-técnica do que foi entregue]
**Arquitetura:** [resumo do ADR em linguagem de negócio]

## Resultado
| Indicador                    | Antes        | Depois         |
|------------------------------|--------------|----------------|
| [métrica do discovery]       | [baseline]   | [resultado]    |
| Funcionalidades entregues    | —            | [N] MSs        |
| Cobertura de testes          | —            | [N]%           |
| Bugs em produção             | —            | 0              |
| Prazo                        | [estimado]   | [realizado]    |

## Diferenciais aplicados
- [ADR: decisão 1 e por que foi certa para este cliente]
- [Gate: validação que evitou retrabalho]
- [TDD: como os testes garantiram a entrega sem regressões]

*Cliente anonimizado a pedido. Detalhes disponíveis em NDA.*
```

### Passo 2.3: Geração do Template de Proposta

Produzir em `docs/ThronusSpec/05_Monitoramento/proposta_template_[CATEGORIA].md`:

```markdown
# Proposta de Projeto — [Categoria]
**Preparada por:** Thronus Digital | [data]

## Diagnóstico inicial
[Problemas típicos desta categoria, derivados do FMO]

## Escopo proposto
**Perfil TCA:** [nano/micro/standard/enterprise]
**Estimativa de Micro Specs:** [range baseado em projetos similares]
**Estimativa de prazo:** [range baseado em velocidade histórica]
**Cobertura mínima de testes:** [% conforme perfil]

## Entregas por fase
| Fase        | Entrega                              | Duração estimada |
|-------------|--------------------------------------|------------------|
| Diagnóstico | FMO + Discovery validado             | [N dias]         |
| Arquitetura | ADR aprovado + stack definida        | [N dias]         |
| Ciclo [N]   | [MSs típicas desta categoria]        | [N semanas]      |

## Garantias de qualidade
- TDD obrigatório: código só existe após testes comprovarem a necessidade
- Cobertura mínima: [N]%
- Zero deploys sem health check automático
- Relatório de progresso mensal em linguagem não-técnica
- Rastreabilidade total: cada funcionalidade ligada a um requisito de negócio

## Sustentação pós-entrega
[Tier recomendado para este tipo de projeto + justificativa]

## Investimento
[A ser definido após diagnóstico AI-First]
```

### Passo 2.4: Exportar para o CRM
Se `payload_index.json → integracoes.crm` estiver configurado:
* Criar registro de "Projeto concluído" com as métricas do case study
* Marcar o segmento de mercado para uso em prospecção de projetos similares
* Sugerir 3 empresas do mesmo segmento no CRM para abordagem proativa (se dados disponíveis)

---

## 3. Saída Esperada no Terminal

```
[TCA_PROPOSAL_GENERATOR_OK] MATERIAL COMERCIAL GERADO
  Case study      : docs/.../case_study_[ANO].md
  Template proposta: docs/.../proposta_template_[CATEGORIA].md
  Segmento        : [setor] — [porte]
  Métricas-chave  : [N] MSs | [N]% cobertura | [N] dias | 0 bugs prod
  CRM             : [registrado | não configurado]
  Próximo uso     : compartilhar com equipe comercial para prospecção em [setor]
```
