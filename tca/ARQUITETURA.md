# Arquitetura de Referência

> **Conteúdo canônico.** O que **todo produto** gerado pela TCA precisa ter, expresso como
> obrigação e não como implementação — a TCA governa projetos de qualquer stack.
>
> A decisão de arquitetura (`[ESTADO_ARCHITECTURE]`) não fecha sem responder a cada
> obrigação aplicável ao perfil. Os limiares estão em `profiles/<perfil>.json →
> requisitos_do_produto`; como se verifica cada um, o projeto declara em
> `tca.project.json → verificacoes`.
>
> Isto é **feedforward**: o produto nasce com a propriedade. Portão que confere depois é o
> último recurso, não o mecanismo.

---

## 1. Controle de acesso — duas camadas

Autorização de **ação** e isolamento de **linha** são camadas distintas e ambas obrigatórias
a partir do perfil `micro`. Se o serviço esquecer um filtro, o banco ainda barra; sem a
segunda camada, um único defeito de filtro vaza a base inteira.

**Camada de aplicação — RBAC**
- Matriz papel × recurso × ação como **dado versionado**, não código espalhado.
- **Negar por padrão.** Ausência de regra é negação, nunca permissão.
- A verificação acontece na **fronteira do serviço de aplicação** — não na view, não no
  template — porque é a camada que o Port/Adapter já isola e que se testa sem HTTP.
- Permissão de **objeto** é distinta de permissão de **modelo**. A primeira é onde o
  vazamento acontece.
- Conceder papel é, ele mesmo, uma permissão, e toda concessão é registrada em trilha
  append-only.

**Camada de dados — isolamento de linha**
- Política de linha ativa **e forçada**: sem forçar, o dono da tabela ignora a política, e o
  processo da aplicação costuma ser o dono. É a falha silenciosa clássica.
- Contexto da sessão definido **por requisição e dentro da transação**, para não vazar entre
  requisições quando há pool de conexão.
- Política separada por operação, com condição de **leitura e de escrita**. Só a de leitura
  permite mover um registro para outro tenant.
- Políticas são schema: vivem em migração versionada e reversível.

**Verificação que vale é o teste negativo**: autenticado como A, tentar ler e escrever
registro de B, e exigir zero linhas ou erro. Teste positivo não prova isolamento.

---

## 2. Dependência externa — resiliência e economia

Toda dependência externa fica **atrás de um port**. O adapter é obrigado a:

| Obrigação | Por quê |
|---|---|
| **Timeout** explícito | dependência lenta não pode virar indisponibilidade própria |
| **Retry** com recuo exponencial e jitter | retry sincronizado transforma incidente em avalanche |
| **Circuit breaker** | insistir em serviço caído consome recurso e atrasa a fila |
| **Chave de idempotência** em operação não-GET retentável | retry sem ela duplica efeito |
| **Orçamento declarado** de chamadas | dependência sem teto é custo sem teto |
| **Caminho de degradação** | falha de dependência não essencial não derruba a operação |

Falha de dependência externa **nunca cascateia**: o teste de falha de dependência é
obrigatório a partir do perfil `micro`.

---

## 3. Modelo de linguagem — a dependência com custo

Um modelo é dependência externa com uma dimensão a mais: **cada chamada tem preço**. Além
de tudo da seção 2:

- **Teto por operação, por conversa e por dia.** Sem teto, um laço de agente é
  indisponibilidade e fatura no mesmo evento.
- **Corte explícito ao atingir o teto**, com caminho de degradação declarado. Falha
  silenciosa por estouro de orçamento é o pior dos mundos.
- **Cache de prefixo** onde o provedor suportar; **lote** onde a latência permitir.
- **Prompt é conteúdo metodológico**: versionado como código, com âncora em fonte canônica
  e hash. Prompt em banco ou embutido em código de aplicação não é versionado — é perdido.
- **Registro de custo por operação**, para que o orçamento seja verificável e não estimado.
- O agente **nunca executa ação irreversível sem confirmação humana explícita**, e nunca
  finge ser humano quando questionado diretamente.

---

## 4. Observabilidade

- **Log estruturado** em formato consultável. Log em texto livre não agrega, não correlaciona
  e não serve para investigar incidente.
