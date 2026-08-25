# tca — a metodologia como artefato executável

A TCA é descrita em prosa nos skills de `docs/ThronusSpec/02_Setup/`. Este pacote é a
parte dela que **executa**: os portões que dependiam de disciplina passam a ser comandos
que falham sozinhos.

Existe por uma razão registrada: pelo ÂNCORA §2.6, fonte canônica precisa ser única para
o conteúdo que governa, versionada e verificável por resumo criptográfico. Metodologia
copiada para dentro de cada projeto não é nenhuma das três coisas — e markdown copiado
não executa, que é a razão de os portões serem declarados e inoperantes.

## Requisitos

Python 3.8+ e a biblioteca padrão. Nada mais. A TCA governa projetos de qualquer stack e
não pode impor runtime a nenhum deles.

## Instalação no projeto

```sh
git config core.hooksPath tca/hooks     # ativa o portão de commit
./tca/bin/tca verify-self               # confere a integridade do pacote
./tca/bin/tca verify                    # confere a coerência do estado
```

## Comandos

### `tca close-ms <MS-ID> [--titulo T] [--testes N] [--dry-run]`

Fecha o ciclo de uma Micro Spec em uma operação. É o remédio para o gap documental —
ciclo que termina sem archive, sem log e sem limpar o contexto.

**Entradas** — o comando lê:

| Arquivo | Uso |
|---|---|
| `context/activeContext.md` | contexto da MS ativa e o campo `**MS ativa:**` |
| `docs/ThronusSpec/03_Desenvolvimento/payload_index.json` | estado da trilha |
| `docs/ThronusSpec/05_Monitoramento/performance_logs.json` | histórico |

**Saídas** — o comando escreve:

| Arquivo | Efeito |
|---|---|
| `payload_archive/<msNNN>.json` | criado com o núcleo obrigatório e o contexto verbatim |
| `payload_index.json` | `ultima_micro_spec_concluida`, `micro_spec_ativa=null`, `_archive.keys` derivado do diretório |
| `performance_logs.json` | um registro por MS, sem duplicar |
| `context/activeContext.md` | reescrito vazio, preservando a fase |
| `tca_execution_log.jsonl` | evidência de que o comando executou |

**Propriedades garantidas:**

- **Idempotente.** Fechar MS já fechada é no-op — não reescreve o archive nem duplica o
  registro de log.
- **Conservador.** Só toca os campos que este contrato declara possuir. Qualquer outro
  campo do `payload_index.json` é preservado — inclusive os que um projeto tenha
  acrescentado por conta própria.
- **Não inventa.** Sem título derivável do contexto e sem `--titulo`, o comando **falha**
  em vez de inferir. Lacuna declarada, não preenchida.
- **Escrita atômica por arquivo** (tmp + `replace`). Não há transação entre os quatro
  arquivos; se a máquina cair no meio, `tca verify` detecta o estado parcial e uma nova
  execução completa o fechamento.

### `tca verify [--strict]`

Coerência dos artefatos de controle. Reprova quando:

- `AGENTS.md` está ausente, desatualizado ou foi editado à mão;
- `_archive.keys` diverge dos arquivos em disco;
- há MS ativa no `activeContext` sem `micro_spec_ativa` no índice, ou o inverso — ciclo
  aberto sem registro, ou fechado sem limpeza;
- `ultima_micro_spec_concluida` não tem archive correspondente;
- algum artefato de controle não é JSON válido.

Com `--strict`, archive fora do núcleo obrigatório também reprova. Sem a flag, vira aviso
— projetos existentes têm archives legados e o comando não deve travá-los antes da
triagem.

### `tca diff [--cached]`

**Snapshot-diff bidirecional.** Compara os arquivos tocados com a lista prevista em
`**Arquivos a criar/modificar:**` do `activeContext.md`, e reprova nos dois sentidos:

| Saída | Significado |
|---|---|
| `INESPERADO` | tocado sem estar previsto na spec |
| `FALTANTE` | **previsto na spec e não entregue** |

