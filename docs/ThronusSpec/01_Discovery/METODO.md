# Discovery Thronus — Método PONTE

> **Conteúdo canônico.** Converte oportunidade diagnosticada em **escopo comprometido**:
> preço, prazo e parametrização técnica sustentados em evidência e em prática estabelecida.
>
> Versão 2.0 · Agosto de 2026

---

## 1. Âncoras metodológicas

Nada aqui é invenção de casa. Cada mecanismo tem origem declarada e verificável.

| Mecanismo | Âncora | O que se toma |
|---|---|---|
| Estrutura do conjunto de requisitos | **ISO/IEC/IEEE 29148** | requisito é verificável e rastreável por definição; requisito de qualidade é remetido à série 250xx |
| Taxonomia de qualidade | **ISO/IEC 25010:2023** | nove características, incluindo *Safety*, acrescentada na revisão de 2023 |
| Sintaxe de requisito | **EARS** (Mavin, Rolls-Royce, 2009) | cinco padrões de frase que tornam o requisito parseável sem DSL |
| Modelagem colaborativa | **Domain Storytelling · EventStorming · Event Modeling** | instrumento da fase N; contexto delimitado como fronteira de decomposição |
| Ambiguidade como artefato | **spec-kit (GitHub)** | marcador de esclarecimento contável e bloqueante; desvio de portão exige justificativa escrita |
| Tamanho funcional | **COSMIC — ISO/IEC 19761** | quatro tipos de movimento de dado; medida por processo funcional |
| Rigor proporcional à criticidade | **DO-178C · IEC 61508** | a criticidade classificada determina quais objetivos de ciclo de vida se aplicam |
| Prontidão, bandas e não compensação | **FMO AI-First v4.1** | seis saídas do §4.6, exibição em banda, nível conservador, três gates |
| Protocolo de portão | **ÂNCORA** | três estados, signatário nomeado, não compensação |

---

## 2. Posição na cadeia

```
Etapa 0 — Diagnóstico AI-First (FMO)    prontidão do cliente e oportunidade identificada
        ↓  seis saídas do §4.6
DISCOVERY (PONTE)                        oportunidade → escopo comprometido
        ↓  Documento de Entrada
Etapas 1 a 4 — execução                  automação · operações · produto · growth
```

Na Etapa 3 o Documento de Entrada é o insumo da TCA e permite que `[ESTADO_DISCOVERY]` e
`[ESTADO_FUNCTIONAL]` rodem sem redescobrir nada.

**O que ele resolve.** Sem ele, escopo, prazo e preço saem do diagnóstico. Mas o FMO mede
prontidão organizacional, não tamanho de trabalho. Maturidade informa **risco de execução e
pré-condições**; tamanho se mede no modelo da necessidade, por COSMIC.

---

## 3. O que o Discovery recebe

As seis saídas do FMO §4.6 são insumo obrigatório e **não são recoletadas**:

| Saída do FMO | Uso no Discovery |
|---|---|
| Perfil dimensional — nível, evidência, confiança, **lacunas** | fator de risco de execução; lacunas viram pauta do levantamento |
| **Mapa de pré-condições** | obrigações do cliente — nunca escopo nosso silencioso (§6) |
| **Portfólio de oportunidades** | a oportunidade a enquadrar sai daqui |
| Registro de decisão dos três gates | não atendido bloqueia; condicionado entra como pendência com dono |
| Plano de validação — indicador, baseline, **critérios de interrupção** | critério de sucesso e gatilho de parada |
| Registro de apuração — banda, nível conservador, confiança | calibra a profundidade exigida (§7) |

**Regras herdadas, não reinterpretadas.** Nível por evidência atual, não por intenção declarada.
Escore em fronteira se exibe em banda, nunca como nível único. **Toda decisão derivada usa o
nível inferior da banda** — e dimensionamento de escopo é decisão derivada (FMO §4.3). Nível de
Tier 1 não é intercambiável com nível de Tier 2, e L5 só existe no Tier 2.

**Quando não há FMO.** Produto próprio não tem cliente a diagnosticar. É a única entrada
legítima sem FMO, e exige o substituto: evidência de mercado, hipótese falseável e **critério de
morte declarado**. Ausência de FMO com cliente é exceção declarada, com responsável nomeado.

---

## 4. As cinco fases

### P — Portfólio recebido
Ler as seis saídas. Verificar elegibilidade contra os três gates do FMO. Gate não atendido
encerra aqui: o caso de uso é adiado, redesenhado, limitado ou rejeitado (FMO §4.5).

