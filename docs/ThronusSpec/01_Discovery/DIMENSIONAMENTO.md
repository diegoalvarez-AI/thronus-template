# Discovery — Dimensionamento de Escopo, Prazo e Custo

> Tamanho por medida padronizada, rigor por criticidade classificada, esforço em banda.
> Âncoras: ISO/IEC 19761 (COSMIC) · ISO/IEC 25010:2023 · DO-178C e IEC 61508 · FMO v4.1 §4.3.

---

## 1. Três grandezas independentes

Colapsá-las num número é a origem da falha grosseira de prazo e custo.

| Grandeza | Medida por | O que decide |
|---|---|---|
| **Tamanho funcional** | COSMIC (ISO/IEC 19761), sobre o modelo da fase N | quantas Micro Specs, quanto paralelismo |
| **Tipo de produto** | natureza do que se constrói | quais características de qualidade se aplicam |
| **Nível de garantia** | consequência da falha, no princípio do DO-178C | rigor em cada característica, quais portões operam |

Atravessando as três, o **risco de execução**, que vem do FMO e alarga a banda sem alterar o
tamanho medido.

---

## 1-A. Unidade por natureza de intervenção

COSMIC mede software. O programa tem itens que não são software, e cada natureza tem a sua
unidade — declarada em `INTERVENCOES.md`:

| Natureza | Unidade |
|---|---|
| Eliminar atividade | atividades removidas |
| Padronizar procedimento | procedimentos escritos × exceções tratadas |
| Capacitar, mentorar, aculturar | turmas × comportamentos-alvo × prazo de reforço |
| Integrar sistemas existentes | pares origem-destino × campos mapeados |
| Automatizar rotina | rotinas × passos × pontos de decisão |
| Assistente ou agente simples | intenções × canais |
| Agente com autonomia | intenções × ferramentas × ações irreversíveis |
| Orquestração | fluxos × sistemas coordenados × pontos de retomada |
| Painel e indicador | indicadores × fontes distintas |
| API e sistema sob medida | processos funcionais em CFP (§2) |

A banda (§6) e o compromisso conservador valem para todas, sem exceção.

---

## 2. Tamanho de software — COSMIC, ISO/IEC 19761

COSMIC mede tamanho funcional contando **movimentos de dado** nos processos funcionais
modelados. Quatro tipos, um ponto (CFP) cada:

| Movimento | O que é |
|---|---|
| **Entry** | dado cruza a fronteira, de fora para dentro do software |
| **Exit** | dado cruza a fronteira, de dentro para fora |
| **Read** | dado é lido do armazenamento persistente |
| **Write** | dado é gravado no armazenamento persistente |

Regras do método que valem sem exceção: o escopo da medição fica **inteiramente dentro de uma
camada**; a fronteira é declarada antes de contar; cada processo funcional é disparado por um
único evento; e a contagem é do **modelo**, não da conversa.

Isto é o que substitui julgamento por medida. Um processo funcional com 3 movimentos e outro
com 40 deixam de ser ambos "média complexidade".

**O que se conta em cada etapa do portfólio:**

| Etapa | Processo funcional é | Fronteira típica |
|---|---|---|
| **1 — Automação e Agentes** | cada intenção atendida, cada rotina disparada | entre canal e automação |
| **2 — Operações Inteligentes** | cada indicador calculado, cada rotina de operação | entre fonte de dado e painel |
| **3 — Produto Digital** | cada caso de uso com gatilho único | entre usuário/sistema externo e a aplicação |

**Conversão de CFP para Micro Specs.** A razão CFP-por-MS é medida no histórico da própria
Thronus, não estipulada. Enquanto não houver série suficiente, a conversão é premissa declarada
na proposta, com a base explicitada. Lacuna conhecida, não omissão — e é o primeiro indicador a
calibrar assim que houver projetos medidos.

**Limite declarado.** COSMIC mede tamanho funcional. Não mede esforço de integração com sistema
legado mal documentado, nem trabalho de qualidade não funcional. Estes entram pela banda (§6),
não pela contagem.

---

## 3. Tipo de produto → características de qualidade aplicáveis

Recorte da ISO/IEC 25010:2023 por tipo. O que não se aplica se declara, não se omite.

| Tipo | Características em primeiro plano |
|---|---|
| `agente` | confiabilidade · segurança · *safety* (restrição operacional, falha segura, supervisão humana proporcional ao impacto) |
| `automacao` | confiabilidade (recuperabilidade, tolerância a falha) · manutenibilidade |
| `operacao` | adequação funcional (correção) · compatibilidade (interoperabilidade) · eficiência de desempenho |
| `api` | compatibilidade · manutenibilidade (modificabilidade) · segurança · flexibilidade |
| `site` | eficiência de desempenho (comportamento temporal, uso de recurso) · capacidade de interação (acessibilidade) |
| `saas` | segurança (confidencialidade, integridade, responsabilização) · flexibilidade (escalabilidade) · confiabilidade (disponibilidade) |
| `sistema` | segurança · adequação funcional · manutenibilidade · confiabilidade |