O segundo caso é o que passava sem ruído. O gate descrito nos skills procura arquivo
inesperado; arquivo previsto que não apareceu não gerava sinal — e é essa a assinatura da
entrega parcial. Foi o que deixou a deleção de uma rota ir a produção como se nunca
tivesse sido decidida.

Campo ausente é **lacuna, não aprovação**: sem lista prevista o comando falha em vez de
passar por omissão. Travessão significa "nenhum arquivo", que é diferente de não declarar.

Os artefatos que a própria TCA governa — `activeContext`, índice, archives, logs, lock,
configuração — **não contam**. Todo commit de fechamento os toca, e contá-los faria o
portão reprovar sempre até virar ruído que se aprende a ignorar. Eles são governados pelo
`verify`.

`--cached` compara só o que está em staging: é a forma usada pelo portão de commit.

### `tca trace [--write] [--strict] [--impacto ARQUIVO]`

**O índice de rastreabilidade.** Constrói `identificador → arquivo → Micro Spec` a partir
de marcadores em comentário e do histórico git. Marcador é texto, não recurso de runner —
a TCA não pode depender de `pytest.mark`, tag de vitest ou anotação de JUnit.

```
# @tca RF-014 UC-003
// @tca RF-031 RNF-007
```

`--impacto <arquivo>` responde, **antes** de escrever a primeira linha: quais testes
alcançam o arquivo, quais requisitos ele toca, quais Micro Specs o alteraram. Usa
`comandos.testes_relacionados` para o grafo de módulos; sem ele, cai no marcador do
próprio arquivo e avisa.

O mesmo grafo serve à análise de impacto e à seleção de teste. É a peça que ataca os dois
maiores custos medidos: a leitura exploratória e as idas e vindas de correção.

**Cobertura de requisito exige universo declarado.** Com `comandos.listar_requisitos` — um
comando que imprime um identificador por linha — o índice calcula quantos requisitos têm
teste e lista os que não têm; `--strict` reprova nesse caso. Sem o universo, a cobertura é
**lacuna declarada, nunca 100%**: o índice sabe o que está coberto, não o que falta.

O pacote `tca/` fica fora da varredura. Ele documenta a convenção, e os exemplos entrariam
no índice como se fossem cobertura real.

### `tca sev [ID | --listar | --validar]`

**Registro canônico de severidade.** Para cada violação revisável, o nível e a **origem da
regra** ficam fixados em `tca/severidades.json` — que entra no `CANON.sha256`, porque
alterá-lo muda o resultado que o método produz.

Existe porque severidade decidida no momento do portão é julgamento, e julgamento carrega
o viés de quem conduz a avaliação — que o ÂNCORA §2.4 quer restringir, e que é mais forte
quando quem avalia tem interesse na aprovação.

`--validar` confere a boa-formação e reporta quantas linhas têm detecção automática e
quantas dependem de revisor humano. É um número útil por si: mede o quanto do método já
executa sozinho.

### `tca gate [--de VERIF,...] [--achados ID,...] [--pendencia ID=Nome]`

Calcula o estado do portão sob **não compensação**, nos três estados do ÂNCORA:

| Estado | Quando |
|---|---|
| `ATENDIDO` | nenhum bloqueante, nenhuma pendência sem dono |
| `CONDICIONADO` | pendências residuais, **todas com responsável nomeado** |
| `NAO_ATENDIDO` | qualquer bloqueante, ou pendência sem responsável |

`--de diff,trace,selfcheck,doctor` executa as verificações e traduz o que elas encontram
em identificadores do registro — o portão deixa de depender de alguém converter código de
saída em achado à mão. `--achados` cobre o que ainda depende de revisor, e os dois somam.

`--classe fix|feat|tecnico` aplica as regras da classe: correção dispensa cobertura de
requisito e exige teste de regressão; nova capacidade admite a emenda como pendência
acompanhada; mudança técnica dispensa ambos. O tipo do Conventional Commit já dá a classe.