### O — Oportunidade enquadrada
- **Problema canônico**: "[Quem] precisa de [o quê] para [por quê], mas hoje isso é difícil
  porque [obstáculo]." Se a frase não fecha sem ambiguidade, a fase não terminou.
- **Valor esperado** com indicador e **baseline medido**, herdado do plano de validação do FMO.
- **Decisores nomeados**: quem paga, quem decide escopo, quem bloqueia, quem assina.
- **Etapa do portfólio**: 1, 2 ou 3.

### N — Necessidade levantada e modelada

O instrumento é escolhido pelo modo de entrada; a saída é a mesma.

| Modo de entrada | Instrumento | Por quê |
|---|---|---|
| Cliente estruturado, não documentado | **Domain Storytelling** + entrevista dirigida | narra como o trabalho acontece com atores e objetos de trabalho; a história é a validação |
| Cliente de baixa maturidade | **EventStorming** big picture, depois Domain Storytelling do processo atual | descobre eventos e fronteiras quando ninguém sabe descrever o processo |
| Oportunidade interna (produto próprio) | **Event Modeling** das jornadas + evidência de mercado | mapeia jornada de usuário e de API antes de existir usuário |

Da modelagem saem, obrigatoriamente: **contextos delimitados** — que são a fronteira de
decomposição em Micro Specs, e não um recorte arbitrário — linguagem ubíqua com sinônimos
proibidos, atores, objetos de trabalho, eventos de domínio, regras e suas exceções, integrações.

**Requisito se escreve em EARS.** Os cinco padrões, e nenhum outro formato:

| Padrão | Forma | Uso |
|---|---|---|
| Ubíquo | *O sistema deve [resposta].* | vale sempre |
| Dirigido a evento | *Quando [gatilho], o sistema deve [resposta].* | reação a acontecimento |
| Dirigido a estado | *Enquanto [estado], o sistema deve [resposta].* | vale durante uma condição |
| Comportamento indesejado | *Se [gatilho], então o sistema deve [resposta].* | erro, falha, abuso |
| Recurso opcional | *Onde [recurso está presente], o sistema deve [resposta].* | variação de configuração |

Combinações são admitidas — *Enquanto [estado], quando [gatilho], o sistema deve [resposta]*.
Frase que não cabe em nenhum padrão não é requisito: é intenção, e volta para o levantamento.
É esta sintaxe que faz o requisito virar cenário de teste no `[ESTADO_RED]` sem tradução humana.

**Requisitos de qualidade na taxonomia ISO/IEC 25010:2023**, característica por característica,
declarando quando não se aplica: adequação funcional · eficiência de desempenho ·
compatibilidade · capacidade de interação · confiabilidade · segurança · manutenibilidade ·
flexibilidade · *safety*. É esta seção que parametriza `requisitos_do_produto` na TCA.

**Ambiguidade é artefato, não silêncio.** O que ninguém disse vira `[A ESCLARECER]` — contável,
com impacto declarado sobre a banda, e bloqueante no portão G1. Item não resolvido até o portão
vira exclusão explícita de escopo ou pendência com dono. Nunca premissa silenciosa.

### T — Tamanho e tipo declarados
Ver `DIMENSIONAMENTO.md`: tamanho medido em COSMIC a partir dos processos funcionais
modelados; tipo de produto e nível de garantia atribuídos por evidência; FMO entra como risco de
execução e pré-condição.

### E — Entrada comprometida
Passar pelos quatro portões (§5). Colher assinatura dos responsáveis nomeados. Emitir o
**Documento de Entrada**.

---

## 5. Portões não compensatórios

Protocolo do FMO §4.5 e do `tca gate`: três estados, mudança privativa de responsável nomeado,
com data, evidência consultada e justificativa.

| Portão | Pergunta de decisão | Verificação |
|---|---|---|
| **G1 — Necessidade compreendida** | O problema fecha sem ambiguidade, o modelo tem contextos delimitados e linguagem ubíqua, e todo requisito está em um dos cinco padrões EARS. | zero `[A ESCLARECER]` sem destino |
| **G2 — Escopo delimitado** | Dentro e fora estão escritos, e cada item de escopo tem critério de aceite verificável na acepção da ISO 29148. | todo requisito é verificável e rastreável |
| **G3 — Pré-condições assumidas** | Cada pré-condição tem dono nomeado **do lado do cliente**, prazo e consequência declarada. | nenhuma pré-condição sem destino |
| **G4 — Dimensionamento sustentado** | Tamanho medido em COSMIC, banda com base declarada, tipo e nível de garantia por evidência, compromisso no extremo conservador. | contagem de CFP registrada e auditável |

