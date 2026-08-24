# Skill: generateProductHandoverSkill (Metodologia TCA v2)

## 1. Objetivo Operacional
Executar o encerramento macro do produto quando a trilha de desenvolvimento atinge 100% de conclusão. Gera documentação operacional, roteiros de homologação e materiais de onboarding derivados do código real e dos artefatos TCA acumulados durante o projeto.

**Ativação:** Invocado manualmente após o gate de encerramento de cada perfil (ex: `GATE_ENCERRAMENTO` em Standard/Enterprise). Não faz parte do ciclo por MS — é executado uma vez ao final do produto.

---

## 2. Fontes de Contexto

* `docs/ThronusSpec/01_Planejamento/discovery.md` — problema, stakeholders, critérios de sucesso
* `docs/ThronusSpec/01_Planejamento/functional_model.md` — casos de uso, regras de negócio, glossário
* `docs/ThronusSpec/01_Planejamento/architecture_decision.md` — ADR, stack, decisões transversais
* `docs/ThronusSpec/03_Desenvolvimento/payload_index.json` — estado final da trilha, modelos e serviços
* `docs/ThronusSpec/03_Desenvolvimento/payload_archive/` — contratos de todas as MSs entregues
* `docs/ThronusSpec/01_Planejamento/Base referencial da especificacao/` — editais, contratos, especificações originais (se presentes)

Usar leitura dirigida (CAP-SEARCH) para inspecionar arquivos de código grandes (views, rotas, modelos) em vez de carregá-los inteiros.

---

## 3. Diretriz de Escopo Incremental e Não Destrutivo
A IA está proibida de apagar ou sobrescrever documentação já aprovada. Toda atualização é **incremental**: adiciona ou corrige apenas o que a nova MS/entrega impacta, preservando o restante intacto.

---

## 4. Artefatos Gerados

### Passo 4.1: Roteiros de Homologação (QA Humano)
* **Destino:** `docs/ThronusSpec/04_Gates_e_CI/roteiros_teste_manual.md`
* Guias passo a passo para validação caixa-preta em staging: nome do caso de uso, dados de entrada, ações do operador, resultado esperado.
* Derivar dos cenários BDD de cada MS — mas escritos em linguagem não técnica para o validador humano.

### Passo 4.2: Manual de Operação do Sistema
* **Destino:** `docs/ThronusSpec/01_Planejamento/MANUAL_USUARIO.md`
* Linguagem não técnica, orientada ao usuário final.
* Mapear: fluxos principais, novos status e alertas, erros comuns e como resolvê-los.
* Estruturar por perfil de acesso (RBAC) identificado em `payload_index.json → perfis_e_permissoes_ativos`.

### Passo 4.3: Programa de Onboarding por Perfil
* **Destino:** `docs/ThronusSpec/01_Planejamento/ONBOARDING_PERFIS.md`
* Para cada perfil ativo: escopo de atuação (o que pode e não pode fazer), rotina diária sugerida, guia rápido de erros comuns.
* Usar os nomes reais de botões, menus e URLs extraídos do código de roteamento.

### Passo 4.4: Central de Ajuda Contextual (Embarcada no Produto)
* **Auto-detecção de stack:** Identificar o framework de frontend em uso (Django Templates, React, Vue, HTML/HTMX, Blade, etc.) e produzir os componentes no formato nativo.
* **Segmentação por perfil:** O conteúdo de ajuda é filtrado pelo perfil do usuário logado.
* **Diagramas:** Incluir diagramas Mermaid.js para fluxos complexos (pipelines, regras de desempate, estados de aprovação).
* **Injeção:** Os componentes de ajuda vão diretamente para o diretório de templates/views identificado no projeto.

---

## 5. Saída Esperada no Terminal

```
[TCA_HANDOVER_SUCCESS] DOCUMENTAÇÃO OPERACIONAL GERADA
  Base referencial    : [arquivos utilizados]
  Arquivos produzidos :
    - docs/.../roteiros_teste_manual.md
    - docs/.../MANUAL_USUARIO.md
    - docs/.../ONBOARDING_PERFIS.md
    - [componentes de help injetados no frontend]
  Stack detectada     : [framework e tecnologia do projeto]
  Status              : PRODUTO_PRONTO_PARA_DEPLOY ✓
```
