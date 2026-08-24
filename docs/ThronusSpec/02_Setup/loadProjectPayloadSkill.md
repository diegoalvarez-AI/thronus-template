# Skill: loadProjectPayloadSkill (Metodologia TCA v2 — Tiered Context)

## 1. Objetivo Operacional
Executar a inicialização de contexto ("Cold Start") de forma eficiente, carregando apenas o contexto necessário em três camadas progressivas. O custo de contexto alvo por sessão é ≤ 15k tokens antes de escrever qualquer linha de código.

---

## 2. Camada 1 — Hot Context (Sempre Carregado)

### Passo 2.1: Carregar o índice técnico mínimo
* Ler `docs/ThronusSpec/03_Desenvolvimento/payload_index.json` (≈14 KB — sempre disponível).
  * Este arquivo contém: arquitetura, dependências, modelos, serviços reutilizáveis, perfis, `estado_da_trilha`, e a lista de chaves no archive (`_archive.keys`).
  * **NÃO carregar** `docs/ThronusSpec/03_Desenvolvimento/projeto_payload.json` (arquivo legado completo, 81 KB).
* Verificar `estado_da_trilha.micro_spec_ativa` e `ultima_micro_spec_concluida`.

### Passo 2.2: Verificar o contexto de sessão ativo
* Ler `docs/ThronusSpec/03_Desenvolvimento/context/activeContext.md`.
  * Se o arquivo contiver uma Micro Spec ativa (não o marcador de "nenhuma spec"), confirmar que a spec não foi interrompida e continuar do ponto correto.
  * Se estiver vazio ou com marcador de sessão limpa: prosseguir para geração de nova spec (Passo 3).

---

## 3. Camada 2 — Warm Context (MS Ativa)

### Passo 3.1: Identificar contratos relevantes para a MS ativa
* Determinar quais contratos do archive são necessários para a MS em desenvolvimento (ex: se a MS usa `ConsolidacaoLoteService`, carregar `ms008.json`).
* Usar **leitura dirigida (CAP-SEARCH)** para localizar dependências cirúrgicas: em vez de ler arquivos-alvo inteiros (ex: um módulo com 3k linhas), delegar a um subagente de exploração — ou, sem ele, usar `grep -n` — para retornar apenas o ponto de inserção:
  ```
  "Localize em admin.py a classe [ClassName] e retorne: número da linha, superclasse, 
   e os 5 campos imediatamente antes e depois do ponto de inserção ideal para [nova_classe]."
  ```
* Carregar apenas os arquivos `payload_archive/<ms_NNN>.json` identificados como dependências diretas.

### Passo 3.2: Geração e Validação de Escopo (Loop Fechado)
1. **GERAÇÃO:** Ler as regras lógicas e contratos na pasta de planejamento (`01_Planejamento/`), fatiando a próxima tarefa pendente e escrevendo os cenários BDD em `context/activeContext.md` com o formato padrão completo (objetivo, modelo de dados, URLs, views, template, cenários CT-01..CT-N, arquivos a criar/modificar, dependências, invariantes).
2. **VALIDAÇÃO:** Confrontar a spec gerada contra as fontes brutas, garantindo que não haja simplificações de regras de negócio ou omissões de schemas.
3. **FEEDBACK LOOP:** Se houver gaps, reescrever a spec automaticamente. Se 100% aderente, encerrar o loop.

---

## 4. Camada 3 — Cold Context (Demanda Explícita)

* Arquivos `payload_archive/<ms_XXX>.json` de MSs históricas não relacionadas à MS ativa são carregados **somente se explicitamente necessário** para resolver uma dependência de contrato.
* Arquivos de código fonte grandes são lidos **somente na faixa de linhas identificada pela leitura dirigida (CAP-SEARCH)**, nunca inteiros.
* **Sentinela de contexto:** Antes de qualquer leitura de arquivo ≥ 200 linhas, estimar o custo em tokens. Se o total acumulado da sessão ultrapassar 40k tokens de leitura, preferir a leitura dirigida (CAP-SEARCH) à leitura direta.

---

## 5. Transição de Saída (Opcionalidade Proibida)
Após validação 100% do escopo em `context/activeContext.md`, o motor de IA emite o status `STATUS_DOCUMENTACAO_LIBERADA` e transita imediatamente para `[ESTADO_PLAN]`, invocando `evaluatePlanIntegritySkill.md`.

**Não encerrar o comando após a validação do escopo.**
