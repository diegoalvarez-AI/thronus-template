# Skill: gitCommitGuardSkill (Metodologia TCA v2)

## 1. Objetivo Operacional
Auditar o ambiente de staging antes do commit, construir a mensagem Conventional Commits e executar o commit com lista explícita de arquivos. Garante que nenhum arquivo fora do escopo da spec entre no repositório.

---

## 2. Protocolo de Auditoria Final

### Passo 2.1: Snapshot-Diff Gate (Última Barreira)
* Executar `git diff --name-only HEAD` e `git status --short`.
* Comparar a lista de arquivos modificados/criados contra a seção "Arquivos a criar/modificar" em `context/activeContext.md`.
* **Se houver arquivos inesperados:** listar explicitamente, aguardar instrução humana. Se confirmado como erro → `[ABORT]` sem commit.
* **Se a lista bater exatamente:** prosseguir.

### Passo 2.2: Verificação Sanitária
* Confirmar que arquivos temporários, logs de debug, rascunhos de contexto ou credenciais não estão na área de staging.
* Verificar que a suíte de testes está 100% verde (resultado do estado EDGE ainda válido).
* Executar o linter do projeto (ruff / eslint / golangci-lint / etc.) — nenhum erro novo permitido.

### Passo 2.3: Construção da Mensagem de Commit
Formato Conventional Commits com MS-ID obrigatório:

```
<type>(<scope>): <descrição imperativa e concisa> [MS-NNN]
```

**Types permitidos:**
- `feat` — nova funcionalidade
- `fix` — correção de bug
- `refactor` — melhoria sem mudança de comportamento
- `test` — adição ou correção de testes apenas
- `chore` — configuração, dependências, CI/CD
- `docs` — documentação

**Scope:** nome do módulo, serviço ou domínio afetado.

**Exemplos válidos:**
```
feat(importacao): implementa persistência de respostas de alunos [MS-001]
fix(ranking): corrige cálculo de desempate por frequência [MS-023]
refactor(auth): extrai lógica de permissão para Port interface [MS-015]
```

### Passo 2.4: Execução do Commit
```bash
git add <arquivo1> <arquivo2> ...   # lista explícita — nunca git add .
git commit -m "<mensagem gerada>"
```

A lista de arquivos no `git add` deve ser idêntica à seção "Arquivos a criar/modificar" de `activeContext.md`. Qualquer arquivo adicional requer confirmação humana antes de ser incluído.

---

## 3. Saída Esperada no Terminal

```
[TCA_COMMIT_GUARD] COMMIT EXECUTADO
  Arquivos commitados : [lista]
  Mensagem            : <tipo>(<escopo>): <descrição> [MS-NNN]
  Diff check          : LIMPO — nenhum arquivo inesperado
  Status              : STATUS_PRONTO_PARA_COMMIT → COMMITADO ✓
```
