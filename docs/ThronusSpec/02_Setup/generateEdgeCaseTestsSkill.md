# Skill: generateEdgeCaseTestsSkill (Metodologia TCA)

## 1. Objetivo Operacional
Garantir a máxima resiliência e blindagem de segurança do software em desenvolvimento. Este skill atua na fase de escrita de testes (Ciclo RED do TDD), forçando a IA a gerar cenários de teste automatizados focados estritamente em limites, falhas, inputs corrompidos e ataques de estouro de escopo [source: 1].

## 2. Protocolo de Geração de Casos Extremos (Passo a Passo Obrigatório)
O motor de IA deve abrir e analisar os requisitos contidos em `context/activeContext.md` e gerar cenários de teste unitários ou de integração para as seguintes categorias [source: 1]:

### Passo 2.1: Estouro de Limites de Dados e Tipagem
* **Valores Fora de Escopo:** Gerar testes injetando dados numéricos além dos limites permitidos (ex: notas negativas, pontuações acima do teto estipulado, valores vazios) [source: 1, 0.1.4].
* **Injeção de Strings Gigantes:** Testar o comportamento do modelo ao receber payloads contendo textos imensos ou caracteres especiais inválidos em campos delimitados.

### Passo 2.2: Payload Malformado, Nulos e Vazios
* **Contratos Corrompidos:** Injetar estruturas JSON ou dicionários de entrada com chaves ausentes, chaves renomeadas incorretamente ou com valores nulos em campos obrigatórios, garantindo que o sistema capture o erro sem gerar falhas catastróficas (Internal Server Error) [source: 1].

### Passo 2.3: Idempotência sob Concorrência Crítica
* **Disparos Simultâneos:** Gerar cenários de testes que simulem requisições duplicadas enviadas exatamente no mesmo milissegundo com chaves de identificação idênticas, validando se a restrição única do Postgres bloqueia a persistência duplicada com sucesso [source: 1].

### Passo 2.4: Quebra de Permissões e Segurança
* **Invasão de Contexto:** Tentar disparar a execução de serviços ou endpoints utilizando usuários autenticados mas que não possuem os perfis de acesso adequados listados na matriz do `projeto_payload.json`, garantindo o bloqueio por exceção de segurança [source: 1].

## 3. Saída Esperada
* Escrever e acoplar os blocos de código de testes automatizados diretamente dentro do arquivo de testes da funcionalidade corrente [source: 1].
* Emitir o status `STATUS_EDGE_CASES_PRONTOS` no terminal para dar sequência ao ciclo.
