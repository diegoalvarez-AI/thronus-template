# Skill: generateEdgeCaseTestsSkill (Metodologia TCA v2)

## 1. Objetivo Operacional
Injetar e validar cenários de estresse, limite e segurança após o estado GREEN. O skill opera sobre `context/activeContext.md` para derivar os casos extremos relevantes ao domínio e stack da MS ativa — independente de linguagem ou framework.

---

## 2. Protocolo de Geração de Casos Extremos

### Passo 2.1: Estouro de Limites e Tipagem
* **Valores fora de escopo:** Injetar dados numéricos além dos limites definidos nos critérios de aceite (negativos, acima do teto, zero onde não permitido).
* **Strings extremas:** Payloads com textos muito longos, caracteres especiais, unicode inesperado, ou strings vazias em campos obrigatórios.
* **Tipos errados:** Passar string onde se espera inteiro, null onde se espera lista, float onde se espera inteiro.

### Passo 2.2: Payload Malformado, Nulos e Ausentes
* **Chaves ausentes:** Estruturas de entrada (JSON, dict, objeto) com campos obrigatórios faltando.
* **Chaves extras:** Campos não previstos no contrato — verificar que são ignorados sem erro catastrófico.
* **Valores nulos em campos não-anuláveis:** Garantir que a camada de validação rejeita com mensagem clara, não com exceção genérica de infraestrutura.

### Passo 2.3: Idempotência e Concorrência
* **Requisições duplicadas:** Simular o mesmo comando/operação enviado duas vezes em sequência — o resultado deve ser idêntico ao de uma única execução (sem duplicatas de dados, sem erro na segunda chamada se idempotente por spec).
* **Conflito de constraint:** Se o domínio tem unicidade (email único, código único, etc.), verificar que a constraint bloqueia a duplicata com erro tratado, não com stack trace.

### Passo 2.4: Quebra de Permissão e Segurança
* **Acesso sem autenticação:** Endpoints ou serviços que exigem autenticação devem retornar 401/403 — não 500.
* **Escalada de privilégio:** Usuário com perfil de menor privilégio tentando executar operação reservada a perfil superior — verificar bloqueio explícito.
* **Injeção:** Se o serviço constrói queries ou comandos com input externo, verificar que inputs maliciosos não alteram a estrutura do comando (SQL injection, command injection, path traversal).

### Passo 2.5: Seleção de Casos por Relevância
* Não gerar todos os casos acima para toda MS. Ler `context/activeContext.md` e selecionar apenas as categorias aplicáveis ao domínio e risco da MS ativa.
* MSs que processam apenas dados internos (sem input externo) podem pular §2.4.
* MSs puramente de leitura podem pular §2.3.

---

## 3. Saída Esperada

* Escrever os casos EDGE no arquivo de testes da MS atual (`test_edge_ms<NNN>_<descricao>`).
* Executar a suíte completa — todos os testes EDGE e BDD devem passar.
* Emitir `STATUS_EDGE_CASES_PRONTOS` e transitar para `[ESTADO_COMMIT]`.
