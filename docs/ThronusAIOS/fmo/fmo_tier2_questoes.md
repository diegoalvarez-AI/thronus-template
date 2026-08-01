# FMO Tier 2 — Diagnóstico AI-First: 26 Perguntas

**Formato:** múltipla escolha + conversa guiada · 60–90 minutos  
**Conduzido por:** consultor Thronus (agente IA + validação humana)  
**Scoring:** A=1 · B=2 · C=3 · D=4 · escala 1–5 por dimensão  
**Output:** `fmo_assessment.json` → alimenta TCA via `fmoToDiscoveryBridgeSkill`

---

**Instrução ao consultor:**  
As perguntas Q1–Q10 do Tier 1 são reutilizadas — se o cliente já completou o Raio-X, confirme as respostas e aprofunde com o follow-up de cada uma. Se não completou, aplique do zero. Perguntas abertas (✎) são exploradas em conversa; o consultor registra evidências concretas, não só a síntese da resposta.

---

## PROCESSOS — 6 perguntas (FP1–FP6)

### FP1 [reutilizada de Q1]
**Quando um funcionário novo entra, como ele aprende a fazer o trabalho?**  
*(opções A–D idênticas ao Tier 1)*

**Follow-up T2:** *Quem criou esse material? Quando foi a última vez que foi atualizado?*

---

### FP2 [reutilizada de Q2]
**Se você sair de férias por 2 semanas, o que acontece com as tarefas que só você (ou alguém-chave) sabe fazer?**  
*(opções A–D idênticas ao Tier 1)*

**Follow-up T2:** *Me dá um exemplo concreto de uma pessoa e uma tarefa específica que dependem dela.*

---

### FP3 — Processo comercial (✎ aberta)
**Me descreve como funciona o processo de venda da empresa — desde o primeiro contato até o pagamento recebido. O que passa pela mão de quem?**

*Guiar a conversa: existe sequência definida? tem registro em algum lugar? muda dependendo de quem está atendendo?*

*Evidências a registrar: número de etapas, ferramentas usadas em cada etapa, nomes das pessoas envolvidas*

---

### FP4 — Volume de trabalho manual (MC)
**Quanto tempo por semana você estima que a equipe gasta em tarefas repetitivas — copiar informação de um lugar para outro, enviar lembretes manualmente, preencher a mesma coisa em sistemas diferentes?**

- A — Mais de 15 horas no total da equipe *(1pt)*
- B — Entre 8 e 15 horas *(2pt)*
- C — Entre 2 e 8 horas *(3pt)*
- D — Menos de 2 horas — a maioria das repetições já foi automatizada *(4pt)*

*Proxy quantitativo para potencial de automação imediato*

---

### FP5 — Mapeamento de risco operacional (✎ aberta)
**Quais processos da empresa dependem de uma única pessoa específica? O que acontece se essa pessoa ficar indisponível por 2 semanas?**

*Registrar: nome do processo, nome da pessoa, impacto estimado*

---

### FP6 — Histórico de melhoria de processo (✎ aberta)
**Nos últimos 6 meses, mudaram a forma de fazer algum processo importante? O que motivou? Como foi a adaptação da equipe?**

*Avaliar: capacidade de mudança interna · velocidade de adaptação · motivadores de melhoria*

---

## DADOS — 5 perguntas (FD1–FD5)

### FD1 [reutilizada de Q3]
**Se eu te pedir agora os clientes que mais compraram nos últimos 3 meses, como você me mostraria? Em quanto tempo?**  
*(opções A–D idênticas ao Tier 1)*

---

### FD2 [reutilizada de Q4]
**Como você acompanha se o negócio está indo bem ou não nesse mês?**  
*(opções A–D idênticas ao Tier 1)*

---

### FD3 — Fragmentação de dados (MC)
**Onde ficam guardadas as informações dos seus clientes? Se eu precisar do histórico completo de um cliente, quantos lugares diferentes você precisaria consultar?**

- A — 4 ou mais lugares (WhatsApp, caderno, e-mail, planilha, sistema...) *(1pt)*
- B — 2 a 3 lugares — daria para juntar, mas dá trabalho *(2pt)*
- C — Principalmente em 1 sistema, com alguns registros fora *(3pt)*
- D — Tudo centralizado — histórico completo em um lugar só *(4pt)*

*Fragmentação de dados de cliente · custo de integração*

---

### FD4 — Integração de fluxo de informação (MC)
**Quando uma venda é fechada, a informação chega automaticamente para quem precisa saber — financeiro, estoque, produção, entrega — ou alguém precisa avisar manualmente?**

- A — Tudo manual — cada área precisa ser avisada separadamente *(1pt)*
- B — Parcialmente — alguns avisos são automáticos, outros manuais *(2pt)*
- C — A maioria chega automaticamente, mas ainda tem lacunas *(3pt)*
- D — Automático — uma venda dispara tudo que precisa acontecer *(4pt)*

*Integração de dados entre áreas · automação de fluxo de informação*

---

### FD5 — Decisão baseada em dados (✎ aberta)
**Me dá um exemplo de uma decisão importante que você tomou no último mês. O que você consultou antes de decidir?**

*Avaliar: uso de dados vs. intuição · quais dados existem e são consultados · presença de indicadores*

---

## GOVERNANÇA — 5 perguntas (FG1–FG5)

### FG1 [reutilizada de Q5]
**Quando acontece um erro que chega até o cliente, o que acontece depois que o problema é resolvido?**  
*(opções A–D idênticas ao Tier 1)*

---

