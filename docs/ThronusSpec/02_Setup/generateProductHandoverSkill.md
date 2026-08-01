# Skill: generateProductHandoverSkill (Metodologia TCA)

## 1. Objetivo Operacional
Executar o encerramento macro de produto quando a trilha de desenvolvimento atinge 100% de conclusão no `cronograma_trilha.json`. Este skill analisa o estado consolidado em `projeto_payload.json`, consome de forma síncrona as documentações históricas e editais presentes na pasta de referência, e realiza a engenharia reversa do código vivo para gerar de forma cirúrgica e incremental os manuais, materiais de onboarding e centrais de ajuda contextual embarcadas.

## 2. Fontes de Contexto e Base de Conhecimento (Contrato Obrigatório)
Para alimentar a inteligência de negócio deste Skill, o motor de IA deve ler obrigatoriamente e de forma integral todo o conteúdo contido no seguinte diretório:
* **Caminho da Base Referencial:** `docs/ThronusSpec/01_Planejamento/Base referencial da especificacao/`
* **Diretriz de Leitura:** Absorver todas as especificações funcionais, regras de negócio, editais jurídicos e fluxos históricos presentes nos arquivos deste diretório (sejam arquivos `.pdf`, `.md`, `.txt`, etc.). 
* **Baseline Inicial:** Caso a pasta esteja vazia, as novas documentações de base históricas inseridas pelo operador neste local servirão como o contexto documental mandatório para o processamento.

## 3. Diretriz Crítica: Escopo Incremental e Não Destrutivo
A IA está terminantemente PROIBIDA de apagar, sobrescrever ou corromper escopos consolidados de outras funcionalidades que já estão prontas no sistema. O escopo de elaboração deve ser cirúrgico:
* Aplique as modificações e acréscimos documentais **apenas no contexto ao qual a nova informação ou alteração de fluxo impacta**.
* Garanta a integridade de todas as outras telas e módulos previamente documentados nos manuais.

## 4. Protocolo de Geração e Entrega (Passo a Passo)

Cruzando a base referencial de planejamento com a varredura física da arquitetura do repositório, a IA atualizará incrementalmente os seguintes artefatos imutáveis de negócio:

### Passo 4.1: Roteiros de Homologação (QA Humano)
* **Caminho:** `docs/ThronusSpec/04_Gates_e_CI/roteiros_teste_manual.md`
* **Diretriz:** Adicionar guias passo a passo de teste caixa-preta para usuários validarem as novas implementações no ambiente de staging. Conter: Nome do caso de uso, Dados de entrada recomendados, Ações do operador e Resultado esperado.

### Passo 4.2: Manual Geral de Operação do Sistema
* **Caminho:** `docs/ThronusSpec/01_Planejamento/MANUAL_USUARIO.md`
* **Diretriz:** Integrar de forma harmoniosa no manual em linguagem universal e não técnica o funcionamento real das novas telas e processamentos. Mapear explicitamente novos status e alertas.

### Passo 4.3: Programa de Onboarding Customizado por Perfil (Suporte Zero)
* **Caminho:** `docs/ThronusSpec/01_Planejamento/ONBOARDING_PERFIS.md`
* **Diretriz:** Atualizar as trilhas de aprendizado focadas para cada um dos perfis ativos identificados no nó `perfis_e_permissoes_ativos` do payload. Para cada perfil afetado pela mudança, adicione: Escopo de Atuação (RBAC), Nova Rotina Diária sugerida e Guia Rápido de Erros Comuns.

### Passo 4.4: Central de Ajuda Contextual & Onboarding Embarcado (Agnóstico)
* **Auto-Detecção de Stack:** Inspecionar a raiz do projeto por reflexão para identificar a arquitetura ativa de apresentação (ex: Django Templates, React, Vue, Blade, HTML puro). Determinar autonomamente a melhor solução, biblioteca e formato de Help (fragmentos, componentes ou parciais).
* **Local de Destino:** Injetar os componentes de ajuda diretamente no diretório nativo de telas/views do frontend encontrado no repositório.
* **UX de Apoio:** Segmentar por perfil logado e focar na interface em execução. O texto deve utilizar o nome literal e exato dos botões de ação, modais e URLs reais extraídas do código de roteamento.
* **Componentes Visuais:** Incluir ou atualizar diagramas em formato **Mermaid.js** para ilustrar cronogramas, fluxos de dados ou regras restritivas da entrega atual.

## 5. Resposta Esperada no Terminal
Após persistir as atualizações síncronas dos quatro documentos com sucesso, a IA deve emitir exclusivamente o seguinte sumário de encerramento:

* **[TCA_HANDOVER_SUCCESS] ATIVOS DE NEGÓCIO E COMPONENTES DE HELP ATUALIZADOS CIRURGICAMENTE**
* **Base Referencial Utilizada:** docs/ThronusSpec/01_Planejamento/Base referencial da especificacao/
* **Arquivos Modificados Incrementalmente:**
  - `docs/ThronusSpec/04_Gates_e_CI/roteiros_teste_manual.md`
  - `docs/ThronusSpec/01_Planejamento/MANUAL_USUARIO.md`
  - `docs/ThronusSpec/01_Planejamento/ONBOARDING_PERFIS.md`
  - [Listar dinamicamente os caminhos e formatos dos componentes de Help injetados/atualizados]
* **Arquitetura Detectada:** [Framework e Tecnologia identificados no repositório]
* **Status:** `PRODUÇÃO_READY_FOR_DEPLOY`.