# Pesquisa: Linguagem mais empregável para estágio/júnior de TI

Ticket: [02-linguagem-mais-empregavel](../issues/02-linguagem-mais-empregavel.md)
Data da pesquisa: **2026-08-14**
Perfil-alvo: estágio/júnior, Brasília/DF presencial-híbrido + remoto Brasil, qualquer área de TI.

> **Aviso de validade.** Todo número aqui tem data. Os dados de pesquisa (Stack Overflow, Código Fonte) são de 2025–2026 e envelhecem devagar. As contagens de portal são snapshots e envelhecem em semanas — trate-as como ordem de grandeza, não como medida. Confiança marcada em cada bloco.

---

## Resumo executivo

1. **O mercado profissional brasileiro é muito mais Java/C# do que as pesquisas globais sugerem.** Na maior pesquisa dev BR datada (Código Fonte 2026, 17.046 respondentes), a linguagem principal é Java 16,5% e C# 14,6% — acima de TypeScript, Python e JavaScript. Os frameworks líderes são Spring Boot (14,1%) e .NET (13,7%). Isso é o inverso do ranking global do Stack Overflow.
2. **O recorte Brasília/DF confirma a hipótese, mas por um caminho diferente do esperado.** O DF **não** tem uma fatia desproporcional das vagas Java do país (~2% do total nacional, mesma proporção que Python e JavaScript). O que o DF tem é uma **composição de empregadores** dominada por consultorias/fábricas de software que atendem órgãos federais, e essas empresas pedem **Java + Spring + Angular** ou **.NET + Angular** de forma quase monolítica. A tese "DF puxa Java/.NET" se confirma no nível de *quem contrata e o que a vaga exige*, não no nível de *volume relativo*.
3. **Python tem o maior volume bruto de vagas no DF** — mas por um motivo que não é desenvolvimento backend. Python no DF aparece em vagas de dados/BI/automação/analista, não em fábrica de software. Como o escopo do mapa é "qualquer área de TI", isso conta a favor dele.
4. **Recomendação: Python (+ SQL) para escrever o bot.** É a interseção entre o maior pool bruto do DF em todas as áreas de TI e o menor atrito para um primeiro projeto digitado à mão. O gap de empregabilidade em Java/Spring — que é real para vagas de *dev* no DF — se fecha com um **segundo** projeto, não trocando a linguagem deste.
5. **O custo dessa escolha está explicitado na seção 5.** Em resumo: perde-se o casamento por keyword com a vaga mais numerosa de dev do DF (Java/Spring), e perde-se contato com tipagem estática/build system/ecossistema corporativo.

---

## 1. Demanda real por linguagem no Brasil

### 1.1 Pesquisa Código Fonte 2026 — fonte primária BR, a mais relevante aqui

