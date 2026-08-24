# Skill: evaluatePlanIntegritySkill (Metodologia TCA v2)

## 1. Objetivo Operacional
Auditar criticamente o plano de implementação técnica antes de liberar a escrita de código. Executa no máximo **3 ciclos de auto-correção** (MAX_ITERATIONS=3). Se o plano não for aprovado em 3 iterações, emite rollback para revisão humana — sem looping infinito.

---

## 2. Protocolo de Auditoria (MAX_ITERATIONS = 3)

### Passo 2.1: Critérios de Inspeção Técnica

**A — Aderência BDD:**
* Cruzar o plano com `context/activeContext.md`. Cada cenário CT-XX deve ter uma estratégia técnica de código e um caso de teste correspondente desenhado. Mocks ou omissões geram rejeição imediata.

**B — Blindagem de Infraestrutura:**
> Aplicar conforme o stack decidido no ADR (`payload_index.json → arquitetura_e_padroes`). Os termos abaixo são conceituais, não específicos de um banco ou ORM.

* Verificar se coleções/tabelas de alta volumetria possuem índices compostos e constraints de unicidade.
* Verificar se o plano introduz novas constraints ou índices e se estão incluídos no artefato de migração gerado pelo stack.

**C — Conformidade de Legado:**
* Garantir que o plano reutiliza e estende os contratos catalogados no `payload_index.json` e nos `payload_archive/<ms_XXX>.json` relevantes.
* Proibir reescritas de contratos estáveis — verificar se a alteração prevista é uma extensão ou uma substituição.

**D — Isolamento de Camadas DDD:**
* Verificar que a camada `domain/` não importa nenhum framework nem biblioteca de infraestrutura — apenas a biblioteca padrão da linguagem.
* Verificar que a camada `application/` não importa modelos de persistência diretamente — usar apenas os contratos declarados em `application/ports/` (Protocol, interface, trait — conforme a linguagem).
* Verificar que a camada `infrastructure/` é o único ponto de acesso ao ORM, ao cliente HTTP e a qualquer I/O externo.

**E — Snapshot-Diff Pré-Código:**
* Listar explicitamente os arquivos que serão criados e modificados.
* Confirmar que nenhum arquivo fora do escopo definido em `activeContext.md` será tocado.

### Passo 2.2: Loop de Auto-Ajuste (MAX 3 ITERAÇÕES)

```
iteração = 0
enquanto iteração < 3:
    gaps = inspecionar(plano, critérios A–E)
    se gaps == []:
        → APROVADO: emitir [TCA_INTEGRITY_CHECK] e aguardar gate humano
    senão:
        listar gaps encontrados
        reescrever o plano automaticamente resolvendo os gaps
        iteração += 1

se iteração == 3 e gaps != []:
    → emitir STATUS_PLANO_REQUER_REVISAO_HUMANA
    → aguardar instrução (ROLLBACK [SPEC])
```

---

## 3. Resposta de Aprovação (Gate Humano)

Após aprovação interna, emitir o sumário e **aguardar uma confirmação humana** antes de transitar para `[ESTADO_RED]`. Esta é a única pausa obrigatória do pipeline — elimina o risco de compoundamento de erros silenciosos:

```
[TCA_INTEGRITY_CHECK] ARQUITETURA VALIDADA — AGUARDANDO GATE HUMANO

  Iterações de Ajuste : [N]
  Impacto persistência: [índices, constraints, tabelas/coleções criadas ou alteradas]
  Arquivos previstos  : [lista de creates e modifies]
  Gaps Residuais      : NENHUM
  Status              : STATUS_PLANO_CONFORME_LIBERADO_PARA_DESENVOLVIMENTO

  ► Confirme com OK para iniciar o ciclo TDD RED.
    Ou forneça correções adicionais para reiniciar a auditoria.
```

## 4. Resposta de Rejeição (Rollback)

```
[TCA_INTEGRITY_REJECTED] MAX_ITERATIONS ATINGIDO

  Iterações executadas : 3
  Gaps persistentes    : [lista detalhada]
  Status               : STATUS_PLANO_REQUER_REVISAO_HUMANA

  ► O plano requer intervenção arquitetural antes de prosseguir.
    Forneça diretrizes adicionais para reiniciar o ESTADO_PLAN.
```
