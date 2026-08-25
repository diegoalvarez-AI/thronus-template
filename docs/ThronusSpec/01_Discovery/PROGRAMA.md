# Programa de Evolução — gabarito

> Saída principal do Discovery. Base da proposta comercial e do contrato, e a peça que permite
> ao cliente **evoluir dentro da linha de serviços da Thronus** em vez de comprar uma entrega
> isolada.
>
> Um programa pode ter itens de várias etapas do portfólio. A ordem é determinada pela
> dependência, não pelo valor do contrato.
>
> Procedência obrigatória: `[observado]` · `[relatado]` · `[FMO]` · `[premissa Thronus]` ·
> `[A ESCLARECER]`. O que foi relatado e não observado é declarado como tal.

---

## 0. Identificação
Cliente · setor · porte · responsável Thronus · datas do campo · versão do documento.

**Onboarding:** patrocinador nomeado · pessoas que executam liberadas · acessos concedidos ·
autorização de gravação · termo de dados · agenda fechada. Item pendente é pré-condição com
dono e prazo (seção 6), nunca motivo para começar assim mesmo.

**Herança do diagnóstico:** versão do FMO · tier aplicado · perfil dimensional com banda e
**nível conservador adotado** por dimensão · confiança · estado dos três gates.

## 1. Escopo do levantamento
**SIPOC** do processo levantado: fornecedor · entrada · processo · saída · cliente.
O que ficou **fora** do levantamento, e por quê.

## 2. Processo — como é hoje e como passa a ser
Registro em Domain Storytelling: atores · objetos de trabalho · atividades · sistemas e
planilhas realmente em uso.
**Glossário do cliente** — termo, significado, sinônimos em circulação.
**Quem validou** o registro e quando. Validação é de quem executa o processo.

**To-be candidato, lado a lado com o as-is.** Para cada atividade: qual restrição a justificava,
qual capacidade a dissolve (`METODO.md` §1.2), e o que passa a acontecer no lugar. As atividades
que se **preservam por exigirem julgamento, relacionamento ou responsabilização** são declaradas
explicitamente.

## 3. Perda medida
| Oportunidade | Onde ocorre | **Eixo de valor** | Medida | Método e amostra | Baseline | Quem mede |
|---|---|---|---|---|---|---|

Eixo é um de quatro: produtividade · ineficiência corrigida · custo · faturamento
(`METODO.md` §7). Faturamento exige a cadeia causal escrita.

Tempo de atravessamento contra tempo de processamento · espera · retrabalho · redigitação ·
aprovação parada. Oportunidade sem número não entra.

## 4. Intervenções propostas
| # | Oportunidade | Natureza | Etapa | Dono (cliente) | Critério de sucesso | Se não for feita |
|---|---|---|---|---|---|---|

Natureza conforme `INTERVENCOES.md`. **Salto na ordem ESIA exige justificativa** na seção 9.

## 5. Trilha sequenciada
Ordem de execução com as dependências explícitas.

```
[item] → depende de → [item ou pré-condição]
```

Regras que a trilha respeita: não se mede o que não está definido · não se automatiza o que não
está estável · não se constrói sobre dado que não existe · não se entrega o que a equipe não
sabe operar.

## 6. Pré-condições do cliente
| Pré-condição | Dono (cliente) | Prazo | Destino | Consequência se não cumprida |
|---|---|---|---|---|

Destino é um de três: **obrigação do cliente** · **item de programa precificado** ·
**exclusão declarada**. Sem destino, reprova G4.

## 7. Adoção e capacitação
Itens de capacitação com **comportamento-alvo** — o que a pessoa passará a fazer diferente.
Sequência ADKAR: consciência e desejo antes de conhecimento e habilidade; reforço com dono e
prazo após a entrega. Avaliação no nível de comportamento, observada no trabalho.

## 7-A. Valor entregue durante o Discovery
| Intervenção | Dor atacada | Baseline | Medida após | Em uso desde | Operada por |
|---|---|---|---|---|---|

De uma a três intervenções **em uso**, não protótipo (`METODO.md` §5). Portão G6 depende disto.

## 7-B. Trabalho assistido por IA
O que foi transcrito, reconstruído, cruzado ou redigido por agente, e o que foi validado em
campo. Toda afirmação deste documento carrega procedência — `[observado]`, `[relatado]`,
`[inferido pela IA]` — e o que está como inferido não sustentou portão.

## 8. Dimensionamento
Por item: unidade da sua natureza · banda de esforço · **compromisso no extremo conservador** ·
fatores que alargaram a banda. Total do programa e total por etapa do portfólio.
Ver `DIMENSIONAMENTO.md`.

## 9. Desvios justificados
Salto na ordem ESIA · portão atendido por exceção · obrigação dispensada. Um por linha, com
instância superior nomeada, fundamento e critério de interrupção.

## 10. Riscos e critérios de interrupção
| Risco | Probabilidade | Impacto | Mitigação | Gatilho de interrupção |
|---|---|---|---|---|

Critérios de interrupção herdados do plano de validação do FMO.

## 11. Itens a esclarecer
Todo `[A ESCLARECER]` que sobreviveu ao portão: impacto declarado sobre a banda, quem confirma,
até quando, e o que acontece se não confirmar.

## 12. Registro dos portões
| Portão | Estado | Signatário (humano) | Data | Evidência | Justificativa |
|---|---|---|---|---|---|
| G1 — Processo compreendido | | | | | |
| G2 — Perda medida | | | | | |
| G3 — Redesenho justificado | | | | | |
| G4 — Pré-condições assumidas | | | | | |
| G5 — Programa dimensionado | | | | | |
| G6 — Valor entregue | | | | | |

## 13. Itens que seguem para a TCA
| Item do programa | Natureza | Tipo de produto | Nível de garantia | Documento de Entrada |
|---|---|---|---|---|

Cada um recebe o seu `DOCUMENTO_DE_ENTRADA.md`. Os demais são entregues pelo artefato da sua
natureza, com o mesmo rigor de critério de aceite e evidência.
