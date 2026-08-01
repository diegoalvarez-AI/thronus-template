# Skill: deploySkill (Metodologia TCA v2)

## 1. Objetivo Operacional
Executar o deploy automático da entrega pós-commit, verificar a saúde do ambiente após o deploy e registrar o resultado no payload. Agnóstico de plataforma: detecta o padrão de infra do projeto via `payload_index.json → arquitetura_e_padroes.infra` e executa o procedimento adequado.

**Ativação:** Invocado automaticamente após `[ESTADO_COMMIT]` quando `estado_da_trilha.cd_ativo = true`. Em projetos sem CD configurado, emite aviso e encerra sem erro.

---

## 2. Protocolo de Deploy

### Passo 2.1: Verificar CD Configurado
* Ler `payload_index.json → estado_da_trilha.cd_ativo`.
* Se `false` ou campo ausente: emitir `STATUS_CD_NAO_CONFIGURADO` e encerrar. O deploy manual permanece responsabilidade do operador.

### Passo 2.2: Detectar Padrão de Infra
Ler `payload_index.json → arquitetura_e_padroes.infra` e selecionar o procedimento:

| Padrão infra                        | Procedimento                                      |
|-------------------------------------|---------------------------------------------------|
| `docker-compose-vps`                | SSH → `git pull` + `docker compose up --build -d`|
| `github-pages` / `vercel` / `netlify` | Push para branch de deploy (já é o trigger)     |
| `railway` / `render` / `fly.io`     | Deploy via CLI da plataforma                      |
| `kubernetes`                        | `kubectl set image` ou `helm upgrade`             |
| `serverless` (AWS Lambda / CF)      | `serverless deploy` ou `aws lambda update`        |
| custom                              | Executar `deploy_index.json → comando_deploy`     |

### Passo 2.3: Executar Deploy

#### Para `docker-compose-vps` (padrão mais comum em projetos standard):
```bash
# Via GitHub Actions (variáveis em secrets do repositório):
# DEPLOY_HOST, DEPLOY_USER, DEPLOY_SSH_KEY, DEPLOY_PATH

ssh $DEPLOY_USER@$DEPLOY_HOST << 'EOF'
  set -e
  cd $DEPLOY_PATH
  git pull origin main
  docker compose up --build -d
  sleep 10
  curl -sf http://localhost/health/ > /dev/null
EOF
```

O arquivo `.github/workflows/ci.yml` deve conter um job `deploy` separado do job `test`, executado apenas em push para `main`/`master` após o job `test` passar.

### Passo 2.4: Verificação Pós-Deploy (Health Check)
* Aguardar 10–30s para containers subirem.
* Executar requisição GET ao endpoint `/health/` (ou equivalente do projeto).
* Critério de sucesso: HTTP 200 com `{"status": "ok"}`.
* Critério de falha: timeout, HTTP ≠ 200, ou `{"status": "degraded"}`.

### Passo 2.5: Tratamento de Falha de Deploy
Em caso de falha no health check:
1. Capturar logs do container (`docker compose logs web --tail=100`).
2. Registrar falha em `05_Monitoramento/deploy_log.json` com timestamp, commit hash e logs.
3. **Não reverter automaticamente o commit** — o código passou em CI; o problema é de ambiente.
4. Emitir `STATUS_DEPLOY_FALHOU` com diagnóstico e aguardar intervenção humana.
5. Invocar `productionMonitorSkill.md` para coletar contexto adicional.

### Passo 2.6: Atualizar Payload Pós-Deploy Bem-Sucedido
Atualizar `payload_index.json → estado_da_trilha`:
```json
{
  "ultimo_deploy": {
    "ms_id": "MS-NNN",
    "commit": "<sha>",
    "timestamp": "<ISO8601>",
    "ambiente": "production",
    "status": "ok"
  }
}
```

---

## 3. Configuração Mínima no Projeto

Para ativar o CD, o projeto precisa de:

1. `payload_index.json → estado_da_trilha.cd_ativo: true`
2. `payload_index.json → arquitetura_e_padroes.infra: "docker-compose-vps"` (ou padrão adequado)
3. Endpoint `/health/` respondendo `{"status": "ok"}` em produção
4. Job `deploy` configurado no pipeline CI (`.github/workflows/ci.yml` ou equivalente)
5. Secrets de deploy configurados no repositório (nunca no código)

---

## 4. Saída Esperada no Terminal

```
[TCA_DEPLOY_SUCCESS] DEPLOY EXECUTADO E VERIFICADO
  MS deployada    : MS-NNN
  Ambiente        : production
  Health check    : OK (HTTP 200)
  Tempo total     : ~Ns
  Status          : PRODUÇÃO_ATUALIZADA ✓
```

```
[TCA_DEPLOY_FALHOU] INTERVENÇÃO REQUERIDA
  MS alvo         : MS-NNN
  Falha em        : health_check | container_startup | ssh_connection
  Logs coletados  : 05_Monitoramento/deploy_log.json
  Ação sugerida   : verificar logs + rollback de container se necessário
```
