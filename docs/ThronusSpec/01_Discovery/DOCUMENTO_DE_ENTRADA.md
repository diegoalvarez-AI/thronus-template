# Documento de Entrada — gabarito

> Saída única do Discovery. Base da proposta comercial e insumo da execução.
> Seção não aplicável se declara como tal, com a razão. Nunca se omite em silêncio.
>
> Marcação obrigatória de procedência em toda afirmação: `[cliente]` · `[FMO]` ·
> `[premissa Thronus]` · `[A CONFIRMAR]`.

---

## 0. Identificação
Cliente · oportunidade · etapa do portfólio (1, 2 ou 3) · responsável Thronus · data · versão.

**Herança do diagnóstico:** versão do FMO · tier aplicado · data · perfil dimensional com banda
e **nível conservador adotado** por dimensão · confiança · estado dos três gates. Sem FMO:
registrar a exceção, quem a autorizou, e o substituto apresentado (evidência de mercado,
hipótese falseável, critério de morte).

## 1. Problema canônico
> "[Quem] precisa de [o quê] para [por quê], mas hoje isso é difícil porque [obstáculo]."

Uma frase, sem ambiguidade. Se não fecha, o Discovery não passou da fase O.

## 2. Valor esperado
Indicador · **baseline medido** e sua fonte · alvo · prazo de verificação · quem mede.
Sem baseline não há prova de entrega. Herdado do plano de validação do FMO.

## 3. Pessoas nomeadas
| Papel | Nome | Responsabilidade |
|---|---|---|
| Paga | | autoriza investimento |
| Decide escopo | | resolve dúvida de escopo em até [prazo] |
| Pode bloquear | | poder de veto declarado |
| Assina o portão | | por portão, conforme `tca.signatarios.json` |

## 4. Modelo da necessidade
Atores e responsabilidades · processo como é hoje · processo como passa a ser · dados que
entram, circulam e saem · regras que valem sempre e suas exceções · integrações obrigatórias.

**Fronteira:** o que o sistema faz, e o que fica fora.

## 5. Escopo
**Dentro** — cada item com critério de aceite verificável.
**Fora** — cada exclusão com a consequência declarada para o resultado.

Exclusão não escrita é escopo assumido.

## 6. Pré-condições do cliente
| Pré-condição | Dono (cliente) | Prazo | Destino | Consequência se não cumprida |
|---|---|---|---|---|

Destino é um de três: **obrigação do cliente** · **item de escopo precificado** ·
**exclusão declarada**. Sem destino, reprova G3.

## 7. Dimensionamento
Tamanho contado, com unidade e contagem explícitas · tipo de produto · nível de garantia com a
consequência da falha que o justifica · banda de esforço · **compromisso no extremo
conservador** · fatores que alargaram a banda, um a um.

## 8. Requisitos de qualidade
Classes de operação e volume por jornada crítica · natureza do dado (pessoal, financeiro,
multi-tenant) · dependências externas e o que acontece se cada uma cair · uso de modelo de
linguagem e teto aceitável · ambiente de uso do usuário final · operações irreversíveis.

Cada resposta parametriza `requisitos_do_produto` e `verificacoes` na execução.

## 9. Riscos e critérios de interrupção
| Risco | Probabilidade | Impacto | Mitigação | Gatilho de interrupção |
|---|---|---|---|---|

Critérios de interrupção herdados do plano de validação do FMO.

## 10. Incertezas residuais
Todo `[A CONFIRMAR]` que sobreviveu ao portão, com impacto declarado sobre a banda e o destino:
quem confirma, até quando, e o que acontece se não confirmar.

## 11. Registro dos portões
| Portão | Estado | Signatário | Data | Evidência | Justificativa |
|---|---|---|---|---|---|
| G1 — Necessidade compreendida | | | | | |
| G2 — Escopo delimitado | | | | | |
| G3 — Pré-condições assumidas | | | | | |
| G4 — Dimensionamento sustentado | | | | | |

Pendência condicionada exige responsável nomeado e prazo. Exceção a portão não atendido exige
instância superior, fundamento registrado e critério de interrupção — e o portão permanece
registrado como não atendido.
