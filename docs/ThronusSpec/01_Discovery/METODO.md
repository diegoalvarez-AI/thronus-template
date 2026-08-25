# Discovery Thronus — Método PONTE

> **Conteúdo canônico.** Converte oportunidade diagnosticada em **escopo comprometido**:
> preço, prazo e parametrização técnica que se sustentam na evidência coletada.
>
> Fontes: FMO AI-First v4.1 (Alvarez & Alvarez, ago/2026) · portfólio Thronus em etapas ·
> protocolo de portão do ÂNCORA · TCA (`tca/METODOLOGIA.md`).
>
> Versão 1.0 · Agosto de 2026

---

## 1. Posição na cadeia

```
Etapa 0 — Diagnóstico AI-First (FMO)    prontidão do cliente e oportunidade identificada
        ↓  seis saídas do §4.6
DISCOVERY (PONTE)                        oportunidade → escopo comprometido
        ↓  Documento de Entrada
Etapas 1 a 4 — execução                  automação · operações · produto · growth
```

Para a Etapa 3 — Produto Digital Sob Medida — o Documento de Entrada é o insumo da TCA, e
permite que `[ESTADO_DISCOVERY]` e `[ESTADO_FUNCTIONAL]` rodem sem redescobrir nada.

**O que o Discovery não é.** Não é o `[ESTADO_DISCOVERY]` da TCA. Aquele é fase interna de um
projeto de software já contratado. Este é anterior ao contrato e vale para as Etapas 1, 2 e 3.

**O que ele resolve.** Sem ele, escopo, prazo e preço são comprometidos logo após o
diagnóstico. Mas o FMO mede prontidão organizacional, não tamanho de trabalho. Maturidade
informa **risco de execução e pré-condições** — nunca tamanho. Tamanho vem do modelo da
necessidade, e o modelo da necessidade é o que o Discovery produz.

---

## 2. O que o Discovery recebe

As seis saídas do diagnóstico (FMO v4.1, §4.6) são insumo obrigatório e **não são recoletadas**:

| Saída do FMO | Uso no Discovery |
|---|---|
| Perfil dimensional — nível, evidência, confiança e **lacunas** por dimensão | fator de risco de execução; as lacunas viram pauta do levantamento |
| **Mapa de pré-condições** | obrigações do cliente — nunca escopo nosso silencioso (§5) |
| **Portfólio de oportunidades** — casos por valor, esforço, risco, dependências | a oportunidade a enquadrar sai daqui |
| Registro de decisão — estado dos três gates | gate não atendido bloqueia; condicionado entra como pendência com dono |
| Plano de validação — indicadores, baseline, hipótese de valor, **critérios de interrupção** | vira o critério de sucesso e o gatilho de parada |
| Registro de apuração — par de respostas, banda, nível conservador, confiança | define a profundidade exigida (§6) |

**Regras herdadas, não reinterpretadas.** Nível por evidência atual, não por intenção declarada.
Escore em fronteira se exibe em banda, nunca como nível único. **Toda decisão derivada usa o
nível inferior da banda** — e dimensionamento de escopo é decisão derivada (FMO §4.3). Nível de
Tier 1 (T1-L1 a T1-L4) não é intercambiável com nível de Tier 2, e L5 só existe no Tier 2. O
perfil dimensional é o resultado; a média agregada é descritiva e secundária.

**Quando não há FMO.** Produto próprio da Thronus não tem cliente a diagnosticar. É a única
entrada legítima sem FMO, e exige o substituto: evidência de oportunidade de mercado, hipótese
falseável e **critério de morte declarado**. Ausência de FMO em engajamento com cliente é
exceção declarada, com responsável nomeado — nunca caminho normal.

---

## 3. As cinco fases

### P — Portfólio recebido
Ler as seis saídas. Verificar elegibilidade: os três gates do FMO — valor e viabilidade,
viabilidade técnica e de dados, IA responsável — estão atendidos ou condicionados para esta
oportunidade? Gate não atendido encerra aqui: o caso de uso é adiado, redesenhado, limitado ou
rejeitado (FMO §4.5). Registrar o que se herdou e com que confiança.

### O — Oportunidade enquadrada
Uma oportunidade do portfólio por vez. Produzir:
- **Problema canônico**: "[Quem] precisa de [o quê] para [por quê], mas hoje isso é difícil
  porque [obstáculo]." Se a frase não fecha sem ambiguidade, o enquadramento não terminou.
- **Valor esperado** com indicador e **baseline medido**, herdado do plano de validação do FMO.
  Sem baseline não há prova de entrega, e sem prova não há expansão nem case.
- **Decisores nomeados**: quem paga, quem decide escopo, quem pode bloquear, quem assina.
- **Etapa do portfólio**: 1, 2 ou 3. Determina o instrumento da fase seguinte e o destino da saída.

### N — Necessidade levantada e modelada
Instrumento conforme o modo de entrada — a saída é a mesma, o caminho não:

| Modo de entrada | Instrumento | Risco dominante |
|---|---|---|
| Cliente estruturado, não documentado | entrevista dirigida e transcrição crítica | distorcer ou perder o que foi dito |
| Cliente de baixa maturidade | modelagem do processo como ele é hoje | resolver o problema errado |
| Oportunidade interna (produto próprio) | evidência de mercado e hipótese falseável | construir o que ninguém compra |

Modelar, em linguagem de negócio: atores e responsabilidades · processo como é hoje e como
passa a ser · dados que entram, circulam e saem · regras que valem sempre e suas exceções ·
fronteiras — o que o sistema faz e o que fica fora · integrações obrigatórias.