**Não compensação.** Precisão de estimativa não compensa escopo indefinido.

| Estado | Condição | Consequência |
|---|---|---|
| **Atendido** | todos os elementos satisfeitos | não obstrui o compromisso |
| **Condicionado** | núcleo satisfeito, subsiste obrigação acessória | compromisso admissível, com pendência rastreada, dono e prazo |
| **Não atendido** | qualquer elemento essencial insatisfeito | compromisso obstruído, sem compensação |

Desvio de portão exige justificativa escrita em seção própria do Documento de Entrada, no
mesmo espírito do *Complexity Tracking* do spec-kit: a exceção é registrada, tem instância
superior nomeada e critério de interrupção, e **não altera o resultado registrado**.

---

## 6. Pré-condição do cliente não é escopo nosso

O mapa de pré-condições do FMO lista o que precisa existir antes da automação ou da IA — dado
organizado, processo documentado, papéis definidos, acesso concedido, decisão tomada. Absorver
isso sem precificar é o mecanismo pelo qual o prazo estoura: a entrega fica parada esperando
algo que ninguém se comprometeu a fazer.

Cada pré-condição recebe um de três destinos, e só três:

1. **Obrigação do cliente** — dono nomeado, prazo, consequência declarada do descumprimento.
2. **Item de escopo precificado** — a Thronus faz, e está no preço e no prazo.
3. **Exclusão declarada** — não será feito, e a consequência para o resultado está escrita.

Pré-condição sem destino reprova G3.

---

## 7. Profundidade proporcional à criticidade

O Discovery não tem tamanho fixo. O princípio é o do DO-178C e da IEC 61508: **a criticidade
classificada determina quais objetivos se aplicam**, e o custo cresce com ela — em aviação, um
sistema no nível mais alto custa da ordem de três vezes o do nível seguinte. Rigor uniforme é
desperdício em um extremo e negligência no outro.

| Nível de garantia | Profundidade do Discovery |
|---|---|
| **G1 — operacional** | modelagem leve, EARS só nos requisitos de fronteira, qualidade nas características aplicáveis |
| **G2 — material** | modelagem completa, EARS em todos os requisitos, COSMIC medido, qualidade nas nove características |
| **G3 — institucional** | tudo de G2, mais análise de consequência por processo funcional, evidência documental das pré-condições e portão com signatário nomeado por instância superior |

**O critério de parada é a largura da banda, não a completude do documento.** Levanta-se até
poder comprometer preço e prazo no extremo conservador. Depois disso, continuar consome margem
para reduzir incerteza que já não muda a decisão.

Seção sem consumidor declarado não se produz.

---

## 8. O que o Documento de Entrada parametriza na TCA

| Saída do Discovery | Consome na TCA |
|---|---|
| Tamanho em CFP e contextos delimitados | `perfil` e a decomposição inicial em Micro Specs |
| Tipo de produto | quais eixos de `requisitos_do_produto` existem |
| Nível de garantia | limiares dos eixos e quais portões operam |
| Requisitos de qualidade em ISO 25010 | valores de `requisitos_do_produto` e esqueleto de `verificacoes` |
| Requisitos EARS, identificados como `UC-NN` e `RN-NN` | universo de `comandos.listar_requisitos`, que torna a cobertura de requisito calculável em `tca trace`, e os cenários do `[ESTADO_RED]` |
| Registro de decisão e restrições | o que o `[ESTADO_ARCHITECTURE]` precisa responder |

Nas Etapas 1 e 2 o destino é a implantação, não a TCA. O documento é o mesmo; seção não
aplicável se declara como tal.

---

## 9. Invariantes

- **Maturidade não estima tamanho.** Informa risco e pré-condição. Tamanho se mede em COSMIC.
- **Requisito fora dos cinco padrões EARS não é requisito** — é intenção.
- **Compromisso no extremo conservador da banda.** O otimista é calibração (FMO §4.3).
- **Evidência acima de intenção declarada.** Na dúvida, o nível inferior.
- **Pré-condição do cliente tem dono nomeado, prazo e consequência.**
- **Ambiguidade é artefato contável e bloqueante**, nunca premissa silenciosa.
- **Rigor proporcional à criticidade**, não uniforme.
- **Portão não compensatório.** Nenhuma dimensão compensa a ausência de outra.