`--assinar Nome` confere contra `tca.signatarios.json` — autorização declarada antes,
ato registrado agora, com a referência do que foi aprovado. `--exigir-assinatura` reprova
portão sem signatário.

Três propriedades que, juntas, são a não compensação:

1. **Bloqueante não é neutralizado.** Desempenho em outro critério não compensa condição
   necessária.
2. **Pendência sem responsável bloqueia.** Sem dono não é pendência acompanhada — é achado
   não endereçado.
3. **Achado fora do registro é erro**, não julgamento na hora. Declarar a linha é decisão
   de método, tomada antes e por escrito.

### `tca selfcheck`

**A verificação está de pé?** Responde ao incidente em que um estágio de integração
contínua rodava sem banco: toda execução falhava, o estágio dependente nunca era
alcançado, e o desconhecimento durou dias porque nada perguntava se a própria verificação
executava.

Reprova quando:

- o projeto não declara `comandos.testes` — sem contrato não se afirma que a suíte roda;
- a contagem de testes **caiu** além da tolerância em relação à última medição desta
  máquina — o sinal de suíte que parou de executar;
- a última execução registrada da suíte terminou em erro.

A comparação é sempre contra medição do **mesmo ambiente**. Sem base local, avisa em vez
de reprovar — comparar máquinas diferentes seria pior que não comparar.

### `tca canon [--write]`

Integridade do **conteúdo metodológico** — o que, alterado, muda o resultado que o método
produz. Hoje cobre `docs/ThronusSpec/02_Setup/*.md` e `profiles/*.json`, declarados em
`tca/CANON.sha256`.

`--write` regenera o arquivo a partir do repositório; sem a flag, verifica. Dois
manifestos, dois propósitos: `MANIFEST.sha256` guarda o código do pacote, `CANON.sha256`
guarda a metodologia.

### `tca doctor [--strict]`

**O detector de inferência local.** Compara os arquivos de metodologia do projeto com o
canon declarado e classifica cada um:

| Saída | Significado |
|---|---|
| `DIVERGE` | arquivo existe e foi editado no projeto |
| `AUSENTE` | arquivo do canon não existe aqui |
| `EXTRA` | arquivo de metodologia não declarado no canon |
| `OVERRIDE` | divergência declarada em `tca-overrides.json` — decisão, não acidente |

Sem `--strict`, apenas relata e sai com zero: é o modo de migração, para o projeto poder
adotar o pacote antes de ter triado as divergências. Com `--strict`, divergência não
declarada reprova.

Um override exige `arquivo`, `motivo` e `responsavel` — papel genérico não satisfaz o
requisito de responsabilidade nomeada. Override incompleto é erro, não aviso:

```json
{
  "overrides": [
    {
      "arquivo": "docs/ThronusSpec/02_Setup/discoverySkill.md",
      "motivo": "domínio educacional exige levantamento de calendário letivo",
      "responsavel": "Diego Alvarez",
      "em": "2026-08-24"
    }
  ]
}
```

### `tca agents [--write]`

Gera o `AGENTS.md` a partir de duas fontes e verifica que ele está em dia:

| Fonte | Natureza |
|---|---|
| `tca/METODOLOGIA.md` | canônica, sem placeholders, coberta pelo `CANON.sha256` |
| `PROJETO.md` | específica do projeto, com placeholders, editável |

O `AGENTS.md` continua sendo **um arquivo só**, porque o padrão aberto não tem mecanismo
de include e um harness que não suporte importação precisa ler tudo em um lugar. A
concatenação é material, mas **verificada** — é isso que a distingue de uma cópia editada
à mão. Editar o `AGENTS.md` diretamente reprova em `tca agents` e em `tca verify`.

Para mudar a metodologia, edite `tca/METODOLOGIA.md` e rode `tca canon --write`. Para
mudar o projeto, edite `PROJETO.md`. Depois, `tca agents --write`.

