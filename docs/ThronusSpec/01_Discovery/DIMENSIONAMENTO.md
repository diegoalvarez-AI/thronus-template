# Discovery — Dimensionamento de Escopo, Prazo e Custo

> Como se chega a tamanho, prazo e preço sem extrapolá-los de um instrumento de prontidão.
> Ver `METODO.md` §1.

---

## 1. Três grandezas independentes

Colapsá-las num número só é a origem da falha grosseira de prazo e custo.

| Grandeza | De onde vem | O que decide |
|---|---|---|
| **Tamanho** | contado no modelo da necessidade (fase N) | quantas Micro Specs, quanto paralelismo |
| **Tipo de produto** | natureza do que se constrói | quais eixos de qualidade existem |
| **Nível de garantia** | consequência da falha | quanto rigor em cada eixo, quais portões operam |

Atravessando as três, o **risco de execução**, que vem do FMO e alarga a banda sem alterar o
tamanho contado.

---

## 2. Tamanho — contado, nunca inferido

Sai do modelo produzido na fase N. A unidade muda com a etapa do portfólio:

| Etapa | Unidade contada |
|---|---|
| **1 — Automação e Agentes** | fluxos conversacionais · intenções · canais · integrações · rotinas |
| **2 — Operações Inteligentes** | indicadores · fontes de dado · rotinas de operação · painéis |
| **3 — Produto Digital** | casos de uso candidatos · regras de negócio · entidades · integrações |

A contagem é do modelo, não da conversa. Item que não está modelado não está contado — e se for
relevante, está como `[A CONFIRMAR]` alargando a banda.

**Conversão em Micro Specs.** A relação entre unidade contada e Micro Spec é medida no
histórico da própria Thronus, não estipulada. Até haver série suficiente, a conversão é
premissa declarada da proposta, com a base explicitada. Lacuna conhecida, não omissão.

---

## 3. Tipo de produto

| Tipo | Eixos que passam a valer | Eixos que não se aplicam |
|---|---|---|
| `agente` | teto de token, caminho de degradação, confirmação humana em ação irreversível | — |
| `automacao` | idempotência, reprocessamento, trilha de execução | interface completa |
| `operacao` | qualidade e origem do dado, invalidação de cache, exportação | teto de token, se não houver modelo |
| `api` | contrato versionado, depreciação, limite por consumidor | sete estados de interface |
| `site` | orçamento de carga, indexação, tempo de primeira pintura | isolamento de linha, se não houver conta |
| `saas` | multi-tenant com isolamento de linha, medição de uso, faturamento | — |
| `sistema` | isolamento de linha, trilha de auditoria, reversibilidade | — |

Tipo é atribuído por evidência do modelo. Produto que é dois tipos recebe a **união** das
obrigações, nunca a interseção.

---

## 4. Nível de garantia

Da consequência da falha, não do tamanho. Um script pode ser G3; uma plataforma pode ser G1.

| Nível | Consequência da falha | Efeito |
|---|---|---|
| **G1 — operacional** | incômodo, retrabalho interno, nada sai da empresa | rigor mínimo do perfil |
| **G2 — material** | perda financeira, perda de prazo, cliente do cliente afetado | trilha de auditoria, teste negativo de acesso, reversibilidade testada |
| **G3 — institucional** | dano a terceiro, sanção legal, quebra de contrato ou de edital | tudo de G2, mais retenção declarada, ensaio de restauração e portão com signatário nomeado |

Dado pessoal, dinheiro de terceiro ou obrigação de edital elevam a G3 independentemente de
qualquer outra consideração.

---

## 5. Risco de execução — onde o FMO entra

O FMO **não estima tamanho**. Responde a outra pergunta: qual a probabilidade de o trabalho ser
interrompido, retrabalhado, ou de a entrega não ser adotada.

| Dimensão em nível baixo | Efeito no dimensionamento |
|---|---|
| **Processos** | requisito instável durante a execução → alarga a banda; exige reversibilidade e entrega faseada |
| **Dados** | dado real diferente do descrito → alarga a banda; gera **pré-condição**, não escopo silencioso |
| **Governança** | decisão e acesso demoram → alarga o prazo; exige decisor nomeado com prazo de resposta |
| **Qualificação** | adoção lenta → orçamento de interação apertado e material de apoio, itens precificados |
| **Receptividade** | resistência à mudança → entrega faseada e comunicação; medir adoção, não só erro |

**Baixa maturidade não aumenta o nosso escopo por si só.** Gera pré-condição, que recebe um dos
três destinos do `METODO.md` §5. Absorver em silêncio é o mecanismo do estouro.

Como o nível usado é sempre o **inferior da banda** (FMO §4.3), o alargamento é conservador por
construção.

---

## 6. Banda de esforço e compromisso conservador

O esforço é **intervalo**, nunca ponto. O compromisso comercial — prazo e preço — usa o
**extremo superior de esforço**, o conservador. O extremo otimista é calibração interna e nunca
é comunicado como prazo.

A largura é função declarada de contadores, não de sensação:

| Fator | Efeito na banda |
|---|---|
| Itens `[A CONFIRMAR]` no modelo | cada um declara o seu impacto; a soma alarga |
| Dimensões do FMO em nível baixo ou em banda | alargam, por §5 |
| Confiança registrada no diagnóstico | confiança baixa alarga |
| Precedente na própria Thronus | trabalho semelhante já entregue estreita |

**Critério de parada:** a banda está estreita o bastante para comprometer no extremo conservador
sem inviabilizar a proposta. Alcançado isso, para. Não alcançado, o que falta é `[A CONFIRMAR]`
nomeado — e a decisão é levantar mais, reduzir escopo, ou declarar a faixa e precificar o risco.

Os fatores de alargamento devem ser **calibrados contra o histórico real** de prazo estimado
versus realizado. Até haver série suficiente, são premissa declarada e revisável — pela mesma
razão que o FMO declara que suas faixas serão recalibradas após o piloto.

---

## 7. O que vai para a proposta

| Item | Origem |
|---|---|
| Escopo comprometido e **exclusões explícitas** | fase N e portão G2 |
| Prazo e investimento | banda, no extremo conservador |
| Pré-condições do cliente com dono, prazo e consequência | mapa de pré-condições do FMO, portão G3 |
| Indicador de sucesso com baseline medido | plano de validação do FMO |
| Critérios de interrupção | plano de validação do FMO |
| Premissas declaradas e sua base | fatores de banda deste documento |

Proposta que não carrega exclusões, pré-condições e premissas não está comprometendo escopo —
está apostando nele.