### FG2 [reutilizada de Q6]
**Como está organizada a tomada de decisão no dia a dia da empresa?**  
*(opções A–D idênticas ao Tier 1)*

---

### FG3 — Clareza de papéis (MC)
**Se eu perguntar para qualquer funcionário da sua empresa quem é responsável por cada área principal, eles me dariam a mesma resposta?**

- A — Não — "todo mundo faz tudo" e as responsabilidades são difusas *(1pt)*
- B — Talvez — as pessoas sabem na prática, mas não está escrito *(2pt)*
- C — Provavelmente sim para as áreas principais *(3pt)*
- D — Sim — responsabilidades estão claras e documentadas para toda a equipe *(4pt)*

*Clareza de papéis e responsabilidades · maturidade de estrutura organizacional*

---

### FG4 — Segurança e controle de acesso (✎ aberta)
**Quem tem acesso a informações financeiras e de clientes da empresa? Isso é controlado de alguma forma?**

*Avaliar: controle de acesso · exposição de dados sensíveis · risco LGPD*

---

### FG5 — Compliance tecnológico (MC)
**Seus contratos com sistemas e plataformas que a empresa usa estão atualizados? Você sabe o que pode e não pode fazer com os dados que eles guardam?**

- A — Não sei — nunca li esses contratos com atenção *(1pt)*
- B — Já li alguns, mas não tenho controle sobre isso *(2pt)*
- C — Os principais estão atualizados e sei os pontos mais importantes *(3pt)*
- D — Temos processo de revisão periódica de contratos de tecnologia *(4pt)*

*Compliance tecnológico · exposição contratual*

---

## QUALIFICAÇÃO — 5 perguntas (FQ1–FQ5)

### FQ1 [reutilizada de Q7]
**Quando precisam aprender uma ferramenta nova, como costuma funcionar na sua equipe?**  
*(opções A–D idênticas ao Tier 1)*

---

### FQ2 [reutilizada de Q8]
**Hoje, alguém na sua equipe usa alguma ferramenta de inteligência artificial no trabalho?**  
*(opções A–D idênticas ao Tier 1)*

---

### FQ3 — Velocidade de adoção histórica (✎ aberta)
**Pensa na última ferramenta nova que implementaram. Quanto tempo até todo mundo usar de verdade? Quem mais ajudou nessa adaptação? Quem mais travou?**

*Registrar: tempo real de adoção, nomes/perfis de champions e resistências*

---

### FQ4 — Autonomia tecnológica (MC)
**Quando alguém da equipe tem um problema com uma ferramenta de trabalho, o que ela faz primeiro?**

- A — Para tudo e espera alguém de TI ou você mesmo resolver *(1pt)*
- B — Pede ajuda para um colega que entende mais *(2pt)*
- C — Tenta resolver sozinha primeiro, e pede ajuda se não conseguir *(3pt)*
- D — Busca a solução (vídeo, suporte, documentação) e costuma resolver sozinha *(4pt)*

*Autonomia tecnológica · dependência de suporte externo*

---

### FQ5 — Dispersão de capacidade (✎ aberta)
**Qual é a maior diferença de habilidade digital entre o funcionário mais avançado e o mais básico da equipe? Isso afeta o trabalho no dia a dia?**

*Identificar: dispersão de capacidade · impacto na operação · necessidade de nivelamento*

---

## RECEPTIVIDADE — 5 perguntas (FR1–FR5)

### FR1 [reutilizada de Q9]
**Pensa em uma mudança importante que vocês tentaram implementar nos últimos 2 anos. O que aconteceu?**  
*(opções A–D idênticas ao Tier 1)*

---

### FR2 [reutilizada de Q10]
**Como você descreveria a disposição do time para mudar a forma como trabalha?**  
*(opções A–D idênticas ao Tier 1)*

---

### FR3 — Padrão de reação à mudança (✎ aberta)
**Quando você propõe uma mudança importante para a equipe, qual é a reação típica nos primeiros dias? E depois de algumas semanas?**

*Avaliar: reação inicial vs. reação sustentada · diferença entre aceitação e adoção real*

---

### FR4 — Aprendizado organizacional sobre mudança (✎ aberta)
**O que você já aprendeu sobre o que precisa acontecer para a equipe abraçar uma mudança de verdade?**

*Extrair: sabedoria organizacional sobre gestão de mudança · fatores de sucesso já descobertos pelo dono*

---

### FR5 — Bloqueios crônicos (✎ aberta)
**Tem algum processo ou área que você já tentou mudar mais de uma vez e não conseguiu implementar de verdade? O que sempre trava?**

*Identificar: bloqueios sistêmicos · áreas de alta resistência · padrões de falha recorrentes*

---

## Scoring Tier 2

### Por dimensão (escala 1–5)
O nível é atribuído pelo consultor com base na rubrica comportamental (`fmo_rubrica.md`), não pela média matemática das opções — o consultor cruza as evidências das perguntas abertas com as respostas de múltipla escolha para determinar o nível real.

### Regras de triangulação

| Par de perguntas              | O que revelar                                      |
|-------------------------------|----------------------------------------------------|
| FP1 + FP2                     | Nível real de dependência de pessoas               |
| FD5 + Q3/Q4                   | Uso real de dados vs. intuição                     |
| FR3 + FR4                     | Diferença entre intenção e histórico real de mudança |
| FG3 + FG4                     | Clareza de papéis vs. controle efetivo de acesso   |
| FQ3 + FQ4                     | Velocidade de adoção vs. autonomia no dia a dia    |