### `tca lock [--write] [--origem URL] [--ref SHA]`

Fixa a **procedência da metodologia instalada** em `tca.lock.json`: origem, versão, ref e
— o campo que importa — o `sha256` do próprio `CANON.sha256`.

Sem isso há um buraco: quem edita um skill **e** roda `tca canon --write` deixa o `doctor`
verde, porque o canon guarda a metodologia e nada guardaria o canon. Com o lock, o
`doctor` detecta que o canon foi regenerado localmente e trata isso como divergência não
declarada.

`.thronus-template-version` e `tca.lock.json` não se sobrepõem: o primeiro guarda a
identidade do **projeto** (nome, cliente, perfil, starter) e é consumido pelo
`apply-starter.sh`; o segundo guarda a procedência da **metodologia**.

### `tca update [--apply]`

Confere se a metodologia instalada está atrás da origem declarada no lock, e opcionalmente
aplica a versão nova. A distribuição é por **tag git**: `tca update` lista as tags de
versão da origem e compara com o que o lock registra.

Sem `--apply`, só reporta e sai com 1 quando há atraso. Com `--apply`:

- **recusa** se houver divergência não declarada — atualizar sobrescreveria conteúdo
  metodológico, e perder edição local em silêncio é pior que não atualizar;
- **preserva** os arquivos com override declarado, listando cada um;
- reescreve o `tca.lock.json` com a versão, a ref e o novo hash do canon.

Depois de aplicar, rode `tca agents --write` (a metodologia mudou, o gerado precisa
acompanhar) e `tca doctor --strict`.

### `tca metrics [--repo D] [--desde REF] [--suite-segundos N] [--write]`

**Linha de base do processo, derivada do que já aconteceu.** Não muda nada no fluxo, não
pede dado novo e não instrumenta a execução: lê o histórico git e os archives.

Existe pelo requisito de ancoragem econômica do ÂNCORA — *benefício que não foi definido
antes não pode ser verificado depois*. Sem medir o processo antes de mudá-lo, "melhora a
produtividade" é a mesma declaração não verificável que o método critica.

| Indicador | Origem |
|---|---|
| `ms_entregues` | commits cujo assunto cita `MS-NNN` |
| `ms_com_archive_pct` | quantas dessas MS têm registro de archive — **o gap documental, quantificado** |
| `commits_por_ms_mediana` | git |
| `arquivos_por_ms_mediana` · `linhas_por_ms_mediana` | git — dimensionam se a Micro Spec é de fato micro |
| `duracao_ms_horas_mediana` | git, só sobre MS com mais de um commit |
| `lead_time_entre_ms_horas_mediana` | intervalo entre fechamentos — a cadência real |
| `correcoes_apos_entrega` | commits `fix` posteriores ao primeiro commit da MS — proxy de retrabalho |
| `testes_por_ms_mediana` | archives, **com a cobertura do campo declarada** |

**Cada valor declara a própria origem** — `derivado:git`, `derivado:archives` ou
`reportado` — e a cobertura quando o campo não existe em todo o histórico. É a exigência de
proveniência aplicada à própria medição: um número derivado de 8 de 41 archives não vale o
mesmo que um derivado de 104 commits, e a saída diz qual é qual.

#### Custo por fase

`tca fase <NOME>` marca cada transição do pipeline. Uma chamada por transição, e é o que
torna o custo de cada fase derivável: o intervalo entre commits mistura escrita de spec,
implementação e espera, e não responde **quanto custa especificar**.

`tca fase --listar` mostra a linha do tempo da MS ativa, com a duração de cada transição.
Sem marcação, avisa em vez de imprimir lista vazia.

`metrics` deriva `fase_<nome>_horas_mediana` para cada fase marcada, e
`custo_spec_horas_mediana` — soma de SPEC e PLAN — com a construção (RED, GREEN, EDGE) na
nota, para comparação direta.

