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
