# Skill: productionMonitorSkill (Metodologia TCA v2)

## 1. Objetivo Operacional
Executar varredura proativa de saúde em produção: verificar infraestrutura, integridade de dados de negócio e SLAs operacionais. Quando detectar anomalia, criar automaticamente uma entrada de triagem via `backlogTriageSkill.md` para que a falha seja tratada no próximo ciclo TDD.

**Ativação:** Invocado após `[ESTADO_DEPLOY]` (verificação pós-deploy) e periodicamente via cron job / comando de manutenção. Também pode ser invocado manualmente: "Execute productionMonitorSkill."

---

## 2. Protocolo de Monitoramento

### Passo 2.1: Saúde de Infraestrutura
* GET `/health/` (ou endpoint equivalente do projeto).
* Critério: HTTP 200 + `{"status": "ok", "db": "ok"}`.
* Se `"db": "error"`: crítico — invocar `backlogTriageSkill` com prioridade CRÍTICO imediatamente.
* Se timeout de rede: verificar se containers estão em execução; registrar em `deploy_log.json`.

### Passo 2.2: Integridade de Dados de Negócio
Ler `payload_index.json → modelos_e_tabelas_detectados` para identificar as entidades críticas do projeto.
Para cada entidade com `criticidade: "alta"`:

* Verificar registros em estados de transição há mais de `sla_horas` horas (configurável por modelo).
* Verificar registros órfãos (FK nula em campo obrigatório).
* Verificar invariantes declaradas no `payload_archive` (ex: append-only, unicidade).
* Registrar contagem de anomalias por categoria.

Exemplo genérico de verificação (adaptar à stack do projeto):
```
# pseudo-código independente de tecnologia
for entidade in entidades_criticas:
    travados = entidade.filter(status=TRANSICAO, atualizado_há > sla_horas)
    if travados.count() > 0:
        anomalias.append(("SLA_VIOLADO", entidade.nome, travados.count()))
```

### Passo 2.3: Revisão de Logs de Erro
* Verificar logs estruturados das últimas N horas (via Sentry API, CloudWatch, Papertrail, stdout do container — conforme stack).
* Agrupar erros por tipo (5xx, exceções não tratadas, validação falha).
* Se taxa de erros 5xx > threshold configurado: classificar como CRÍTICO.
* Se novos tipos de erro (não vistos nas últimas 24h): classificar como ALTO.

### Passo 2.4: Relatório de Saúde
Gerar relatório em `05_Monitoramento/health_report_<YYYYMMDD>.json`:
```json
{
  "timestamp": "<ISO8601>",
  "infra": { "status": "ok|degraded|down", "latencia_ms": 0 },
  "dados": {
    "anomalias": [],
    "entidades_verificadas": 0
  },
  "logs": {
    "erros_5xx": 0,
    "novos_tipos": []
  },
  "status_geral": "SAUDAVEL|ATENÇÃO|CRITICO"
}
```

### Passo 2.5: Criação Automática de Triagem
Para cada anomalia detectada:
* Construir texto de demanda descritivo: `"[MONITOR] <entidade>: <anomalia> — <contagem> registros afetados desde <timestamp>"`.
* Invocar `backlogTriageSkill.md` com o texto gerado.
* A triagem classifica como `bug_fix` com prioridade derivada da severidade.

---

## 3. Configuração no Projeto

Adicionar ao `payload_index.json → modelos_e_tabelas_detectados` o campo de monitoramento:
```json
{
  "nome": "LoteImportacao",
  "criticidade": "alta",
  "sla_horas": 24,
  "estado_transicao": "PROCESSANDO",
  "invariante": "status não pode permanecer em PROCESSANDO por mais de sla_horas"
}
```

Adicionar ao `payload_index.json → estado_da_trilha`:
```json
{
  "monitor_ativo": true,
  "monitor_threshold_5xx_por_hora": 5,
  "monitor_janela_logs_horas": 24
}
```

---

## 4. Integração com Stack

O skill invoca o **comando de monitoramento nativo do projeto** (se existir), não acessa a infraestrutura diretamente:

| Stack               | Comando                                          |
|---------------------|--------------------------------------------------|
| Django              | `python manage.py monitorar_saude`               |
| FastAPI + Alembic   | `python -m scripts.health_check`                 |
| Node.js + Prisma    | `node scripts/health-check.js`                   |
| Rails               | `rails health:check`                             |
| Custom              | `payload_index.json → comandos.monitor`          |

O comando deve retornar exit code 0 (saudável) ou não-zero (anomalia), e imprimir JSON de relatório em stdout para que o skill consuma.

---

## 5. Saída Esperada no Terminal

```
[TCA_MONITOR_OK] PRODUÇÃO SAUDÁVEL
  Infra           : ok (latência 42ms)
  Dados negócio   : 0 anomalias em 8 entidades
  Logs (24h)      : 0 erros 5xx, 0 novos tipos de erro
  Relatório       : 05_Monitoramento/health_report_20260801.json
```

```
[TCA_MONITOR_ATENÇÃO] ANOMALIAS DETECTADAS — TRIAGEM CRIADA
  Anomalias       : 3 LoteImportacao travados em PROCESSANDO há >24h
  Prioridade      : ALTO
  Triage criada   : MS-NNN adicionada ao backlog
  Relatório       : 05_Monitoramento/health_report_20260801.json
```
