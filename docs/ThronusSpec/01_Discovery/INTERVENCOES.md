# Catálogo de Intervenções

> Cada oportunidade da fase O recebe uma **natureza** na fase N. A natureza determina o
> artefato mínimo, a unidade de dimensionamento, o critério de sucesso e o destino.
>
> Ordem ESIA obrigatória: eliminar → simplificar/padronizar → integrar → automatizar →
> assistir com IA → construir. Capacitar é transversal. Salto na ordem exige justificativa
> escrita no Programa.

---

## 1. Quadro-resumo

| # | Natureza | Etapa | Unidade de dimensionamento | Vai para a TCA? |
|---|---|---|---|---|
| 1 | Eliminar atividade | — | atividades removidas | não |
| 2 | Padronizar procedimento | — | procedimentos escritos | não |
| 3 | Capacitar, mentorar, aculturar | — | turmas × comportamentos-alvo | não |
| 4 | Integrar sistemas existentes | 1 | pares origem-destino × campos | **sim**, quando há código |
| 5 | Automatizar rotina | 1 | rotinas × passos × pontos de decisão | **sim** |
| 6 | Assistente ou agente simples | 1 | intenções × canais | **sim** |
| 7 | Agente com autonomia | 1 | intenções × ferramentas × ações irreversíveis | **sim** |
| 8 | Orquestração | 1–2 | fluxos × sistemas coordenados | **sim** |
| 9 | Painel e indicador | 2 | indicadores × fontes | **sim** |
| 10 | API como produto | 3 | processos funcionais (COSMIC) | **sim** |
| 11 | Sistema sob medida | 3 | processos funcionais (COSMIC) | **sim** |

O que vai para a TCA usa o `DOCUMENTO_DE_ENTRADA.md`, com perfil, tipo e nível de garantia.
O que não vai tem o seu artefato mínimo aqui, e é entregue e verificado do mesmo modo: com
critério de aceite e evidência.

---

## 2. Artefato mínimo por natureza

### 1 · Eliminar atividade
**Quando cabe:** a atividade não agrega valor ao cliente do processo, ou existe só para
compensar falha de outra etapa.
**Artefato:** atividade nomeada · por que existe hoje · o que se perde ao removê-la · quem
autoriza a remoção · o que passa a acontecer no lugar.
**Sucesso:** o tempo de atravessamento cai e nenhuma saída do processo se perde.

### 2 · Padronizar procedimento
**Quando cabe:** a atividade é necessária, é feita de formas diferentes por pessoas diferentes,
e a variação causa erro ou retrabalho.
**Artefato:** procedimento escrito em linguagem do cliente · dono do procedimento · gatilho ·
passos · exceções e o que fazer nelas · indicador de conformidade.
**Sucesso:** a variação entre executores cai e o retrabalho medido na fase O cai.
**Regra:** padronizar antes de automatizar. Automatizar variação é multiplicar variação.

### 3 · Capacitar, mentorar, aculturar
**Quando cabe:** Qualificação ou Receptividade baixas no FMO, ou intervenção que a equipe
precisará operar sozinha.
**Artefato:** **comportamento-alvo** — o que a pessoa passará a fazer diferente, não o que vai
saber · público e pré-requisito · formato e carga · quem conduz · avaliação no **nível 3 de
Kirkpatrick**, observada no trabalho e não em formulário de reação.
**Sequência de mudança (ADKAR):** consciência do problema e desejo de mudar **antes** de
conhecimento e habilidade; reforço declarado, com dono, depois da entrega.
**Sucesso:** o comportamento-alvo é observado no campo após o prazo declarado.

### 4 · Integrar sistemas existentes
**Quando cabe:** a informação já existe em um sistema e é redigitada em outro.
**Artefato:** par origem-destino · campos e o mapeamento entre eles · gatilho e frequência ·
o que fazer quando a origem está indisponível · como se evita duplicar efeito ao reprocessar ·
quem responde por cada lado.
**Sucesso:** a redigitação medida na fase O vai a zero e nenhum registro se perde.

### 5 · Automatizar rotina
**Quando cabe:** a rotina é estável, padronizada, e não exige julgamento.
**Artefato:** gatilho · passos · pontos de decisão e a regra de cada um · o que fazer em cada
falha · o que **nunca** é feito sem confirmação humana · trilha de execução · dono da operação.
**Sucesso:** a rotina roda sem intervenção na taxa declarada, e a exceção é visível a alguém.

### 6 · Assistente ou agente simples
**Quando cabe:** há atendimento, triagem ou consulta repetitiva, com resposta derivável de
base conhecida.
**Artefato:** intenções atendidas · o que ele **não faz** · canais · base de conhecimento e seu
dono · **regra de escalonamento para humano** · tom e vocabulário · teto de custo por conversa
e por dia · o que se registra de cada interação.
**Sucesso:** a taxa de resolução sem humano declarada é atingida, sem queda na satisfação.
**Regra:** escalonamento para humano é obrigatório e nunca é silencioso.

### 7 · Agente com autonomia
**Quando cabe:** o agente executa ação em sistema, não apenas responde.
**Artefato:** tudo de 6, mais — ferramentas que ele pode acionar · **ações irreversíveis, que
exigem confirmação humana explícita** · limite de alçada · o que acontece quando ele erra ·
como se audita o que ele fez.
**Sucesso:** nenhuma ação irreversível executada sem confirmação, e a trilha permite reconstituir
qualquer decisão.

### 8 · Orquestração
**Quando cabe:** vários sistemas, automações ou agentes precisam agir em sequência ou em
paralelo, com estado compartilhado.
**Artefato:** fluxo · sistemas coordenados · estado e onde ele vive · o que acontece quando um
passo falha no meio · como se retoma sem repetir efeito · quem observa o fluxo.
**Sucesso:** o fluxo completa na taxa declarada e a falha parcial é recuperável.

### 9 · Painel e indicador
**Quando cabe:** existe decisão recorrente tomada sem dado.
**Artefato:** **a decisão que o painel sustenta e quem a toma** · indicador · fórmula · fonte ·
frequência de atualização · o que significa estar fora da faixa · quem age quando está.
**Sucesso:** a decisão passa a ser tomada com o indicador, verificado com o dono da decisão.
**Regra:** painel sem decisão declarada não se constrói. É a forma mais comum de entrega que
ninguém usa.

### 10 · API como produto
**Artefato:** `DOCUMENTO_DE_ENTRADA.md` completo, com tipo `api` — contrato versionado,
política de depreciação, limite por consumidor.
**Unidade:** processos funcionais em COSMIC.

### 11 · Sistema sob medida
**Artefato:** `DOCUMENTO_DE_ENTRADA.md` completo, com tipo `saas` ou `sistema`.
**Unidade:** processos funcionais em COSMIC.

---

## 3. Regras que valem para todas

- **Toda intervenção tem dono do lado do cliente.** Sem dono, não entra no programa.
- **Toda intervenção tem critério de sucesso verificável**, ligado ao baseline da fase O.
- **Toda intervenção declara o que acontece se não for feita** — é o que sustenta a prioridade.
- **Intervenção que a equipe não sabe operar carrega item de capacitação**, ou não se entrega.
- **Nenhuma intervenção de natureza 4 a 11 se aprova com a natureza anterior pendente** sem
  justificativa escrita. É a ordem ESIA, e é o que impede automatizar o caos.