- **Fonte:** [pesquisa.codigofonte.com.br/2026/ranking](https://pesquisa.codigofonte.com.br/2026/ranking)
- **Coleta:** 23/02/2026 a 09/06/2026. **17.046 participantes.** Tratamento de dados por Tiago Tomazetti.
- **Confiança:** alta para "o que devs BR usam no trabalho"; média para "o que o mercado abre de vaga" (é autodeclaração de quem já está empregado, viesada para quem segue o Código Fonte TV).

Linguagem principal declarada:

| # | Linguagem | % |
|---|-----------|-----|
| 1 | Java | 16,5% |
| 2 | C# | 14,6% |
| 3 | TypeScript | 14,1% |
| 4 | Python | 13,8% |
| 5 | JavaScript | 11,7% |
| 6 | PHP | 9,8% |
| 7 | Go | 2,4% |
| 8 | Kotlin | 2,3% |
| 9 | Dart | 1,8% |
| 10 | Delphi | 1,5% |

Frameworks/ferramentas: **Spring Boot 14,1%**, **.NET 13,7%**, React 7,6%.

> **Leitura.** Java + C# somam 31,1% — quase um terço do mercado dev brasileiro empregado. JS + TS somam 25,8%. Python sozinho, 13,8%. O ecossistema corporativo brasileiro (banco, seguradora, governo, consultoria) é o que sustenta esse número, e ele é o empregador típico de júnior no Brasil.

### 1.2 Stack Overflow Developer Survey 2025 — contraponto global

- **Fonte:** [survey.stackoverflow.co/2025/technology](https://survey.stackoverflow.co/2025/technology) — publicada em 2025, amostra global.
- **Confiança:** alta para tendência global; **baixa para o mercado BR de estágio** — a amostra é dominada por EUA/Europa e por devs seniores/hobbyistas.

| Todos os respondentes | % | Quem está aprendendo a programar | % |
|---|---|---|---|
| JavaScript | 66,0% | Python | 71,8% |
| HTML/CSS | 61,9% | HTML/CSS | 66,6% |
| SQL | 58,6% | JavaScript | 62,8% |
| Python | 57,9% | C | 48,0% |
| Bash/Shell | 48,7% | Bash/Shell | 47,0% |

Python subiu **+7 pontos percentuais** de 2024 para 2025 e é a linguagem que mais devs querem aprender.

> **Leitura.** Essa pesquisa é a razão pela qual quase todo conteúdo em português repete "JavaScript e Python lideram". Para o mercado brasileiro de contratação isso é enganoso: a Código Fonte 2026 mostra a realidade local, e ela é outra. **Não use o Stack Overflow como base para decidir empregabilidade no DF.**

### 1.3 Nota sobre SQL

SQL aparece em 58,6% dos respondentes do Stack Overflow 2025 e é requisito quase universal nas vagas de estágio de TI no DF (dev, dados, BI, suporte). **SQL não é uma alternativa às linguagens acima — é aditivo obrigatório.** Qualquer que seja a escolha, o projeto deve exercitar SQL de mão própria.

---

## 2. Recorte Brasília/DF

### 2.1 Contagens diretas em portais

**Metodologia e sua limitação — leia antes de usar os números.** Tentei contagem direta em seis portais. Catho e Adzuna retornaram HTTP 403 a acesso automatizado. Indeed não expõe total. Vagas.com retornou contagem inconsistente (1 vaga para "java em brasilia", claramente um filtro estrito de título). Só **LinkedIn (busca pública)** e **Glassdoor** produziram totais declarados. Os números do Glassdoor abaixo vêm de títulos de páginas indexadas — **a data exata do snapshot é desconhecida (indexação recente, provavelmente 2026-H1)**. **Confiança: baixa em valor absoluto, média em razão entre linguagens.**

*Ironia registrada: a dificuldade de contar vagas nesses portais é exatamente o problema que este projeto vai resolver. Depois que o bot rodar por algumas semanas, ele produz um dado melhor que qualquer coisa desta seção.*

**Glassdoor — Brasília/DF, sem filtro de senioridade** (snapshot indexado, ~2026):

| Termo | Vagas DF | Vagas Brasil | DF / Brasil |
|---|---|---|---|
| python | 111 | ~3.995–4.347 | ~2,7% |
| java | 61 | 2.759 | ~2,2% |
| javascript | 57 | 2.256 | ~2,5% |
| net (.NET) | 27 | — | — |
| desenvolvedor net | 16 | 588 | ~2,7% |
| php | 16 | 364 (desenvolvedor php) | ~4,4% |
| programador (geral) | 188 | — | — |

**Glassdoor — DF, recorte júnior/estágio:**

| Termo | Vagas DF |
|---|---|
| estágio ti | 41 |
| estagiário de ti | 21 |
| estágio em software | 16 |
| desenvolvedor júnior | 13 |
| estágio em programador | 11 |
| programador júnior | 10 |
| junior javascript | 5 |

**LinkedIn busca pública — Brasília, filtro estágio+entry-level (`f_E=1,2`), consultado em 2026-08-14:**

| Termo | Vagas |
|---|---|
| Java | 9 |
| Python | 4 |
| JavaScript | 3 |
| C# | 3 |
| .NET | 3 |
| TypeScript | 2 |

*Ressalva forte: o LinkedIn público retornou os mesmos totais com e sem o filtro de senioridade, o que sugere cache ou truncamento. Use só a ordenação, não os valores.*

Outros pontos indexados para DF: **55 vagas de "Desenvolvedor Java" em Brasília** (LinkedIn), **34 vagas de "programador java" no Distrito Federal** e **43 no Centro-Oeste** (Adzuna, snapshot rotulado maio/2026), **61 vagas de "java"** (Glassdoor).

### 2.2 O que os números dizem — e o que eles escondem

**A tese "DF puxa Java/.NET" NÃO se confirma em volume relativo.** O DF fica em ~2–3% do total nacional para *todas* as linguagens. Não há concentração estatística de Java em Brasília nesses dados.

**Mas ela se confirma em composição de empregador e em requisito de vaga.** Os empregadores que aparecem repetidamente nas buscas de dev em Brasília são consultorias/fábricas de software de perfil govtech:

- **Basis Tecnologia** (DF/BH/SP, fundada 2010) — micro-serviços com **Spring Cloud + Angular**.
- **Engesoftware** (Brasília, desde 1995) — **Java, Quarkus, Angular, Git**.
- **Mirante Tecnologia** — **.NET, Angular, AWS, Postgres**.
- **Implanta Informática**, **Place Tecnologia**, **DATAEASY**, **Global HITSS**, **Portal de Compras Públicas**, **Logiks**, **CTIS/Indra** — mesma família: sistemas corporativos para órgãos, front Angular, back Java ou .NET.

E o lado da demanda pública reforça:

- **Dataprev** abriu edital de fábrica de software de R$ 14,41 mi cujo **lote principal — R$ 11,69 mi — é explicitamente "Desenvolvimento de Sistemas Transacionais com tecnologia Java"** ([Convergência Digital](https://www.convergenciadigital.com.br/)). O contrato define a stack que a consultoria vai contratar.
- **Serpro** (sede em Brasília) padronizou desenvolvimento em **Java/Spring**; o framework **Demoiselle**, integralmente em Java, foi adotado pelo governo federal como base padrão para contratação de software na Administração Pública ([serpro.gov.br](https://www.serpro.gov.br/)). Decisão antiga, mas o legado que ela criou é o que está em manutenção hoje.

**Conclusão do recorte DF:** para vaga de **desenvolvedor** no DF, Java/Spring é o alvo #1 e .NET o #2 — não porque haja mais vagas Java em Brasília do que no resto do país, mas porque *as vagas de dev que existem em Brasília são majoritariamente dessa família*, e porque a estabilidade do contrato público faz essas stacks não rotacionarem.

**Contudo:** Python lidera o volume bruto no DF (111 vs 61). Inspecionando as vagas, elas são de **dados, BI, automação, análise** — "desenvolvimento de rotinas e sistemas de informação usando Python e SQL", analista de dados, engenheiro de software com Power BI/Qlik + scripts Python. Órgão público federal gera muita demanda de dado e automação, não só de sistema transacional. **Como o escopo do mapa é "qualquer área de TI", esse pool conta.**

---

## 3. Encaixe com o projeto (bot: HTTP → parse → dedup → SQLite/Postgres → Telegram, em CI grátis)

Nenhuma é descartada. O que muda é o atrito por etapa. Avaliação por conhecimento de ecossistema, confiança alta.

| | **Python** | **TypeScript/Node** | **Java** | **C#/.NET** |
|---|---|---|---|---|
| **HTTP + JSON** | `httpx`/`requests` — trivial | `fetch` nativo — trivial | `HttpClient` (JDK 11+) — ok, verboso | `HttpClient` — ok |
| **Parse de HTML** | `BeautifulSoup`/`lxml` — o melhor do mercado | `cheerio` — bom | `jsoup` — excelente, subestimado | `HtmlAgilityPack` / `AngleSharp` — bom |
| **Navegador headless** | `playwright-python` — ótimo | Playwright (nativo, é a casa dele) — ótimo | Playwright-java — funciona, menos exemplos | Playwright .NET — funciona |
| **SQLite** | `sqlite3` **na stdlib**, zero dependência | `better-sqlite3` (binário nativo, complica CI) ou `node:sqlite` | JDBC + driver, boilerplate | `Microsoft.Data.Sqlite` — ok |
| **Postgres** | `psycopg` — ótimo | `pg` / `postgres.js` — ótimo | JDBC — ótimo | Npgsql — ótimo |
| **Telegram** | `python-telegram-bot` — maduro, ou HTTP puro (a API é 1 POST) | `grammY`/`telegraf` — maduros | `TelegramBots` — ok | `Telegram.Bot` — ok |
| **CI grátis (GitHub Actions)** | preinstalado no runner, `setup-python` é rápido, sem build step | preinstalado, mas exige decidir tsconfig/ESM/build | `setup-java` + Gradle/Maven: build e cache pesam no cron diário | `setup-dotnet` + restore/build, idem |
| **Atrito total p/ este projeto** | **mais baixo** | baixo | médio-alto | médio-alto |

**Observação importante para o escopo do mapa:** a API do Telegram é um HTTP POST com JSON. **Nenhuma linguagem precisa de biblioteca de bot.** Escrever a chamada à mão é, inclusive, mais didático — e a regra "primeira vez é sua" favorece isso.

**Ponto contra Java neste projeto especificamente:** um cron diário que roda 30 segundos paga o preço de JVM startup + build no CI toda vez. Não é bloqueante no free tier, mas é atrito real repetido 365 vezes.

**Ponto contra TypeScript neste projeto especificamente:** antes de escrever a primeira linha útil, você precisa decidir `tsconfig`, ESM vs CJS, runner (`tsx`/`node --strip-types`/build), e `better-sqlite3` é módulo nativo que pode exigir toolchain no runner. Para quem nunca digitou código sozinho, isso é meia sessão gasta em cerimônia antes do primeiro `console.log`.

---

## 4. Sinal de portfólio: o mesmo bot em Python vs TypeScript vs Java

**Confiança: média.** Não há pesquisa datada sobre percepção de recrutador BR por linguagem de projeto pessoal; o que segue é inferência a partir de como as vagas listadas acima são escritas.

**Onde a linguagem importa muito:** no **filtro por keyword**. Vaga de estagiário em fábrica de software do DF cujo texto diz "conhecimento básico em Java e Spring Boot" (encontrado literalmente nas vagas de estágio DF indexadas) é triada por keyword antes de qualquer humano ler. Um projeto em Java no GitHub casa; um em Python não casa. Isso é mecânico e é o argumento mais forte a favor de Java aqui.

**Onde a linguagem importa pouco:** na **conversa técnica**. O que diferencia esse bot de um projeto de curso não é a linguagem — é:

- deduplicação com chave estável (o que identifica "a mesma vaga" em dois portais?),
- persistência e detecção de delta entre execuções,
- tratamento de "coletei 0 vagas: quebrou ou não teve?",
- agendamento e idempotência,
- rodar de graça, sozinho, todo dia, sem babá.

Isso é engenharia, e um entrevistador de estágio que sabe o que pergunta vai perguntar sobre isso. Um que não sabe vai olhar a linguagem. **Você não controla qual dos dois te entrevista — mas controla o filtro anterior, que é sempre por keyword.**

**Diferença de sinal por linguagem:**

| Linguagem do bot | O que sinaliza | Para quem casa |
|---|---|---|
| **Python** | automação, dados, scripting, "resolve problema" | estágio de dados/BI/automação/infra no DF (o maior pool bruto), qualquer vaga que diga "Python e SQL" |
| **TypeScript** | web moderno, full-stack | remoto Brasil em startup/produto — o maior pool júnior remoto do país |
| **Java** | encaixe direto na vaga corporativa/govtech | fábrica de software DF — o maior pool de **dev** presencial no DF |
| **C#/.NET** | idem Java, pool DF um pouco menor | consultorias .NET do DF (Mirante, Engesoftware et al.) |

Nenhuma dessas é "a mesma coisa". Elas apontam para **três mercados diferentes**, e a pergunta "qual me torna mais empregável" só tem resposta depois de escolher o mercado.

---

## 5. Recomendação

### Recomendo **Python + SQL** para escrever o bot.

**Fundamentação:**

1. **É o maior pool bruto do DF quando o escopo é "qualquer área de TI"** — 111 vagas vs 61 de Java no snapshot Glassdoor DF — porque cobre dados, BI, automação e infra, além de dev. O mapa explicitamente inclui essas áreas.
2. **É o menor atrito para um primeiro projeto digitado à mão** — e essa é a variável dominante, porque o mapa diz que *o aprendizado é a digitação*. `sqlite3` na stdlib, sem build step, sem tsconfig, sem Gradle, preinstalado no runner do GitHub Actions. O tempo economizado em cerimônia vai para dedup e persistência, que é onde está o aprendizado real.
3. **Python + SQL é o par que aparece literalmente no texto das vagas do DF** ("desenvolvimento de rotinas e sistemas de informação utilizando Python e SQL"), inclusive em vagas de órgão.
4. **Não fecha nenhuma porta.** Python é o segundo idioma quase universal: mesmo nas fábricas Java do DF, automação e teste rodam em Python.

### Custo explícito desta escolha

Sendo honesto, isso é o que você paga:

- **Você não casa por keyword com a vaga de dev mais numerosa de Brasília.** Fábrica de software govtech pede Java+Spring+Angular ou .NET+Angular. Seu portfólio não vai bater nesse filtro. Isso é uma perda real, não hipotética — a Código Fonte 2026 mostra Java 16,5% + C# 14,6% = 31,1% do mercado empregado nacional, e no DF a concentração de empregador nessa família é maior ainda.
- **Você não exercita tipagem estática, build system, nem injeção de dependência** — que é o vocabulário da entrevista corporativa brasileira.
- **Mitigação obrigatória, não opcional:** se a meta for vaga de **dev** no DF, o **segundo** projeto tem que ser Java/Spring Boot (ou .NET). Este ticket não deve ser lido como "Python resolve"; deve ser lido como "Python para este bot, Java para a próxima entrega". Registre isso no mapa antes que vire esquecimento.

### Custo das alternativas, se você discordar

**Se escolher Java/Spring Boot para o bot:**
- *Ganha:* casamento direto com o alvo #1 de dev no DF; um projeto Java real vale mais que um curso de Java; o `jsoup` é ótimo e o Postgres via JDBC é sólido.
- *Paga:* a rampa mais íngreme possível para quem nunca digitou código sozinho — Maven/Gradle, JVM, classpath, tipos, tudo antes do primeiro parse funcionar. Risco alto de o projeto morrer na cerimônia em vez de morrer na parte interessante. E CI mais lento e mais caro em minutos no free tier. Se você escolher isso, **reduza o escopo do v1** (uma fonte, sem headless) para compensar.

**Se escolher TypeScript para o bot:**
- *Ganha:* o maior pool **júnior remoto do Brasil** (JS+TS = 25,8% na Código Fonte 2026, e TS sozinho já passou Python); Playwright é nativo do ecossistema; tipagem estática sem o peso da JVM — um bom meio-termo entre Python e Java.
- *Paga:* meia sessão de cerimônia de configuração antes da primeira linha útil; `better-sqlite3` é módulo nativo e pode dar dor no runner de CI; e **abandona o recorte DF presencial** — TS praticamente não aparece nas fábricas govtech de Brasília (2 vagas no snapshot LinkedIn DF entry-level, 57 no Glassdoor DF contra 61 de Java com empregadores muito diferentes).

**Se escolher C#/.NET:** mesmo perfil de Java (14,6% nacional, forte no DF), ecossistema de scraping menor, e menos material de aprendizado em português para iniciante. Só faz sentido se você já tiver um alvo .NET específico em Brasília.

---

## 6. O que este ticket NÃO resolveu

- **Contagem confiável de vagas por linguagem no DF.** Portais bloqueiam automação (403) ou não expõem total. Os números aqui são snapshots indexados de data imprecisa. **O próprio bot é o instrumento que corrige isso** — depois de 4 semanas de coleta, você terá um dado datado, seu, e melhor que tudo nesta página. Vale reabrir este ticket com dados próprios.
- **Recorte por senioridade nas pesquisas.** A Código Fonte 2026 segmenta por senioridade (Estágio/Júnior/Pleno/Sênior) na seção de remuneração, mas **a página de ranking de tecnologias é agregada** — não dá para saber se a distribuição de linguagem entre estagiários difere da geral. Provavelmente difere (júnior entra mais em front e em automação).
- **Concursos públicos do DF.** Se o alvo incluir concurso (TCDF, CLDF e outros previstos para 2026), o conteúdo programático de TI muda a conta completamente — é outro estudo, não outra linguagem. Fora do escopo deste ticket.

---

## Fontes

| Fonte | Data | Tipo | Confiança |
|---|---|---|---|
| [Pesquisa Código Fonte 2026 — Ranking](https://pesquisa.codigofonte.com.br/2026/ranking) | coleta 23/02–09/06/2026, 17.046 respondentes | Primária, survey BR | **Alta** |
| [Stack Overflow Developer Survey 2025 — Technology](https://survey.stackoverflow.co/2025/technology) | 2025, global | Primária, survey global | Alta (global) / **Baixa (BR estágio)** |
| [Glassdoor — buscas Brasília/DF e Brasil](https://www.glassdoor.com.br/) | snapshots indexados, data imprecisa (~2026-H1) | Contagem de portal | **Baixa** (absoluto) / Média (razão) |
| [LinkedIn — busca pública, Brasília, entry-level](https://www.linkedin.com/jobs/search) | consultado 2026-08-14 | Contagem de portal | **Baixa** (indícios de cache) |
| [Adzuna Brasil — Distrito Federal / Centro-Oeste](https://www.adzuna.com.br/) | snapshot rotulado maio/2026 | Contagem de portal | Baixa |
| [Serpro — Demoiselle / padronização Java no governo federal](https://www.serpro.gov.br/) | histórico (adoção original ~2009), legado vigente | Primária institucional | Média |
| [Convergência Digital — edital Dataprev fábrica de software R$ 14,41 mi, lote Java R$ 11,69 mi](https://www.convergenciadigital.com.br/) | data do edital não confirmada (URL original retornou 404) | Notícia setorial | **Baixa-Média** — reconfirmar antes de citar |
| [Brasscom — Perspectivas do Mercado de Trabalho TIC 2025](https://brasscom.org.br/tic-pode-gerar-ate-147-mil-empregos-formais-no-brasil-em-2025/) | 2025 | Primária setorial | Alta (macro) / não quebra por linguagem |
| Perfis de empregadores DF (Basis, Engesoftware, Mirante, Implanta, Place, DATAEASY, Global HITSS) | via descrições de vaga indexadas, ~2026 | Observacional | Média |