Sem marcação, é **lacuna declarada, não zero**. E o comando é o único escritor de
`estado_da_trilha.fase_atual`.

#### Densidade de especificação e piso da decomposição

Dois indicadores que decidem **quão pequena a Micro Spec deve ser**.

**Densidade** — quanto a spec declara por unidade entregue. Spec pouco densa deixa espaço
para o agente inventar dentro da MS, que é a origem do preenchimento silencioso de lacuna:

| Indicador | O que diz |
|---|---|
| `linhas_por_arquivo_declarado` | superfície de invenção por unidade declarada |
| `arquivos_tocados_por_declarado` | 1,0 significa que entregou exatamente o previsto |
| `cenarios_por_ms_mediana` | densidade de cenário na spec |

Só é calculável em MS fechadas por `tca close-ms`, porque é ele que preserva o
`contexto_ativo` verbatim. Archive legado vira **lacuna declarada, não zero**.

**Piso da decomposição** — o que se paga por MS independente do tamanho. Duas parcelas:

- `custo_fixo_mecanico_segundos` — **medido**: tempo dos comandos de verificação;
- `custo_fixo_estimado_horas` — **estimado** pelo lead time do quartil de MS menores, e
  rotulado como **teto do piso**: se a menor MS observada tem centenas de linhas, o piso
  real é menor e desconhecido.

`custo_fixo_mecanico_pct` mostra a fração do piso que é máquina. Quando ela é próxima de
zero, o piso é humano — escrever spec, revisar, aprovar — e automatizar o fechamento **não
o baixa**.

#### Medição automática da suíte

`--medir-suite` executa e cronometra o comando que o projeto declara em
`tca.project.json`, e registra o resultado como `derivado:execucao` — não como reportado:

```json
{
  "comandos": {
    "testes": "pytest -q",
    "contar_testes": "pytest --collect-only -q | grep -c '::'"
  }
}
```

`contar_testes` precisa imprimir **somente um inteiro** em stdout. É contrato, não
formato adivinhado: sem ele, o número vira lacuna em vez de vir de parsing heurístico da
saída de um runner.

As duas medidas são independentes por um motivo prático: **contar é barato e não exige
ambiente; medir exige o projeto inteiro de pé**. `--contar-testes` roda só a contagem —
útil onde banco, fila ou serviços não estão disponíveis. `--medir-suite` executa a suíte
e, se houver contrato de contagem, conta também.

Sem `tca.project.json`, o comando **não adivinha** — registra a ausência como lacuna.
`--detectar` sugere o que declarar com base nos arquivos presentes, e nunca executa nada
por conta própria. Suíte que falha é registrada com o código de saída, porque tempo de
suíte quebrada não é o mesmo indicador que tempo de suíte verde.

O que continua não instrumentável aparece como **lacuna declarada**, não estimado:

- `token_por_ms` — o harness não expõe consumo ao processo;
- `ms_estacionadas` e `tempo_de_fila` — exigem a triagem de não conformidade em classes,
  que ainda não existe.

`--repo` mede outro repositório sem escrever nada nele. Sem `--write` é relatório puro:
não grava linha de base nem registro de execução — é comando de medida, não portão.

### `tca tune [--write]`

**Auto-ajuste por máquina.** Deriva parâmetros de execução do que foi medido *nesta*
máquina e do hardware dela, e emite `.tca/tuning-<host>.json`.

Existe porque medida de tempo sem ambiente é incomparável: 26s numa máquina de 4 núcleos
com disco mecânico não é o mesmo número que 26s noutra. Por isso **todo registro de
`tca metrics` carrega a impressão digital da máquina** — host, núcleos, RAM, disco
rotacional e sistema — e o `tune` só considera medições do próprio ambiente. Séries de
máquinas diferentes nunca se misturam.

Cada parâmetro sai com **porquê e evidência**:

| Parâmetro | Deriva de |
|---|---|
| `concorrencia_max` | núcleos, menos um em disco mecânico — o gargalo é I/O, não CPU |
| `isolamento_por_arquivo` | `overhead_pct` medido; acima de 60% recomenda desligar na camada sem I/O |
| `laco_local_por_selecao` | comparação entre `loop_local_segundos` e `suite_segundos` |
| `observadores_redundantes` | disco rotacional |

Sem medição da máquina, os parâmetros que dependem dela saem como `null` com a instrução
do que rodar — não com um valor inventado.

**A TCA emite; o projeto consome.** Nenhuma configuração de runner é alterada: escrever no
`vitest.config.ts` ou equivalente seria a TCA introduzir conteúdo que o projeto não
declarou. O arquivo gerado é por máquina e não é versionado — versionar faria o ajuste de
um ambiente governar os demais.

### `tca manifest [--write]`

Gera ou confere o `MANIFEST.sha256`. Existe porque gerar o manifesto com um comando
digitado à mão é passo que depende de disciplina — e foi assim que bytecode entrou no
manifesto e quebrou o `verify-self` em checkout limpo, passando localmente porque o
arquivo existia na máquina de quem rodou os testes.

`__pycache__`, `.pyc`, temporários e o próprio manifesto nunca entram.

### `tca verify-self`

Confere `MANIFEST.sha256` contra o conteúdo do pacote. A TCA é fonte canônica: precisa
ser verificável como qualquer outra.

### `tca version`

Versão e hash curto do manifesto.

## O núcleo do registro de archive

Seis campos, e só eles pertencem à TCA:

| Campo | Origem |
|---|---|
| `ms` | argumento, validado no formato `MS-NNN` |
| `titulo` | `**MS ativa:**` do contexto ou `--titulo` |
| `data_conclusao` | data da execução |
| `fase` | `estado_da_trilha.fase_atual` |
| `tca` | versão e manifesto do pacote que fechou |
| `contexto_ativo` | **texto integral** do `activeContext.md` no fechamento |

Tudo mais vai em `extensao`, livre para o projeto.

A escolha por `contexto_ativo` verbatim é deliberada: extrair contratos, arquivos e
cenários do markdown exigiria inferir estrutura que a especificação não define. Preservar
o texto integral não perde nada e não inventa nada. Quando o schema do contexto for
definido, a extração vira derivação de um dado que já está guardado.

## O portão de commit

`hooks/commit-msg` reprova commit cuja mensagem declara `[MS-NNN]` sem que o diff traga a
atualização dos artefatos de controle, e roda `tca verify` antes de deixar passar.

Emergência: `TCA_SKIP=1 git commit ...`. O aviso fica no terminal e o commit passa — a
saída existe, mas deixa rastro.

## Lacunas declaradas

Registradas em vez de preenchidas por inferência, conforme o invariante de proveniência.

- **`status_modulo_percentual` não é derivável.** Nenhum schema define campo de backlog no
  `payload_index.json`, embora vários skills o mencionem. Enquanto isso, `tca verify`
  emite aviso e o campo não é tocado.
- **`total_testes` não é derivado.** Contar testes depende do runner do projeto, e não há
  contrato declarando esse comando. Vem por `--testes N`; sem a flag, o campo é mantido
  como estava e o comando avisa. Um contrato de comandos do projeto resolveria isso —
  mas seria schema inventado, então fica para quando houver especificação.
- **Sem transação entre arquivos.** Cada escrita é atômica; o conjunto não é. `verify`
  detecta o estado parcial e o comando é idempotente, o que torna a recuperação trivial.
- **`doctor` não compara com o upstream.** Ele responde "os arquivos deste projeto
  conferem com o canon que veio junto?", não "esta TCA está atrasada em relação à
  publicada". Detectar defasagem de versão exige o pacote consultar a origem, o que
  depende de a distribuição existir.

## Testes

```sh
python3 tca/tests/test_tca.py
```

Biblioteca padrão apenas. O pacote não pode exigir runner de testes de nenhum stack.
