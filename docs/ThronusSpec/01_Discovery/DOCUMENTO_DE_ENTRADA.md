# Documento de Entrada — gabarito

> Artefato dos itens do Programa que **viram software** — integração, automação, agente,
> orquestração, painel, API, sistema. Um por item. Os demais itens têm o artefato da sua
> natureza, em `INTERVENCOES.md`. A saída principal do Discovery é o `PROGRAMA.md`.
> Estrutura na acepção da **ISO/IEC/IEEE 29148**: todo requisito é verificável e rastreável, e
> requisito de qualidade é expresso na taxonomia da série 250xx.
>
> Seção não aplicável se declara como tal, com a razão. Nunca se omite em silêncio.
> Procedência obrigatória em toda afirmação: `[cliente]` · `[FMO]` · `[premissa Thronus]` ·
> `[A ESCLARECER]`.

---

## 0. Identificação
Cliente · oportunidade · etapa do portfólio · responsável Thronus · data · versão.

**Herança do diagnóstico:** versão do FMO · tier aplicado · data · perfil dimensional com banda
e **nível conservador adotado** por dimensão · confiança · estado dos três gates. Sem FMO:
registrar a exceção, quem a autorizou, e o substituto (evidência de mercado, hipótese falseável,
critério de morte).

## 1. Problema canônico
> "[Quem] precisa de [o quê] para [por quê], mas hoje isso é difícil porque [obstáculo]."

Uma frase, sem ambiguidade.

## 2. Valor esperado
Indicador · **baseline medido** e sua fonte · alvo · prazo de verificação · quem mede.
Herdado do plano de validação do FMO. Sem baseline não há prova de entrega.

## 3. Pessoas nomeadas
| Papel | Nome | Responsabilidade |
|---|---|---|
| Paga | | autoriza investimento |
| Decide escopo | | resolve dúvida de escopo em até [prazo] |
| Pode bloquear | | poder de veto declarado |
| Assina o portão | | por portão, conforme `tca.signatarios.json` |

## 4. Modelo da necessidade
Instrumento aplicado (Domain Storytelling · EventStorming · Event Modeling) e por quê.

**Linguagem ubíqua** — termo canônico, definição, sinônimos proibidos.
**Contextos delimitados** — cada um com sua responsabilidade e suas fronteiras. São a fronteira
de decomposição em Micro Specs.
**Atores, objetos de trabalho e eventos de domínio.**
**Processo como é hoje** e **como passa a ser**.
**Integrações obrigatórias** e o que acontece se cada uma estiver indisponível.

## 5. Requisitos funcionais — EARS

Cada requisito recebe identificador `UC-NN` (caso de uso) ou `RN-NN` (regra de negócio), em um
dos cinco padrões, e nenhum outro formato:

| ID | Padrão | Requisito | Contexto delimitado | Critério de aceite |
|---|---|---|---|---|
| UC-01 | dirigido a evento | *Quando [gatilho], o sistema deve [resposta].* | | verificável |
| RN-01 | ubíquo | *O sistema deve [resposta].* | | verificável |

Padrões admitidos: ubíquo · dirigido a evento (*Quando*) · dirigido a estado (*Enquanto*) ·
comportamento indesejado (*Se… então*) · recurso opcional (*Onde*) · combinações.

Estes identificadores são o universo de `comandos.listar_requisitos` na TCA e a origem dos
cenários do `[ESTADO_RED]`.

## 6. Requisitos de qualidade — ISO/IEC 25010:2023

Uma linha por característica. "Não se aplica" é resposta válida; omissão não é.

| Característica | Requisito, com medida e limiar | Procedência |
|---|---|---|
| Adequação funcional | | |
| Eficiência de desempenho | por classe de operação: leitura interativa · escrita · relatório · lote | |
| Compatibilidade | | |
| Capacidade de interação | inclui acessibilidade e ambiente de uso do usuário final | |
| Confiabilidade | inclui comportamento sob falha de cada dependência externa | |
| Segurança | inclui natureza do dado: pessoal, financeiro, multi-tenant | |
| Manutenibilidade | | |
| Flexibilidade | inclui volume esperado e crescimento | |
| *Safety* | obrigatória a partir de G2: identificação de risco, falha segura, aviso de perigo, supervisão humana proporcional | |

Esta seção parametriza `requisitos_do_produto` e o esqueleto de `verificacoes` na TCA.

## 7. Escopo
**Dentro** — cada item com critério de aceite verificável.
**Fora** — cada exclusão com a consequência declarada para o resultado.

Exclusão não escrita é escopo assumido.

## 8. Pré-condições do cliente
| Pré-condição | Dono (cliente) | Prazo | Destino | Consequência se não cumprida |
|---|---|---|---|---|

Destino é um de três: **obrigação do cliente** · **item de escopo precificado** ·
**exclusão declarada**. Sem destino, reprova G3.

## 9. Dimensionamento
**Tamanho funcional** — fronteira declarada · processos funcionais · movimentos Entry, Exit,
Read e Write por processo · total em CFP · conversão para Micro Specs com a premissa explicitada.

**Tipo de produto** · **nível de garantia** com a consequência da falha que o justifica ·
**banda de esforço** · **compromisso no extremo conservador** · fatores de alargamento, um a um.

## 10. Riscos e critérios de interrupção
| Risco | Probabilidade | Impacto | Mitigação | Gatilho de interrupção |
|---|---|---|---|---|

Critérios de interrupção herdados do plano de validação do FMO.

## 11. Itens a esclarecer
Todo `[A ESCLARECER]` que sobreviveu ao portão: impacto declarado em CFP potencial, quem
confirma, até quando, e o que acontece se não confirmar.

## 12. Registro dos portões
| Portão | Estado | Signatário | Data | Evidência | Justificativa |
|---|---|---|---|---|---|
| G1 — Necessidade compreendida | | | | | |
| G2 — Escopo delimitado | | | | | |
| G3 — Pré-condições assumidas | | | | | |
| G4 — Dimensionamento sustentado | | | | | |

## 13. Desvios justificados
Portão atendido por exceção, ou obrigação de perfil dispensada. Um por linha, com instância
superior nomeada, fundamento e critério de interrupção. O portão permanece registrado como não
atendido.