Produto que é dois tipos recebe a **união**, nunca a interseção.

---

## 4. Nível de garantia

O princípio vem do DO-178C e da IEC 61508: a criticidade é classificada a partir da
**consequência da falha**, não do tamanho, e determina quais objetivos do ciclo de vida se
aplicam. Um script pode ser G3; uma plataforma pode ser G1.

| Nível | Consequência da falha | Objetivos que passam a valer |
|---|---|---|
| **G1 — operacional** | incômodo, retrabalho interno, nada sai da empresa | rigor mínimo do perfil |
| **G2 — material** | perda financeira, perda de prazo, cliente do cliente afetado | trilha de auditoria, teste negativo de acesso, reversibilidade testada, medição das características de desempenho declaradas |
| **G3 — institucional** | dano a terceiro, sanção legal, quebra de contrato ou de edital | tudo de G2, mais retenção declarada, ensaio de restauração, análise de consequência por processo funcional e portão com signatário de instância superior |

Dado pessoal, dinheiro de terceiro ou obrigação de edital elevam a G3 independentemente de
qualquer outra consideração. A característica *Safety* da ISO 25010:2023 — identificação de
risco, falha segura, aviso de perigo, integração segura — é obrigatória a partir de G2.

---

## 5. Risco de execução — onde o FMO entra

O FMO **não estima tamanho**. Responde a: qual a probabilidade de o trabalho ser interrompido,
retrabalhado, ou de a entrega não ser adotada.

| Dimensão em nível baixo | Efeito |
|---|---|
| **Processos** | requisito instável → alarga a banda; exige reversibilidade e entrega faseada |
| **Dados** | dado real diferente do descrito → alarga a banda; gera **pré-condição**, não escopo silencioso |
| **Governança** | decisão e acesso demoram → alarga o prazo; exige decisor nomeado com prazo de resposta |
| **Qualificação** | adoção lenta → capacidade de interação sobe de prioridade; material de apoio é item precificado |
| **Receptividade** | resistência → entrega faseada; medir adoção, não só erro |

Como o nível usado é sempre o **inferior da banda** (FMO §4.3), o alargamento é conservador por
construção. Baixa maturidade não aumenta o nosso escopo por si só: gera pré-condição, com um dos
três destinos do `METODO.md` §6.

---

## 6. Banda de esforço e compromisso conservador

Esforço é **intervalo**, nunca ponto. O compromisso comercial usa o **extremo superior de
esforço** — o conservador. O otimista é calibração interna e não se comunica como prazo.

A largura é função declarada de contadores, não de sensação:

| Fator | Efeito |
|---|---|
| Itens `[A ESCLARECER]` no modelo | cada um declara o seu impacto em CFP potencial; a soma alarga |
| Dimensões do FMO em nível baixo ou em banda | alargam, por §5 |
| Confiança registrada no diagnóstico | confiança baixa alarga |
| Integração com sistema legado não documentado | alarga — COSMIC não captura (§2) |
| Precedente medido na própria Thronus | estreita |

**Critério de parada:** a banda está estreita o bastante para comprometer no extremo conservador
sem inviabilizar a proposta. Alcançado isso, para. Não alcançado, o que falta é
`[A ESCLARECER]` nomeado — e a decisão é levantar mais, reduzir escopo, ou declarar a faixa e
precificar o risco.

Os fatores devem ser **calibrados contra o histórico real** de estimado versus realizado. Até
haver série, são premissa declarada e revisável — pela mesma razão que o FMO declara que suas
faixas serão recalibradas após o piloto.

---

## 7. O que vai para a proposta

| Item | Origem |
|---|---|
| Escopo comprometido e **exclusões explícitas** | fase N e portão G2 |
| Tamanho em CFP, com fronteira e contagem auditáveis | §2 |
| Prazo e investimento | banda, no extremo conservador |
| Pré-condições do cliente com dono, prazo e consequência | mapa de pré-condições do FMO, portão G3 |
| Indicador de sucesso com baseline medido | plano de validação do FMO |
| Critérios de interrupção | plano de validação do FMO |
| Premissas declaradas e sua base | fatores de banda deste documento |

Proposta que não carrega exclusões, pré-condições e premissas não está comprometendo escopo —
está apostando nele.
