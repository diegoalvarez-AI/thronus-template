# Skill: clientProgressSkill (Metodologia TCA v2 — Visibilidade para o Cliente)

## 1. Objetivo Operacional
Gerar um relatório executivo de progresso do projeto em linguagem não-técnica, entregável diretamente ao cliente sem intermediação de reunião. Transforma os artefatos internos do TCA (payload_archive, logs de deploy, coverage reports) em evidência de valor tangível e auditável.

**Ativação:** Invocado automaticamente em:
- Conclusão de qualquer gate intermediário (GATE_MVP, GATE_RELEASE_N)
- Encerramento de ciclo de manutenção mensal (sustentacaoSkill)
- Solicitação manual: "Gere relatório de progresso para o cliente"

---

## 2. Protocolo de Geração

### Passo 2.1: Coleta de Métricas do Ciclo
Ler os seguintes artefatos:
* `payload_index.json → estado_da_trilha` — MSs concluídas, ativas e pendentes
* `payload_archive/*.json` — contratos das MSs entregues desde o último relatório
* `05_Monitoramento/performance_logs.json` — cobertura, velocidade, deploys
* `05_Monitoramento/deploy_log.json` — histórico de deploys e incidentes
* `05_Monitoramento/health_report_*.json` — saúde pós-deploy

### Passo 2.2: Estrutura do Relatório Executivo

O relatório deve ser escrito em **linguagem empresarial**, sem jargão técnico.
Cada MS concluída é descrita pelo resultado de negócio que entrega, não pelo código que implementa.

```markdown
# Relatório de Progresso — [Nome do Projeto]
**Período:** [data_inicio] a [data_fim]
**Preparado por:** Thronus Digital

---

## O que foi entregue neste ciclo

| Funcionalidade                        | O que resolve                              | Status |
|---------------------------------------|--------------------------------------------|--------|
| [nome_ms em linguagem de usuário]     | [descrição do ganho de negócio]            | ✓      |

## Indicadores de qualidade

| Indicador                    | Valor         | Referência      |
|------------------------------|---------------|-----------------|
| Funcionalidades com cobertura de testes | [N]% | Meta: [min]% |
| Deploys realizados           | [N]           | —               |
| Incidentes em produção       | [N]           | Meta: 0         |
| Tempo médio de entrega por funcionalidade | [Xh] | Estimado: [Yh] |

## Saúde do sistema

[Status geral: SAUDÁVEL / ATENÇÃO / CRÍTICO]
[Últimas verificações: [datas]]

## Próximas entregas previstas

1. [nome_ms em linguagem de usuário] — [semana estimada]
2. [nome_ms em linguagem de usuário] — [semana estimada]
3. [nome_ms em linguagem de usuário] — [semana estimada]

## Situação geral do projeto

[Percentual de conclusão: X%]
[Status: NO PRAZO / ATENÇÃO / ATRASADO]
[Observação: ...]

---
*Relatório gerado automaticamente a partir dos artefatos de governança TCA.*
*Para dúvidas, entre em contato com [contato].*
```

### Passo 2.3: Conversão de Nomenclatura Técnica → Linguagem de Negócio
O agente aplica as seguintes regras de tradução ao descrever cada MS:

| Nome técnico (MS)                          | Linguagem para o cliente                                    |
|--------------------------------------------|-------------------------------------------------------------|
| `bloqueio por prazo de impugnação`         | `Proteção automática contra homologação fora do prazo legal`|
| `Port/Adapter para integração SIGRES`      | `Conexão automática com sistema federal de frequências`     |
| `exportação PDF/XLSX`                      | `Relatório exportável por escola em PDF e planilha`         |
| `edge case: validação de nulos`            | *(não aparece no relatório do cliente — é detalhe interno)* |

### Passo 2.4: Geração de Arquivo e Entrega
* Gravar em `05_Monitoramento/relatorio_cliente_[YYYYMM].md`
* Se integração de e-mail configurada: enviar ao contato do cliente registrado em `payload_index.json → cliente.contato_relatorio`
* Se integração de PDF configurada: gerar versão PDF com identidade visual da Thronus

---

## 3. Saída Esperada no Terminal

```
[TCA_CLIENT_PROGRESS_GERADO] RELATÓRIO EXECUTIVO PRONTO
  Período coberto  : [data] a [data]
  MSs reportadas   : [N] concluídas / [N] em andamento / [N] pendentes
  Cobertura atual  : [N]%
  Incidentes       : [N]
  Arquivo gerado   : 05_Monitoramento/relatorio_cliente_[YYYYMM].md
  Entrega          : [email enviado | disponível para download | geração manual]
```
