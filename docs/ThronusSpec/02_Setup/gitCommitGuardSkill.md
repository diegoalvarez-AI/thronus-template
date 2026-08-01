# Skill: gitCommitGuardSkill (Metodologia TCA)

## 1. Objetivo Operacional
Auditar a integridade técnica de toda a entrega gerada no ciclo antes que o commit seja consolidado no Git. Garante que nenhum lixo de contexto seja enviado ao repositório e padroniza a mensagem do Git utilizando a convenção corporativa para garantir o pleno funcionamento das ferramentas de integração contínua (CI/CD) [source: 1].

## 2. Protocolo de Auditoria Final (Passo a Passo Obrigatório)

### Passo 2.1: Verificação Sanitária do Ambiente de Código
* A IA deve inspecionar a área de staging do Git (`git status`) para garantir que apenas os arquivos produtivos e de testes afetados pela especificação estejam listados.
* Deve verificar se arquivos temporários, logs locais de erros ou rascunhos de contexto foram removidos do escopo de envio.
* Deve acionar o linter e o comando de execução de testes do ecossistema, certificando-se de que a suíte completa permanece verde e sem falhas ocultas [source: 1].

### Passo 2.2: Construção Determinística da Mensagem de Commit
A IA deve formular a mensagem do commit seguindo estritamente a especificação corporativa de *Conventional Commits*, amarrando o ID da Micro Spec correspondente. O formato deve seguir rigorosamente a regra abaixo [source: 1]:

`type(scope): short description [MS-XXX]`

* **Types Permitidos:** `feat` (funcionalidade nova), `fix` (correção de bug), `refactor` (melhoria de código existente sem alterar comportamento) [source: 1].
* **Scope:** O nome do subcomponente ou módulo sendo alterado [source: 1].
* **Description:** Verbo no presente com descrição direta e concisa da alteração [source: 1].
* **ID:** O identificador exato da Micro Spec extraído de dentro da RAM [source: 1].

*Exemplo Válido:* `feat(importacao): implementa persistencia de respostas de alunos [MS-001]` [source: 1]

## 3. Saída Esperada no Terminal
* Exibir o sumário técnico de validação do código.
* Entregar o bloco de texto exato da mensagem de commit formatada [source: 1].
* Emitir o status `STATUS_PRONTO_PARA_COMMIT`.
