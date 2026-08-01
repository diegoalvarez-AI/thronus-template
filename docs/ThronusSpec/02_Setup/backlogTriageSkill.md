# Skill: backlogTriageSkill (Metodologia TCA v2)

## 1. Objetivo Operacional
Classificar, dimensionar e priorizar automaticamente qualquer demanda de cliente — bug, nova feature, ajuste de regra, refatoração ou integração — e inserir a Micro Spec correspondente no backlog do `payload_index.json`, pronta para ser ativada no próximo ciclo TDD.

**Ativação:** Invocado quando chega uma demanda nova durante o ciclo de manutenção evolutiva. Pode ser acionado manualmente ("Triage esta demanda: …") ou por hook de issue tracker.

---

## 2. Protocolo de Triagem

### Passo 2.1: Leitura de Contexto
* Carregar `docs/ThronusSpec/03_Desenvolvimento/payload_index.json` (Hot tier).
* Identificar o maior MS-ID existente para gerar o próximo ID sequencial.
* Carregar `payload_index.json → servicos_e_regras_existentes_reutilizaveis` para detectar dependências.

### Passo 2.2: Classificação do Tipo
Aplicar a seguinte heurística sobre o texto da demanda:

| Sinal no texto                                           | Tipo              |
|----------------------------------------------------------|-------------------|
| "não funciona", "quebrou", "erro", "clientes reclamam"  | `bug_fix`         |
| "novo módulo", "queria adicionar", "precisa de"          | `nova_feature`    |
| "mudou a regra", "edital atualizado", "critério mudou"   | `mudanca_regra`   |
| "reorganizar", "melhorar estrutura", "extrair", "limpar" | `refatoracao`     |
| "conectar com", "integrar", "API de", "sistema X"        | `integracao`      |

Se ambíguo, preferir `nova_feature`. Registrar a ambiguidade no campo `_nota` da MS.

### Passo 2.3: Dimensionamento
Estimar o tamanho baseado na complexidade declarada e no histórico de tamanhos do payload_archive:

| Tamanho | Critério de referência                                                        |
|---------|-------------------------------------------------------------------------------|
| P       | 1 arquivo modificado, regra pontual, sem migration, ≤ 3 CTs esperados        |
| M       | 2–4 arquivos, nova validação ou novo serviço, ≤ 6 CTs esperados              |
| G       | Novo módulo com Port/Adapter, migration, ≥ 7 CTs, testes de integração       |
| GG      | Múltiplos módulos interdependentes — decompor em 2–4 MSs de tamanho G ou M   |

Se GG detectado: propor decomposição antes de inserir no backlog.

### Passo 2.4: Avaliação de Prioridade
Cruzar urgência declarada × impacto no produto:

| Prioridade | Critério                                                            |
|------------|---------------------------------------------------------------------|
| CRÍTICO    | Bug em produção afetando usuários ativos / bloqueio de processo     |
| ALTO       | Mudança de regra contratual com prazo / nova feature com entrega    |
| MÉDIO      | Melhoria solicitada sem prazo definido                              |
| BAIXO      | Refatoração interna, débito técnico sem impacto imediato            |

### Passo 2.5: Detecção de Dependências
* Verificar se a demanda afeta serviços listados em `servicos_e_regras_existentes_reutilizaveis`.
* Verificar se depende de uma MS ainda `em_andamento` — se sim, registrar em `depende_de`.
* Para `mudanca_regra`: identificar no payload_archive todas as MSs que implementam a regra afetada — listar em `impacta_msids`.

### Passo 2.6: Inserção no Backlog
Adicionar ao array `backlog_micro_specs` em `payload_index.json`:

```json
{
  "id": "MS-NNN",
  "nome": "<nome imperativo conciso>",
  "tipo": "<bug_fix|nova_feature|mudanca_regra|refatoracao|integracao>",
  "tamanho": "<P|M|G>",
  "prioridade": "<CRÍTICO|ALTO|MÉDIO|BAIXO>",
  "status": "pendente",
  "origem": "<texto original da demanda ou referência ao ticket>",
  "depende_de": [],
  "impacta_msids": [],
  "_nota": "<observação opcional sobre ambiguidades>"
}
```

Inserir na posição correta respeitando prioridade: CRÍTICO no topo da fila pendente, BAIXO ao final.

---

## 3. Saída Esperada no Terminal

```
[TCA_TRIAGE_COMPLETE] DEMANDA CLASSIFICADA E INSERIDA NO BACKLOG
  ID atribuído  : MS-NNN
  Tipo          : <tipo>
  Tamanho       : <P|M|G>
  Prioridade    : <prioridade>
  Dependências  : <lista ou "nenhuma">
  Impacta MSs   : <lista ou "nenhuma">
  Posição fila  : <N>ª MS pendente
  Próximo passo : Inicie MS-NNN para ativar o ciclo TDD.
```

Se GG detectado:
```
[TCA_TRIAGE_GG_DETECTADO] DEMANDA REQUER DECOMPOSIÇÃO
  Proposta de decomposição:
    MS-NNN-A: <nome>  (tamanho G)
    MS-NNN-B: <nome>  (tamanho M)
  Confirme a decomposição ou forneça ajuste antes de inserir no backlog.
```
