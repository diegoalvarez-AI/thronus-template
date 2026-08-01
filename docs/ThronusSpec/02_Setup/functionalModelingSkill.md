# Skill: functionalModelingSkill (Metodologia TCA — Fase Pré-Código)

## 1. Objetivo Operacional
Estruturar o domínio funcional e de negócio do projeto em termos que sejam independentes de tecnologia, mas suficientemente precisos para guiar decisões de arquitetura e gerar o backlog de Micro Specs. A linguagem é de negócio, não de código.

**Ativação:** Obrigatória em Standard e Enterprise. Recomendada em Micro. Ignorada em Nano.

**Insumo:** `docs/ThronusSpec/01_Planejamento/discovery.md` (produzido por `discoverySkill`).

---

## 2. Protocolo de Modelagem Funcional

### Passo 2.1: Glossário do Domínio (Linguagem Ubíqua)
Definir os termos que terão significado preciso e compartilhado em todo o projeto.
Formato: `**Termo**: definição de negócio. Sinônimos proibidos: [lista].`

Regra: se duas pessoas na equipe usam termos diferentes para a mesma coisa, isso vira uma entrada do glossário com um termo canônico escolhido.

### Passo 2.2: Modelo de Entidades de Domínio
Mapear as entidades de negócio e seus relacionamentos — sem mencionar banco de dados, ORM ou tecnologia:
```
ENTIDADE: [Nome]
  Atributos essenciais: [lista dos campos que identificam ou diferenciam]
  Regras de negócio internas: [o que é sempre verdadeiro sobre essa entidade]
  Relacionamentos: [com quais outras entidades se relaciona e como]
```

### Passo 2.3: Mapa de Casos de Uso
Para cada ator identificado na discovery, listar os casos de uso com critério de aceite:
```
UC-[NN]: [Verbo no infinitivo + Objeto]
  Ator principal: [quem]
  Pré-condição: [o que precisa ser verdade antes]
  Fluxo principal: [sequência numerada de passos]
  Exceções críticas: [o que pode dar errado e como o sistema responde]
  Critério de aceite: [frase verificável que prova que o UC está implementado]
```

### Passo 2.4: Inventário de Regras de Negócio
Numerar cada regra de negócio identificada:
```
RN-[NN]: [Descrição da regra]
  Origem: [cláusula contratual / edital / lei / decisão de produto]
  Escopo: [quais entidades/UCs são afetados]
  Exceções: [quando a regra não se aplica]
```

### Passo 2.5: Geração do Backlog de Micro Specs
A partir dos UCs e RNs, gerar o backlog ordenado de MSs:
- Cada MS deve entregar valor testável e demonstrável de forma isolada
- Estimativa de complexidade: P (≤1 dia) / M (2–3 dias) / G (1 semana) / GG (sprint)
- MSs GG devem ser decompostas em MSs menores antes de iniciar

Formato:
```
MS-[NNN]: [Nome descritivo]
  UC cobertos: [lista]
  RN cobertas: [lista]
  Complexidade: P / M / G
  Dependências: [MSs que devem estar prontas antes]
  Gate de aceite: [GATE_NNN_NOME]
```

### Passo 2.6: Diagrama de Fluxo de Dados (Narrativo)
Descrever em prosa como os dados fluem entre os atores e o sistema nas jornadas críticas identificadas na discovery. Não usar notação de banco ou código — usar frases de negócio.

---

## 3. Output Obrigatório
Escrever `docs/ThronusSpec/01_Planejamento/functional_model.md` com todas as seções.

Emitir `STATUS_FUNCTIONAL_CONCLUIDO` e transitar para `[ESTADO_ARCHITECTURE]`.
