# Skill: sustentacaoSkill (Metodologia TCA v2 — Fase de Sustentação)

## 1. Objetivo Operacional
Estruturar e executar a fase de sustentação de produtos entregues pela Thronus: SLA formal, monitoramento recorrente, revisão de backlog, radar tecnológico periódico e trigger de reavaliação FMO. Transforma a promessa de "acompanhamento durante o ciclo de vida" em processo sistemático e auditável.

**Ativação:** Invocado uma única vez após o primeiro deploy bem-sucedido em produção (gate `PRODUTO_EM_PRODUCAO`). A partir daí, opera em ciclos automáticos conforme configuração.

---

## 2. Configuração de Sustentação

### Passo 2.1: Definir Tier de SLA
Ao ativar a sustentação, registrar em `payload_index.json → sustentacao`:

```json
{
  "sustentacao": {
    "ativa": true,
    "data_inicio": "...",
    "tier": "standard",
    "contato_cliente": "...",
    "ciclo_relatorio_dias": 30,
    "ciclo_monitor_dias": 7,
    "ciclo_revisao_backlog_dias": 30,
    "ciclo_radar_tecnologico_dias": 180,
    "ciclo_fmo_reavaliacao_dias": 365
  }
}
```

### Tiers de SLA disponíveis

| Tier       | Bug CRÍTICO | Bug ALTO | Bug MÉDIO | Relatório cliente | Revisão backlog |
|------------|-------------|----------|-----------|-------------------|-----------------|
| essencial  | 48h         | 5 dias   | 15 dias   | trimestral        | semestral       |
| standard   | 24h         | 72h      | 10 dias   | mensal            | mensal          |
| premium    | 4h          | 24h      | 5 dias    | quinzenal         | quinzenal       |

---

## 3. Ciclos de Sustentação

### Ciclo Semanal — Monitoramento de Saúde
* Invocar `productionMonitorSkill.md`
* Se anomalia detectada: classificar conforme tier de SLA → abrir MS de bug_fix via `backlogTriageSkill.md`
* Registrar resultado em `05_Monitoramento/health_report_[YYYYMMDD].json`

### Ciclo Mensal — Relatório + Revisão de Backlog
* Invocar `clientProgressSkill.md` → gerar relatório executivo do período
* Revisar `payload_index.json → backlog_micro_specs` (pendentes):
  * Identificar MSs bloqueadas por dependência (resolver ou re-priorizar)
  * Identificar MSs que perderam relevância (arquivar)
  * Verificar se novas demandas do cliente foram triadas e inseridas
* Emitir sumário de backlog para o cliente junto ao relatório mensal

### Ciclo Semestral — Radar Tecnológico
* Ler `payload_index.json → arquitetura_e_padroes` (stack atual)
* Para cada dependência principal: verificar versão atual vs. última estável
* Verificar CVEs conhecidos nas dependências (usando `audit` da linguagem/ecossistema)
* Verificar se a stack escolhida no ADR ainda é a recomendação do mercado para o perfil do projeto
* Produzir relatório de radar em `docs/ThronusSpec/01_Planejamento/technology_radar_[ANO_SEM].md`:
  ```
  ADOTAR:   [tecnologias que devem ser incorporadas]
  AVALIAR:  [tecnologias em observação]
  MANTER:   [tecnologias estáveis, sem ação necessária]
  MIGRAR:   [tecnologias com necessidade de atualização planejada]
  ```

### Ciclo Anual — Reavaliação FMO + Expansão
* Invocar `fmoToDiscoveryBridgeSkill.md` com novo assessment do cliente:
  * Quais dimensões evoluíram? (Processos, Dados, Governança, Qualificação, Receptividade)
  * O produto entregue contribuiu para a evolução? Quanto?
* Comparar nível atual vs. nível na época do diagnóstico inicial
* Produzir relatório de evolução de maturidade em `05_Monitoramento/fmo_evolucao_[ANO].md`
* Se nova etapa do portfólio Thronus for adequada (ex: o cliente avançou de Etapa 1 para Etapa 3):
  * Gerar proposta de expansão via `proposalGeneratorSkill.md`
  * Registrar oportunidade no CRM (se integrado)

---

## 4. Controle de SLA

Para cada MS de bug_fix aberta durante a sustentação:
* Registrar `criado_em` no `payload_archive` da MS
* Calcular prazo de resolução conforme tier e prioridade
* Se prazo em risco (>80% consumido sem GREEN): emitir alerta automático
* Ao fechar: registrar `tempo_resolucao` para análise histórica de SLA cumprimento

---

## 5. Saída Esperada no Terminal

### Ao ativar
```
[TCA_SUSTENTACAO_ATIVADA] FASE DE SUSTENTAÇÃO INICIADA
  Produto         : [nome]
  Tier SLA        : [tier]
  Próximo monitor : [data]
  Próximo relatório: [data]
  Próximo radar   : [data]
  Reavaliação FMO : [data]
```

### Ciclo mensal
```
[TCA_SUSTENTACAO_CICLO_MENSAL]
  Monitor         : SAUDÁVEL (0 anomalias) | ATENÇÃO ([N] anomalias → MS-NNN criada)
  Relatório       : gerado e enviado ao cliente
  Backlog         : [N] MSs pendentes | [N] re-priorizadas | [N] arquivadas
```