- **Correlation ID** gerado na borda e propagado por log, trace e rastreador de erro.
- **MS-ID carimbado no release**: erro em produção passa a apontar a Micro Spec que o
  introduziu, o que torna a transição `MONITOR → TRIAGE` precisa em vez de genérica.
- **Health separando liveness de readiness**, com checagem de dependências e timeout, e
  devolvendo versão e release. `SELECT 1` não é health check.
- **Métricas de taxa, erro e duração** por operação.
- **Trilha de acesso a dado pessoal** — quem acessou qual dado de qual titular. Para cliente
  público brasileiro é exigência legal, não refinamento.

---

## 5. Desempenho e recursos computacionais

- **Contagem de consultas assertada em teste.** É a trava mais barata contra N+1, e ela
  protege para sempre: quebra quando uma operação vai de 3 para 40 consultas.
- **Paginação obrigatória** em toda coleção. Endpoint que devolve tudo funciona até o dia em
  que não funciona.
- **Cache com invalidação declarada por Micro Spec.** Sem declarar o que invalida, dado velho
  vira defeito indepurável.
- **Orçamento de desempenho por classe de operação** — leitura interativa, escrita,
  relatório, lote — e não um número único, porque limiar único produz exceção declarada em
  quase todo projeto, e exceção rotineira é o começo do portão que ninguém respeita.
- **Orçamento de carga transferida** ao cliente, verificado no build. Para rede municipal em
  conexão ruim isso é requisito de produto, não detalhe.

---

## 6. Escalabilidade

- **Trabalho pesado fora do caminho da requisição**: relatório, geração de documento e
  importação em massa vão para fila.
- **Teste de carga com volume realista** antes do go-live, a partir do perfil `standard`.
  "Funciona com 50 registros" e "funciona com 40 mil" são sistemas diferentes.
- **Pool de conexão e timeout de instrução** no acesso a dados.

---

## 7. Reversibilidade

- **Toda migração com reversão testada** — aplicar, reverter, reaplicar — no pipeline, não
  na intenção.
- **Operação destrutiva atrás de marcador de execução única**, nunca de parâmetro de
  configuração: configuração se altera por engano; marcador, não.
- **Feature flag** para Micro Spec de raio alto.

---

## 8. Estrutura e isolamento de camadas

- Domínio **não importa framework** nem biblioteca de infraestrutura.
- Aplicação **não importa persistência** diretamente — apenas os contratos declarados em
  `application/ports/`.
- Infraestrutura é o **único ponto de acesso** a ORM, cliente HTTP e qualquer I/O externo.
- Teste que depende de infraestrutura vive na camada de integração, e não na de domínio.

**Isto é verificado mecanicamente**, não revisado: o contrato de camadas é declarado e o
build quebra quando violado. Ferramenta consolidada existe em toda stack relevante —
`import-linter`, `dependency-cruiser`, `ArchUnit`, `NetArchTest`, `depguard`, `Deptrac`.
Declarar em prosa e confiar na revisão é o que produz deriva arquitetural.

---

## 9. Interface, quando existir

- Todo componente tem os **sete estados**: padrão, foco, desabilitado, carregando, erro,
  **vazio** e sem permissão. A entrega incompleta quase sempre é a que só tem o estado feliz.
- **Zero mensagem técnica** ao usuário final: toda exceção vira instrução em português.
  Nunca expor identificador interno, nome de modelo, endpoint ou código de status.
- **Acessibilidade como invariante**, verificada no build. Para contrato público brasileiro é
  exigência legal.
- **Orçamento de interação**: número máximo de passos para a tarefa mais frequente. Quando o
  diagnóstico de maturidade indica baixa qualificação digital, o orçamento aperta.

---

## 10. O que torna isto construção, e não conferência

O `[ESTADO_ARCHITECTURE]` produz o ADR **e** a lista de obrigações aplicáveis ao perfil. A
primeira Micro Spec do projeto é a **MS-000 Fundação**, cuja especificação é derivada dessa
lista: ela instala o substrato antes da primeira funcionalidade.

Nenhuma funcionalidade é construída sobre substrato ausente. É por isso que a MS-000 é
obrigatória e não recomendada — acrescentar controle de acesso ou observabilidade depois de
vinte Micro Specs é a refatoração cara que a metodologia existe para evitar.