**O que ninguém disse não vira requisito.** Vira `[A CONFIRMAR]`, contável, com impacto
declarado sobre a banda de tamanho. Item não confirmado até o portão vira exclusão explícita de
escopo ou pendência com dono. Nunca premissa silenciosa.

### T — Tamanho e tipo declarados
Ver `DIMENSIONAMENTO.md`. Tamanho **contado** a partir do modelo e expresso em **banda**; tipo
de produto e nível de garantia atribuídos por evidência; FMO entra como fator de risco e como
pré-condição, nunca como estimador de tamanho.

### E — Entrada comprometida
Passar pelos quatro portões (§4). Colher assinatura dos responsáveis nomeados. Emitir o
**Documento de Entrada** (`DOCUMENTO_DE_ENTRADA.md`), que é ao mesmo tempo a base da proposta
comercial e o insumo da execução.

---

## 4. Portões não compensatórios

Protocolo idêntico ao do FMO §4.5 e ao `tca gate`: três estados, mudança privativa de
responsável nomeado, com data, evidência consultada e justificativa.

| Portão | Pergunta de decisão |
|---|---|
| **G1 — Necessidade compreendida** | O problema canônico é enunciável sem ambiguidade, atores, dados e regras estão modelados, e o que ficou incerto está declarado e quantificado. |
| **G2 — Escopo delimitado** | O que está dentro e o que está fora está escrito, e cada item de escopo tem critério de aceite verificável. |
| **G3 — Pré-condições assumidas** | Cada pré-condição tem dono nomeado **do lado do cliente**, prazo e consequência declarada se não for cumprida. |
| **G4 — Dimensionamento sustentado** | O tamanho é contado a partir do modelo, a banda tem base declarada, tipo e nível de garantia saem de evidência, e o compromisso usa o extremo conservador. |

**Não compensação.** Precisão de estimativa não compensa escopo indefinido. Confiança alta em
uma dimensão não neutraliza ausência em outra.

| Estado | Condição | Consequência |
|---|---|---|
| **Atendido** | todos os elementos satisfeitos | não obstrui o compromisso |
| **Condicionado** | núcleo satisfeito, subsiste obrigação acessória | compromisso admissível, com pendência rastreada, dono e prazo |
| **Não atendido** | qualquer elemento essencial insatisfeito | compromisso obstruído, sem compensação |

Exceção só por decisão expressa de instância superior à do avaliador, com registro do
fundamento, do responsável e do critério de interrupção. A exceção é documentada e **não altera
o resultado registrado**, que permanece como não atendido.

---

## 5. Pré-condição do cliente não é escopo nosso

É a regra que mais protege prazo e custo.

O mapa de pré-condições do FMO lista o que precisa existir antes da automação ou da IA — dado
organizado, processo documentado, papéis definidos, acesso concedido, decisão tomada. Absorver
isso no escopo sem precificar é o mecanismo pelo qual o prazo estoura: a entrega fica parada
esperando algo que ninguém se comprometeu a fazer.

Cada pré-condição recebe um destino explícito, e só três são admissíveis:

1. **Obrigação do cliente** — dono nomeado, prazo, e consequência declarada do descumprimento.
2. **Item de escopo precificado** — a Thronus faz, e isso está no preço e no prazo.
3. **Exclusão declarada** — não será feito, e a consequência para o resultado está escrita.

Pré-condição sem destino reprova G3.

---

## 6. Profundidade proporcional

O Discovery não tem tamanho fixo. A profundidade é proporcional ao **nível de garantia** e ao
tamanho contado, pelo mesmo princípio que faz o FMO ter dois tiers.

**O critério de parada é a largura da banda, não a completude do documento.** Levanta-se até que
a banda seja estreita o bastante para comprometer preço e prazo no extremo conservador — e para
aí. Continuar depois disso consome margem para reduzir incerteza que já não muda a decisão.

Seção sem consumidor declarado não se produz. Todo item aponta para quem o lê: o portão, a
proposta comercial, ou a parametrização da execução.

---

## 7. Saídas

Um artefato, dois consumidores. O **Documento de Entrada** alimenta:

**Comercial**: escopo comprometido e exclusões, banda de esforço com compromisso no extremo
conservador, pré-condições como cláusula contratual, critérios de interrupção.

**Execução (TCA, Etapa 3)**: perfil, tipo de produto e nível de garantia; limiares de
`requisitos_do_produto`; esqueleto de `verificacoes`; candidatos a UC e RN; e o registro de
decisão que a `[ESTADO_ARCHITECTURE]` precisa responder.

Nas Etapas 1 e 2 o destino é a implantação, não a TCA. O documento é o mesmo, e as seções não
aplicáveis são declaradas como tal, nunca omitidas em silêncio.

---

## 8. Invariantes

- **Maturidade não estima tamanho.** Informa risco e pré-condição.
- **Compromisso no extremo conservador da banda.** O extremo otimista é calibração.
- **Evidência acima de intenção declarada.** Na dúvida, o nível inferior.
- **Pré-condição do cliente tem dono nomeado, prazo e consequência.**
- **O que ninguém disse não vira requisito** — vira `[A CONFIRMAR]` com impacto declarado.
- **Portão não compensatório.** Nenhuma dimensão compensa a ausência de outra.
- **Indeterminação declarada é preferível a precisão não sustentada** (FMO §4.3).
