# Discovery Thronus — Método PONTE

> **Conteúdo canônico.** Método de campo para entrar em micro, pequena e média empresa de
> baixa maturidade, mapear o processo que não existe documentado, medir onde está a perda,
> decidir a natureza de cada intervenção e comprometer um programa de evolução.
>
> A saída **não é a especificação de um sistema**. É um **programa sequenciado de
> intervenções heterogêneas** — eliminação, padronização, capacitação, integração, automação,
> agente, painel, API, sistema — dentro da linha de serviços da Thronus.
>
> Versão 3.0 · Agosto de 2026

---

## 1. Âncoras metodológicas

| Fase | Instrumento | Âncora |
|---|---|---|
| Mapear o processo | **Gemba** — ir ver onde o trabalho acontece | Sistema Toyota de Produção |
| Mapear o processo | **Domain Storytelling** — atores, objetos de trabalho, atividades | Hofer & Schwentner |
| Delimitar o levantamento | **SIPOC** — fornecedor, entrada, processo, saída, cliente | Seis Sigma |
| Medir a perda | **Mapa de Fluxo de Valor** — tempo de atravessamento *versus* tempo de processamento | Lean |
| Decidir a intervenção | **ESIA** — eliminar, simplificar, integrar, automatizar, nesta ordem | Peppard & Rowland (1995) |
| Sustentar a mudança | **ADKAR** — consciência, desejo, conhecimento, habilidade, reforço | Prosci |
| Medir a capacitação | **Kirkpatrick** — reação, aprendizado, **comportamento**, resultado | Kirkpatrick |
| Prontidão e não compensação | seis saídas do §4.6, banda, nível conservador, três gates | **FMO AI-First v4.1** |
| Protocolo de portão | três estados, signatário nomeado, não compensação | **ÂNCORA** |
| Especificar o que vira software | EARS · COSMIC ISO/IEC 19761 · ISO/IEC 25010:2023 · ISO/IEC/IEEE 29148 | ver `DOCUMENTO_DE_ENTRADA.md` |

---

## 2. Posição na cadeia

```
Etapa 0 — Diagnóstico AI-First (FMO)   prontidão do cliente, oportunidades identificadas
        ↓  seis saídas do §4.6
DISCOVERY (PONTE)                       campo → programa de intervenções comprometido
        ↓  Programa · Documento de Entrada (só para o que vira software)
Etapas 1 a 4                            automação · operações · produto · growth
```

O FMO diz **onde a empresa está**. O Discovery diz **o que fazer, em que ordem, de que
natureza, a que custo**. Só parte disso é software — e essa parte segue para a TCA.

---

## 3. Premissa de campo

Em MPME de baixa maturidade, o processo **não existe documentado e não é descrito com
fidelidade por quem não o executa**. Quem descreve de cima descreve o processo como deveria
ser. Por isso o levantamento é presencial, com quem faz, e o registro é do que se observou —
não do que se afirmou. É a mesma regra do FMO: evidência atual acima de intenção declarada.

Infraestrutura ausente e governança fraca não são obstáculo ao levantamento — são **achado**.
Aparecem como pré-condição no programa, com dono e prazo, nunca como escopo nosso silencioso.

---

## 4. As cinco fases

### P — Processo mapeado

Delimitar com **SIPOC** em uma página: quem fornece, o que entra, que processo, o que sai,
quem recebe. Serve para saber onde o levantamento começa e termina, e cabe na conversa com o
dono do negócio.

Ir a campo — **Gemba**. Observar o trabalho onde ele acontece, com quem o executa.

Registrar com **Domain Storytelling**: atores, objetos de trabalho e atividades, em linguagem
pictográfica e vocabulário do cliente. Funciona com quem não fala notação de processo, que é a
regra em MPME. A história é lida de volta para quem a executa, e a correção dele é a validação.

Saída: processo **como ele é hoje**, glossário do vocabulário do cliente, sistemas e planilhas
realmente em uso, e quem depende de quem.

### O — Oportunidade medida

**Mapa de fluxo de valor** sobre o processo mapeado: tempo de atravessamento contra tempo de
processamento, espera, retrabalho, redigitação, aprovação parada, informação transportada à mão.

**Oportunidade sem número não é oportunidade.** Onde não há dado — que é o caso normal —
mede-se por amostragem no campo e declara-se o método e o tamanho da amostra. A medida aqui é
o **baseline** do plano de validação e o que provará, depois, que a entrega gerou resultado.

### N — Natureza da intervenção decidida

Cada oportunidade recebe uma natureza, na ordem **ESIA** estendida, e a ordem é obrigatória:

| Ordem | Natureza | Pergunta |
|---|---|---|
| 1 | **Eliminar** | esta atividade precisa existir? |
| 2 | **Simplificar / padronizar** | o que sobrou pode ser mais simples e ter um procedimento único? |
| 3 | **Integrar** | o que já existe pode conversar, dispensando redigitação? |
| 4 | **Automatizar** | a rotina estável pode rodar sozinha, sem IA? |
| 5 | **Assistir com IA** | o que resta exige julgamento que um agente pode apoiar? |
| 6 | **Construir** | falta capacidade que não existe pronta no mercado? |

