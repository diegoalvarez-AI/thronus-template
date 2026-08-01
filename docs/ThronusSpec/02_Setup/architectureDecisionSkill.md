# Skill: architectureDecisionSkill (Metodologia TCA — Fase Pré-Código)

## 1. Objetivo Operacional
Tomar e documentar as decisões de arquitetura técnica do projeto com base nas restrições e no modelo funcional já mapeados — nunca por preferência pessoal ou tecnologia de moda. A saída é um ADR (Architecture Decision Record) assinado e o `payload_index.json` atualizado com o stack decidido.

**Ativação:** Obrigatória em todos os perfis.

**Insumos:**
- `docs/ThronusSpec/01_Planejamento/discovery.md` (perfil, restrições, equipe)
- `docs/ThronusSpec/01_Planejamento/functional_model.md` (volume, complexidade, integrações)

---

## 2. Framework de Decisão Arquitetural

### Passo 2.1: Perfil do Projeto (4 dimensões)

Avaliar cada dimensão em uma escala de 1–3:

| Dimensão | 1 (Simples) | 2 (Moderado) | 3 (Complexo) |
|----------|-------------|--------------|--------------|
| **Volume de dados** | < 10k registros | 10k–1M | > 1M ou streaming |
| **Concorrência** | Solo / sequencial | Dezenas de usuários simultâneos | Centenas+ / tempo real |
| **Integrações** | Zero ou 1 API externa | 2–4 integrações | 5+ / sistemas legados críticos |
| **Longevidade** | Descartável / POC | 1–3 anos | 3+ anos / produto central |

**Score total** (soma das 4 dimensões):
- 4–6: Perfil Nano/Micro → arquitetura simples é a decisão certa
- 7–9: Perfil Standard → monólito bem estruturado
- 10–12: Perfil Enterprise → considerar separação de domínios

### Passo 2.2: Padrão Arquitetural
Com base no score, selecionar e justificar o padrão:

**Monólito Modular** (score 4–9): Uma única base de código com separação de responsabilidades por módulo/pasta. Recomendado para a maioria dos projetos de PME e governo. Evolui para microserviços se necessário.

**BFF + SPA** (quando UI complexa + API estável): Backend For Frontend servindo uma API; frontend em framework reativo. Usar quando a experiência do usuário é o diferencial.

**Serverless / Functions** (score 4–6 + equipe pequena): Sem gestão de servidor, custo por uso. Ideal para automações, webhooks, integrações pontuais.

**Microserviços** (score 10–12 + equipe > 5 + domínios claramente separados): Somente quando os domínios têm ciclos de vida e equipes INDEPENDENTES. Nunca por antecipação.

**Jamstack / Static + API** (conteúdo predominante): Quando 80%+ do conteúdo é leitura e a escrita é eventual.

### Passo 2.3: Seleção de Tecnologia

Para cada camada, documentar a decisão e a justificativa:

```
CAMADA: [Linguagem principal]
  Decisão: [linguagem/runtime escolhido]
  Justificativa: [por que essa, não outra]
  Alternativa descartada: [qual e por quê foi descartada]

CAMADA: [Framework de aplicação]
  Decisão: [framework escolhido]
  ...

CAMADA: [Persistência]
  Decisão: [banco de dados e modo de acesso]
  ...

CAMADA: [Infraestrutura / Hosting]
  Decisão: [onde roda e como é operado]
  ...

CAMADA: [Frontend / Interface]
  Decisão: [se aplicável: framework, SSR vs CSR vs MPA]
  ...
```

**Regra de ouro da seleção:** A tecnologia escolhida deve ser a **mais simples que resolve o problema**, não a mais poderosa disponível. Complexidade técnica prematura é o maior inimigo de projetos pequenos.

### Passo 2.4: Decisões Transversais

- **Autenticação**: JWT / sessão / OAuth / SAML / sem auth (justificar)
- **Autorização**: RBAC / ABAC / simples (admin/não-admin)
- **Observabilidade**: logs estruturados / APM / none (proporcional ao SLA)
- **Testes**: estratégia de testes adequada ao stack escolhido
- **CI/CD**: GitHub Actions / GitLab CI / sem pipeline (justificar)
- **Containerização**: Docker / bare metal / PaaS (justificar)

### Passo 2.5: ADR — Architecture Decision Record

```
# ADR-001: [Título da decisão principal]

**Data:** [data]
**Status:** Aceito

## Contexto
[O que motivou essa decisão — restrições, escopo, equipe]

## Decisão
[A decisão tomada em uma frase]

## Stack Completo
[Lista do stack decidido por camada]

## Consequências
Positivas: [o que a decisão facilita]
Negativas / trade-offs: [o que essa decisão sacrifica conscientemente]
Riscos residuais: [o que pode dar errado e como detectar]
```

---

## 3. Output Obrigatório

1. Escrever `docs/ThronusSpec/01_Planejamento/architecture_decision.md` com o ADR completo.
2. Atualizar `docs/ThronusSpec/03_Desenvolvimento/payload_index.json`:
   - Preencher `arquitetura_e_padroes` com as decisões tomadas
   - Preencher `dependencias` com o stack decidido
   - Definir `padrao_testes` com a estratégia adequada ao stack
3. Aplicar o starter tecnológico correspondente (se existir em `starters/`), ou criar o scaffold manualmente.

Emitir `STATUS_ARCHITECTURE_CONCLUIDO` e transitar para `[ESTADO_SPEC]`.
