# Skill: monitorEvolutionMetricsSkill (Metodologia TCA)

## 1. Objetivo Operacional
Executar o procedimento de fechamento de ciclo pós-desenvolvimento (Post-Execution Check) após o sucesso da implementação técnica. Este skill audita o estado final do código, extrai indicadores de infraestrutura e consolida o avanço do módulo no mapa de coordenadas, preparando o ambiente para o descarte da sessão corrente [source: 1].

## 2. Protocolo de Consolidação e Registro (Passo a Passo Obrigatório)

### Passo 2.1: Verificação da Cobertura e Estabilidade de Testes
* O motor de IA deve inspecionar os arquivos de log locais da suíte de execução de testes para garantir que 100% dos testes do ciclo atual passaram com sucesso [source: 1].
* Deve confirmar que a taxa de cobertura de código do módulo foi mantida ou expandida e que nenhuma regressão foi causada no código legado estável.

### Passo 2.2: Auditoria Estrutural e Impacto Postgres
* A IA deve analisar as novas declarações de modelos ou arquivos de migração gerados no ciclo para catalogar na pasta de engenharia `docs/ThronusSpec/05_Monitoramento/` [source: 1].
* Deve identificar novos relacionamentos físicos, chaves estrangeiras e índices adicionados, documentando o impacto e estimando a projeção de crescimento de dados com base na volumetria descrita nos requisitos.

### Passo 2.3: Atualização do Snapshot de Estado Permanente
* A IA deve ler o arquivo `docs/ThronusSpec/03_Desenvolvimento/projeto_payload.json` e aplicar um incremento síncrono.
* Deve atualizar o campo `ultima_micro_spec_concluida` com o respectivo ID/Nome da tarefa finalizada [source: 1].
* Deve atualizar o campo `status_modulo_percentual`, recalculando o progresso da trilha com base no cronograma de planejamento [source: 1].
* Deve injetar os novos modelos estáveis, funções reutilizáveis e assinaturas de serviços criados dentro dos dicionários técnicos do JSON [source: 1].

### Passo 2.4: Liberação da Memória RAM
* Após assegurar que o snapshot técnico foi gravado no disco com sucesso, a IA deve abrir o arquivo `context/activeContext.md` e esvaziar completamente o seu conteúdo [source: 1]. Isso impede que contextos defasados causem ruído ou poluição de tokens no "Cold Start" da próxima sessão limpa [source: 1].

## 3. Resposta Esperada no Terminal
A IA deve emitir exclusivamente o seguinte sumário executivo:

* **[TCA_CYCLE_CLOSED] SUCESSO NA CONSOLIDAÇÃO**
* **Spec Concluída e Registrada:** [Nome da micro spec extraída da RAM antes da limpeza] [source: 1].
* **Alterações no Payload:** [Listar novos elementos persistidos no projeto_payload.json] [source: 1].
* **Métricas de Infraestrutura:** [Indicação de novos índices criados / projeção de volumetria] [source: 1].
* **Status:** `CICLO_CONCLUIDO_RAM_LIMPA`. Sistema pronto para receber o próximo ciclo evolutivo.