# FMO AI-First — Framework de Maturidade Operacional

**Versão:** 1.0 · Agosto 2026  
**Uso:** Interno Thronus Digital — diagnóstico de clientes PME antes do Discovery TCA

---

## 1. Propósito

O FMO é o instrumento de diagnóstico que precede toda entrega Thronus. Ele responde: *Onde está essa empresa hoje e o que precisa acontecer antes de construir qualquer solução de IA?*

O diagnóstico qualifica o lead, dimensiona o escopo, alimenta o TCA e protege o ROI do cliente — porque tecnologia aplicada antes de maturidade mínima gera desperdício, não valor.

---

## 2. Cinco Dimensões × Cinco Níveis

| Dimensão       | O que mede                                           |
|----------------|------------------------------------------------------|
| **Processos**  | Como o trabalho acontece, é documentado e passado adiante |
| **Dados**      | Onde as informações ficam, como são acessadas e usadas |
| **Governança** | Responsabilidades, controles, rastreabilidade e compliance |
| **Qualificação** | Capacidade da equipe de adotar e usar tecnologia   |
| **Receptividade** | Como a organização reage à mudança               |

Cada dimensão recebe um nível de **1 a 5**, definido por comportamentos observáveis — nunca por intenção declarada ou auto-avaliação.

---

## 3. Dois Tiers de Diagnóstico

### Tier 1 — Raio-X Operacional (isca de lead)
- 12 perguntas · 10 minutos
- Múltipla escolha A–D · self-serve
- Gratuito ou custo simbólico
- Output: radar 5D + 3 quick wins + etapa recomendada + CTA para Tier 2
- Escala: 1–4 por dimensão (escala parcial)

### Tier 2 — Diagnóstico AI-First (diagnóstico completo)
- 26 perguntas + conversa guiada
- Múltipla escolha + perguntas abertas comportamentais
- Conduzido pela Thronus (agente IA + validação humana)
- Incluso no projeto ou como serviço avulso
- Output: `fmo_assessment.json` + relatório + proposta de Discovery
- Escala: 1–5 por dimensão (escala completa)

### Pipeline
```
Raio-X (T1)  →  lead qualificado  →  Diagnóstico AI-First (T2)  →  fmo_assessment.json  →  TCA Discovery
```

---

## 4. Princípios de Design do Instrumento

### 4.1 Linguagem PME — o que nunca usar

As perguntas nunca usam os termos a seguir como conceitos abstratos:
- "processo", "governança", "maturidade digital", "KPI", "IA"

O que o respondente vê é uma **conversa sobre o negócio dele**, não um formulário de avaliação.

### 4.2 Comportamento, não intenção

Scoring sempre pelo comportamento **observado**, não pelo que o cliente *quer* fazer. "Queremos organizar nossos dados" é L1 ou L2, não L3. L3 é quando os dados *já estão* organizados.

### 4.3 Triangulação por contradição

O Tier 2 pede a mesma informação de ângulos diferentes para revelar a maturidade real vs. a percebida. Exemplos:
- Q1 (como o novo aprende) + Q5 (o que acontece quando alguém sai) → revela dependência real de pessoas
- Q3 (relatório de clientes) + FD5 (última decisão importante) → revela uso real de dados vs. intuição

### 4.4 Proxies quantitativos

Sempre que possível, substituir rating subjetivo por estimativa concreta:
- Não: "De 1 a 5, quão eficientes são seus processos?"
- Sim: "Quantas horas por semana a equipe gasta em tarefas repetitivas?"

### 4.5 Mapeamento para etapa do portfólio

| Score médio FMO | Etapa recomendada       |
|-----------------|-------------------------|
| 1.0–1.5         | Pré-condições: organização antes de automação |
| 1.5–2.5         | Etapa 1: Automação e Agentes de IA            |
| 2.5–3.5         | Etapa 2: Operações Inteligentes               |
| 3.5–4.5         | Etapa 3: Produto Digital Sob Medida           |
| 4.5–5.0         | Etapa 4: Growth e Mercado                     |

---

## 5. Regras de Scoring

1. **L1** quando o comportamento descrito é totalmente reativo, informal e dependente de memória
2. **L2** quando há algum registro ou estrutura informal, mas sem consistência
3. **L3** quando a prática já existe e é seguida de forma consistente pela maioria
4. **L4** quando a prática é monitorada e gera melhoria contínua com dados
5. **L5** quando a automação/IA é parte da norma operacional, não uma exceção

**Regra de arredondamento:** Score 2.3 → L2 (arredonda para baixo). Conservador é melhor que otimista: o cliente prefere ser surpreendido positivamente na entrega.

---

## 6. Output Principal: `fmo_assessment.json`

Gerado ao final do Tier 2 e lido pelo `fmoToDiscoveryBridgeSkill` para pré-popular o `discovery.md` do TCA.

Ver: `fmo_assessment_template.json` neste diretório.

---

## 7. Arquivos deste Diretório

| Arquivo                         | Conteúdo                                        |
|---------------------------------|-------------------------------------------------|
| `fmo_metodologia.md`            | Este documento — visão geral e princípios       |
| `fmo_tier1_questoes.md`         | 12 perguntas do Raio-X com opções e scoring     |
| `fmo_tier2_questoes.md`         | 26 perguntas do Diagnóstico AI-First            |
| `fmo_rubrica.md`                | Âncoras comportamentais 5D × 5 níveis           |
| `fmo_assessment_template.json`  | Schema do arquivo de saída do diagnóstico       |
| `fmo_dimensionamento.md`        | Como scores traduzem em escopo e custo Discovery|