Transversal a todas: **Capacitar**. Em baixa maturidade, intervenção que a equipe não sabe
operar não se sustenta — e volta como retrabalho nosso.

**Não se automatiza o que deveria ser eliminado.** Pular a ordem é o erro que transforma
processo ruim em processo ruim mais caro e mais rápido. Saltar uma etapa exige justificativa
escrita no programa.

O catálogo de naturezas, com o artefato mínimo de cada uma, está em `INTERVENCOES.md`.

### T — Trilha sequenciada

Ordenar as intervenções em um **programa**, respeitando dependências que não se negociam:

- não se mede o que não está definido;
- não se automatiza o que não está estável;
- não se constrói sobre dado que não existe;
- não se entrega ao usuário o que ele não sabe operar.

As pré-condições do mapa do FMO entram na trilha como itens com dono, prazo e consequência.
A trilha atravessa as etapas do portfólio: um mesmo programa pode ter item de Etapa 1 e de
Etapa 3, com a ordem determinada pela dependência, não pelo valor do contrato.

**Adoção é item de trilha, não torcida.** Onde Receptividade ou Qualificação estão baixas no
FMO, o programa carrega itens de **ADKAR** — consciência e desejo antes de conhecimento e
habilidade — e a capacitação é avaliada no **nível de comportamento de Kirkpatrick**: mudou o
que a pessoa faz, não se ela gostou do treinamento.

### E — Entrada comprometida

Cada item da trilha recebe o **artefato mínimo da sua natureza** (`INTERVENCOES.md`). Os itens
de natureza *Construir* — e as automações, agentes, integrações e painéis que virarem software —
recebem o **Documento de Entrada**, que parametriza a TCA.

Passar pelos portões (§5), colher assinatura, emitir o **Programa** (`PROGRAMA.md`).

---

## 5. Portões não compensatórios

Protocolo do FMO §4.5 e do `tca gate`: três estados, mudança privativa de responsável nomeado,
com data, evidência consultada e justificativa.

| Portão | Pergunta de decisão |
|---|---|
| **G1 — Processo compreendido** | O processo foi observado no campo, registrado em linguagem do cliente e **validado por quem o executa**. |
| **G2 — Perda medida** | Cada oportunidade tem número, com método e amostra declarados, e o baseline está registrado. |
| **G3 — Natureza justificada** | Cada intervenção declara a sua natureza, e todo salto na ordem ESIA tem justificativa escrita. |
| **G4 — Pré-condições assumidas** | Cada pré-condição tem dono **do lado do cliente**, prazo e consequência declarada. |
| **G5 — Programa dimensionado** | Cada item tem unidade de dimensionamento da sua natureza, banda de esforço e compromisso no extremo conservador. |

**Não compensação.** Perda bem medida não compensa processo mal compreendido. Precisão de
estimativa não compensa natureza mal escolhida.

| Estado | Condição | Consequência |
|---|---|---|
| **Atendido** | todos os elementos satisfeitos | não obstrui o compromisso |
| **Condicionado** | núcleo satisfeito, subsiste obrigação acessória | compromisso admissível, com pendência rastreada, dono e prazo |
| **Não atendido** | qualquer elemento essencial insatisfeito | compromisso obstruído, sem compensação |

Exceção só por instância superior à do avaliador, com fundamento, responsável e critério de
interrupção registrados. A exceção é documentada e **não altera o resultado**, que permanece
como não atendido.

---

## 6. Pré-condição do cliente não é escopo nosso

Baixa maturidade produz pré-condições: dado a organizar, papel a definir, acesso a conceder,
decisão a tomar. Absorver isso sem precificar é o mecanismo pelo qual o prazo estoura — a
entrega fica parada esperando algo que ninguém assumiu.

Cada pré-condição recebe um de três destinos, e só três:

1. **Obrigação do cliente** — dono nomeado, prazo, consequência declarada do descumprimento.
2. **Item de programa precificado** — a Thronus faz, e está no preço e no prazo.
3. **Exclusão declarada** — não será feito, e a consequência para o resultado está escrita.

Pré-condição sem destino reprova G4.

---

## 7. Profundidade proporcional

O Discovery não tem tamanho fixo. Profundidade proporcional ao nível de garantia e ao tamanho
do programa, no princípio do DO-178C: **a criticidade classificada determina quais objetivos se
aplicam**. Rigor uniforme é desperdício num extremo e negligência no outro.

**O critério de parada é a largura da banda, não a completude do documento.** Levanta-se até
poder comprometer preço e prazo no extremo conservador. Depois disso, continuar consome margem
para reduzir incerteza que já não muda a decisão.

Seção sem consumidor declarado não se produz.

---

## 8. Invariantes

- **O processo é observado, não relatado.** Validação é de quem executa.
- **Oportunidade sem número não é oportunidade.**
- **A ordem ESIA é obrigatória.** Não se automatiza o que deveria ser eliminado.
- **Capacitação é item de trilha e se mede em comportamento**, não em satisfação.
- **Maturidade não estima tamanho.** Informa risco e pré-condição.
- **Pré-condição do cliente tem dono nomeado, prazo e consequência.**
- **Compromisso no extremo conservador da banda** (FMO §4.3).
- **Portão não compensatório.**
- **Nem toda intervenção é software.** A que for segue para a TCA; as demais têm artefato próprio.
