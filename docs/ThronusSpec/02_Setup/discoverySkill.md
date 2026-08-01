# Skill: discoverySkill (Metodologia TCA — Fase Pré-Código)

## 1. Objetivo Operacional
Transformar uma ideia bruta em um problema de negócio bem definido, com stakeholders mapeados, fluxos essenciais identificados e critérios de sucesso mensuráveis. A saída deste skill é o único insumo necessário para o `functionalModelingSkill`.

**Ativação:** Obrigatória em perfis Standard e Enterprise. Obrigatória em Micro. Simplificada em Nano (apenas §2.1 e §2.4).

---

## 2. Protocolo de Descoberta (Loop de Refinamento)

### Passo 2.1: Enunciação do Problema
Formular o problema em uma frase canônica:
> "**[Quem]** precisa de **[o quê]** para **[por quê]**, mas hoje isso é difícil porque **[obstáculo]**."

Se a frase não puder ser completada sem ambiguidade, a descoberta não terminou. Reformular até que seja inequívoca.

### Passo 2.2: Mapa de Stakeholders
Para cada ator identificado, documentar:
- **Papel**: quem é (usuário final, pagador, decisor, parceiro técnico, regulador)
- **Dor principal**: o que os impede hoje
- **Ganho esperado**: o que muda com a solução
- **Poder de bloqueio**: pode impedir o projeto? (alto / médio / baixo)

### Passo 2.3: Jornadas de Negócio (Top 3–5)
Para cada jornada essencial (não features — processos de negócio):
```
ATOR → [ação] → SISTEMA → [resposta] → RESULTADO DE NEGÓCIO
```
Identificar: jornadas **felizes** (caminho ideal) e **críticas** (o que não pode falhar).

### Passo 2.4: Critérios de Sucesso (Mensuráveis)
Definir 3–5 métricas concretas que provam que o projeto entregou valor:
- Quantitativas: "Reduz tempo de X de Y horas para Z minutos"
- Qualitativas com proxy: "Satisfação do usuário ≥ 4/5 após 30 dias de uso"
- Negativas (o que não deve piorar): "Tempo de resposta do sistema atual ≤ 2s mantido"

### Passo 2.5: Restrições e Premissas
- **Orçamento** (faixa): zero / bootstrapped / PME / enterprise
- **Prazo** (faixa): dias / semanas / meses / trimestres
- **Tamanho da equipe**: solo / duo / pequeno time (≤5) / time médio (6–15)
- **Integrações obrigatórias**: sistemas legados, APIs externas, regulamentações
- **Restrições técnicas não-negociáveis**: infraestrutura existente, idioma da equipe, licenças

### Passo 2.6: Registro de Riscos (Top 3–5)
| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| ...   | Alto/Médio/Baixo | Alto/Médio/Baixo | ... |

---

## 3. Output Obrigatório
Escrever `docs/ThronusSpec/01_Planejamento/discovery.md` com todas as seções preenchidas.

Emitir `STATUS_DISCOVERY_CONCLUIDO` e transitar para `[ESTADO_FUNCTIONAL]` (ou para `[ESTADO_ARCHITECTURE]` em perfil Nano).
