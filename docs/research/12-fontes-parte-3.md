# Inventário de fontes — parte 3: fontes parciais e intocadas

Ticket: [#13 — Inventário parte 3: fontes parciais e intocadas](https://github.com/luizhtmoreira/bot-estagio/issues/13) · Parte 1: [01-fontes.md](./01-fontes.md) · Parte 2: [10-fontes-parte-2.md](./10-fontes-parte-2.md) · Mapa: [issue #1](https://github.com/luizhtmoreira/bot-estagio/issues/1)
Data da apuração: **2026-08-16**. Perfil-alvo: estágio **e** júnior, qualquer área de TI, **remoto Brasil** + **presencial/híbrido em Brasília/DF**, orçamento **R$ 0/mês**.

Este ticket não bloqueia a v1 (fonte/stack/infra já decididos com Gupy). Fecha o que #11 deixou pela metade, para alimentar o roteiro de crescimento.

## Como ler este documento

Mesma convenção das partes 1 e 2:

- **[V]** — **VERIFICADO** nesta sessão, com requisição HTTP real feita por mim em 2026-08-16.
- **[P]** — **PRESUMIDO**: inferência, leitura de ToS/robots, ou conhecimento prévio. Não medi.

Onde não consegui medir algo, digo isso explicitamente e digo como mediria.

**Regra de filtro aplicada em toda medição:** todo parâmetro de filtro só é aceito como "filtrando de verdade" se a contagem mudar comparado à mesma query sem esse filtro (ou com um valor de filtro alternativo). Nome de parâmetro errado, nessas APIs, tende a ser ignorado silenciosamente em vez de dar erro — já visto no Sólides e no LinkedIn.

Escrita incremental: cada seção abaixo foi fechada e gravada em disco antes de passar para a próxima fonte, exatamente para evitar a degradação de contexto que interrompeu #11.

## Resumo executivo

- **Empregare é o achado do ticket**: API pública oficial, documentada via OpenAPI/Scalar, com servidor MCP funcional, sem login. 241 vagas de estágio no Brasil, 17 de TI (por busca textual), 7 delas em Brasília. Menor volume que Sólides/Gupy, mas a mais barata de manter de todo o inventário.
- **Remotar é o segundo achado**: API separada do front (`api.remotar.com.br`), 6.388 vagas, categorias e tags estruturadas (inclusive tag dedicada para excluir Jovem Aprendiz). 21 vagas de Programação+Estágio e 114 de Programação+Júnior, **100% remoto** — cobre exatamente o eixo mais fraco da Gupy.
- **Agiel**: as três lacunas técnicas de #11 fecharam (paginação via `onSeeMoreClick`, causa do 500 em `onCursoChange`, e confirmação de que a listagem sem login já basta para notificar). Total nacional agora conhecido: 752 vagas.
- **Companhia de Estágios**: não existe API de vagas no portal `carreira.` porque não existe função de listar vagas ali — é só formulário de cadastro. A fonte, na prática, se resume ao sitemap institucional com `lastmod` (104 programas).
- **Eureca**: os 81 programas variados por completo — só 5 são de TI, zero remotos, 1 toca Brasília.
- **Sólides**: confirmado que `occupationAreas=tecnologia` perde vaga real — achei uma vaga chamada literalmente "ESTÁGIO DE TI" categorizada como "Administrativo" na origem. Recomendação: coletar sem esse filtro e aplicar TI localmente.
- **Nube**: a discrepância de #11 (6.443 vs. 3.629) é interna à própria resposta da API — o campo de metadado `total` não bate com o array de vagas que a mesma chamada devolve. Mesma classe de armadilha do par `totalVagas`/`totalRegistro` achado na Empregare.
- **InfoJobs**: lacuna fechada — categoria estruturada "Informática, TI, Telecomunicações" (id 74) com ~110–150 vagas de estágio, das quais só 4 remotas. Armadilha de localização confirmada (`provincia` textual é ignorado, só id numérico filtra).
- **Glassdoor**: descartado com alta confiança — 403 em toda tentativa e robots explicitamente restritivo para `/Vaga/`.
- **EstágioTrainee**: não é fonte de vagas, é blog institucional (Wix Blog app) sobre processos seletivos.
- **Senado Federal e BairesDev**: nenhum vale coletor dedicado — Senado por ser edital periódico de empregador único, BairesDev por ser empregador único **e** ter perfil de contratação sênior, sem menção a estágio/júnior em toda a página de carreiras.

---

## Prioridade 1 — maior valor esperado

### Empregare — **[V] API pública oficial confirmada, documentada, com OpenAPI e servidor MCP funcional**

Esta é a fonte de maior valor esperado do ticket, e a hipótese se confirmou por completo: **não é engenharia reversa, é uma API que a Empregare oferece de propósito**.

#### robots.txt — **[V] reconfirmado**
```
User-agent: *
Content-Signal: search=yes, ai-input=yes, ai-train=no
Allow: /
Allow: /api/mcp
Allow: /api/docs
Disallow: /api/
...
Sitemap: https://www.empregare.com/pt-br/sitemap-index.xml
```
`https://www.empregare.com/robots.txt` faz **302 → `/pt-br/robots.txt`** [V], conteúdo acima obtido seguindo o redirect.

#### Documentação — **[V] Scalar/OpenAPI real, um único endpoint documentado**

`GET /api/docs` → 302 → `/api/docs/` → 200, página Scalar (viewer de OpenAPI), título *"Empregare - API de Vagas"*, com integração MCP explícita no config JS: `"mcp":{"name":"Empregare - Vagas","url":"https://www.empregare.com/api/mcp"}` [V].

A spec OpenAPI não estava em `/api/docs/openapi/v1.json` (404) como o config sugeria — achei em **`/openapi/v1.json`** (200, 13 KB) [V]. Só documenta **um endpoint**:

```
GET /api/{culture}/vagas/buscar-novo
```
Descrição oficial da própria spec: *"Buscar vagas de emprego (publico, sem login). Busca vagas ativas no jobboard publico da Empregare. Nao requer autenticacao."* [V] — a fonte se autodeclara pública, o que é raro no inventário inteiro.

**Parâmetros documentados** (23 no total) [V]: `Query` (texto livre), `Ordenacao`, `DataPublicacao` (0=qualquer, 1=24h, 2=semana, 3=mês — **filtro de recência nativo**, algo que nenhuma outra fonte do inventário tem), `Modalidade[]`, `Empresa[]`, `Nivel[]`, `Pcd`, `SelecaoCega`, `TipoRecrutamento[]` (1=Externo, 2=Misto, 3=Interno, 4=Alunos), `Pais[]`, `Estado[]`, `Cidade[]`, `Regime[]`, `SubArea[]`, `EmpresaUnidade[]`, `SomenteImpulsionadas`, `Pagina`, `ItensPagina`, `TipoProcessoSeletivo[]` (1=Padrão, 2=Edital/concurso), `culture` (path, `pt-br`/`en-us`/`es-cl`).

#### Acesso técnico e autenticação — **[V] confirmado sem login, sem token, sem UA especial**

```
GET https://www.empregare.com/api/pt-br/vagas/buscar-novo?ItensPagina=1
→ HTTP 200, JSON {"sucesso":true,"model":{...}}
```
Funciona com `curl` puro (UA default, sem header extra) [V]. 10 requisições seguidas → 10/10 HTTP 200, 2,4s total, sem 429 [V].

**Servidor MCP também confirmado funcionando de verdade**, não só anunciado:
```
POST https://www.empregare.com/api/mcp
Content-Type: application/json
Accept: application/json, text/event-stream
Body: {"jsonrpc":"2.0","id":1,"method":"initialize",...}
→ HTTP 200, SSE: {"result":{"protocolVersion":"2025-06-18","capabilities":{"logging":{},"tools":{}},"serverInfo":{"name":"Empregare - Vagas","version":"1.0"}},...}
```
[V]. Responde protocolo MCP real via `text/event-stream`. Para o coletor do bot, a API REST (`buscar-novo`) é mais simples de consumir que MCP — o MCP é mais útil se o Luiz quiser plugar isso num agente de IA depois, não para o cron job de coleta.

#### Cobertura — **[V]**

| Consulta | totalVagas | totalRegistro |
|---|---|---|
| todas (Brasil) | **14.338** | 4.850 |
| `Nivel=Estágio` | 472 | **241** |
| `Nivel=Aprendiz` | 259 | 86 |
| `Nivel=Trainee` (facet) | — | 8 |
| `Modalidade=4` (Totalmente Remoto) | 195 | 40 |
| `Modalidade=3` (Híbrido) | — | 142 |
| `Cidade=Brasília, DF, BR` | 1.442 | 599 |
| `Query=tecnologia` + `Nivel=Estágio` | 31 | **17** |
| `Query=tecnologia` + `Nivel=Estágio` + `Cidade=Brasília, DF, BR` | 11 | **7** |
| `Nivel=Estágio` + `Modalidade=1` (presencial) | 468 | 237 |
| `Nivel=Estágio` + `Modalidade=3` (híbrido) | 4 | 4 |
| `Nivel=Estágio` + `Modalidade=4` (remoto) | 0 | 0 |
| `Nivel=Estágio` + `Modalidade=0` (não informado) | 0 | 0 |

⚠️ **Existem dois contadores, `totalVagas` e `totalRegistro`, e eles nunca batem** [V]. Cross-check: para `Nivel=Estágio`, a soma de `totalRegistro` por modalidade (237 presencial + 4 híbrido + 0 remoto + 0 não-informado = **241**) bate exatamente com o `totalRegistro` sem filtro de modalidade (241) [V] — então **`totalRegistro` é a contagem confiável de registros distintos**, e `totalVagas` provavelmente soma vagas com múltiplas aberturas/vínculos por registro (não investiguei a fundo, mas o teste de soma consistente é forte evidência). **Usar `totalRegistro`, não `totalVagas`, para contagem de vagas.**

**Armadilha confirmada e evitada:** `Modalidade` e `Nivel` aceitam o **valor do campo `nome` do facet** (ex.: `"Estágio"`, `"Totalmente Remoto"`) — testei também o `id` numérico do facet (`Modalidade=4`) e **também funciona** [V] (bateu exatamente com o facet: 40 registros). Os dois formatos funcionam; não testei um valor claramente inválido para confirmar que erra ao invés de ignorar — **não medido**, registrar como risco residual (mesma armadilha do Sólides pode existir aqui).

Amostra real de `Query=tecnologia` + `Nivel=Estágio` (17 registros, 17 exibidos) [V]: majoritariamente vagas reais de TI (*"Estágio em Tecnologia da Informação - EBSERH/DF"*, *"ESTAGIÁRIO DE TI"*, *"Estágio em Ciência de Dados - Instituto Nacional de Tecnologia"*), mas com **falsos positivos por nome de empresa** (*"AMÉRICA TECNOLOGIA"* — vaga de recepção; *"CAMON INFORMATICA SOLUCOES TECNOLOGICAS"* — vaga de financeiro) e **falso positivo semântico** (*"Estágio (Tecnólogo em Estética)"*). **7 das 17 têm cidade em Brasília/DF** [V] — sinal forte de que a agência **RECRUTA EASY** publica muitos editais de estágio de TI de órgãos públicos do DF (EBSERH/DF aparece 4 vezes, inclusive **duplicado** com o mesmo título em datas diferentes — possível re-publicação do mesmo edital, mesmo cuidado de dedup já visto com o TRE-DF na Super Estágios) [V].

`SubArea` (parâmetro dedicado a área profissional, mais confiável que `Query` textual) está documentado mas **não teve valores válidos testados** — a resposta não trouxe facet de `subArea` para descobrir os valores aceitos. **Não consegui medir** o filtro de área "correto"; como medir: pedir ao próprio jobboard (via browser) a lista de subáreas do filtro de UI, ou tentar strings comuns (`"Tecnologia da Informação"`, `"TI"`) e comparar contagem contra baseline.

`DataPublicacao=1` (últimas 24h) não testado nesta sessão — **não medido**; seria o proxy de vazão mais direto de todo o inventário, vale medir depois com `DataPublicacao=1|2|3` para estimar vagas/dia sem precisar rodar o coletor por semanas.

#### Campos — **[V]**
Do objeto `VagaListagemViewModel`: `id`, `url` (relativo; forma curta `empregare.com/v{id}`), `titulo`, `chamada`, `data`, `timestamp`, `salario`, `nivel`, `empresa`, `logoThumb`, `pcd`, `trabalhoRemoto`/`trabalhoRemotoTexto`, `recrutamentoCego`, `cidades[]`, `tags[]`, `tipoProcessoSeletivo`, `codigoEdital`, **`dataCadastro`** (data de publicação real, confirmada em amostra: `"2026-08-10 14:22"`), `dataExpiracao`, `status`, `impulsionada`.

**Tem tudo que faltava em quase toda fonte do inventário**: título de verdade, modalidade estruturada, data de publicação, nível estruturado (inclusive `Trainee`), e ainda `codigoEdital` — que resolveria diretamente o problema de dedup de edital (TRE-DF/EBSERH) que apareceu em Super Estágios e aqui mesmo, **se o campo vier preenchido** (não confirmei se `codigoEdital` está de fato populado nos itens de edital — os exemplos que peguei vieram com o campo, mas não printei o valor; **não medido a fundo**).

Identidade: `id` inteiro [V].

#### Estabilidade
API versionada (`openapi/v1.json`, rota `/api/{culture}/vagas/buscar-novo`), documentada publicamente com Scalar, `robots.txt` libera e recomenda explicitamente (`Allow: /api/mcp`, `Allow: /api/docs`), `Content-Signal: ai-input=yes` — sinal deliberado de "pode ser consumido por agente" [V]. É a única fonte do inventário inteiro (partes 1–3) com esse nível de intenção declarada de ser consumida programaticamente. Risco de quebra silenciosa: baixo, dado o contrato OpenAPI formal.

#### Veredito
**A fonte mais barata de manter do inventário inteiro, se o volume de TI se sustentar.** Confirmado: API pública real, documentada, sem login, com filtro de nível/modalidade/cidade/recência estruturados, servidor MCP funcional, e sinal explícito de robots/Content-Signal convidando consumo automatizado. Volume de TI é modesto (17 registros para `tecnologia`+`Estágio` no Brasil todo, 7 no DF) mas a query por `Query` é textual e imprecisa — o filtro certo (`SubArea`) não foi mapeado. Forte candidata a entrar no roteiro de crescimento; vale 20–30 min adicionais para mapear os valores de `SubArea` antes de decidir a posição na fila.

---

## Prioridade 2 — parciais com achado concreto

### Agiel — **[V] paginação resolvida, `onCursoChange` explicado, listagem confirmada suficiente sem login**

Três perguntas em aberto de #11: paginação AJAX truncando cursos grandes, erro 500 em `onCursoChange`, e se a listagem (sem login) já basta para um alerta de Telegram. As três fecham nesta sessão.

#### Paginação — **[V] resolvida: existe um segundo handler, `onSeeMoreClick`, que acumula**

O handler `onClickBuscar` (usado na busca inicial) sempre devolve só a primeira leva (~30 cards, sem filtro; variável conforme paginação interna). Mas o botão "Veja mais vagas" no fim da página usa um **handler diferente**, achado no HTML renderizado (não no JS separado): `onSeeMoreClick`, que aceita os mesmos parâmetros de busca **mais `page`**, e a cada `page` maior **acumula** (não substitui) os resultados anteriores:

```
POST https://www.agiel.com.br/site/vagas
Headers: X-OCTOBER-REQUEST-HANDLER: onSeeMoreClick
         X-OCTOBER-REQUEST-PARTIALS: ajax_vagas_busca
         X-Requested-With: XMLHttpRequest
Body:    curso=<id ou vazio>&estado=&cidade=&page=<N>
```

Testado sem filtro de curso [V]: `page=1`→30, `page=2`→40 (cumulativo, +10), `page=26`→520, `page=27`→540, `page=30`→600, `page=40`→752, `page=50`→**752 (plateau)** — **752 é o total nacional de vagas de estágio ativas na Agiel, sem filtro de curso** [V]. Isso não estava medido em #11 (só existiam contagens por curso).

Testado com filtro de curso (`curso=211`, "ADMINISTRAÇÃO") [V]: `page=1`→30, `page=5`→100, `page=10`→200, `page=15`→262, `page=20`→**262 (plateau)**. **Confirma que basta chamar `onSeeMoreClick` com um `page` grande o suficiente (≥15–20 para cursos desse porte) para pegar tudo, sem precisar descobrir o total antes.** Para os cursos de TI (todos ≤18 vagas em #11), um único `page=2` ou `3` já basta com folga.

⚠️ Nota de custo: a resposta de `page=40` sem filtro veio com **1,38 MB de HTML** — para varrer os 34 cursos de TI com paginação completa, o ideal é aplicar sempre o filtro `curso=<id>` (que já limita o payload) em vez de paginar a busca sem filtro.

#### `onCursoChange` 500 — **[V] causa raiz encontrada: não é um bug, é uso incorreto do header de partials**

O erro 500 de #11 acontece porque eu (e o agente anterior) reaproveitamos o mesmo header `X-OCTOBER-REQUEST-PARTIALS` usado para `onClickBuscar`. O atributo `data-request-update="estado_dropdown: '#estado', cidade_dropdown: '#cidade'"` do `<select>` é sintaxe **do lado do cliente** (mapeia partial→seletor CSS para o JS injetar o resultado), não o valor esperado pelo header AJAX do October. Passando esse texto literal como partial name, o backend responde `500 "Nome de bloco inválido: estado_dropdown: #estado, cidade_dropdown: #cidade."` [V].

**Corrigido:** omitindo o header `X-OCTOBER-REQUEST-PARTIALS` (ou mandando vazio), `onCursoChange` responde **200 `[]`** [V] — um array vazio. Ou seja, o handler existe e não quebra, mas **não devolve nada útil por essa via** (provavelmente popula os dropdowns de estado/cidade via HTML de partial nomeado internamente que não descobri o nome certo). **Irrelevante para o coletor**: a busca de vagas por `curso` (`onClickBuscar`/`onSeeMoreClick`) não depende de `onCursoChange` — os campos `estado`/`cidade` podem ficar vazios na query e ainda assim a busca funciona [V, testado ao longo desta sessão]. Não vale mais tempo nisso.

#### Login: a listagem já basta para um alerta de Telegram — **[V] confirmado**

Inspecionei um card completo da listagem sem login [V]:
```html
<a href="https://www.agiel.com.br/site/entrar/MG2026001388">
  <img src=".../logo_empresa/MG/ipsemg.jpg" alt="MG2026001388">
</a>
<p>Código: MG2026001388</p>
<h3>CIÊNCIAS CONTÁBEIS, CONTABILIDADE</h3>
<span class="company"><i class="fa fa-building-o"></i>IPSEMG</span>
<span class="location"><i class="fa fa-map-marker"></i>Cidade Administrativa de Minas Gerais</span>
```
Campos presentes sem login: **código** (UF+ano+sequencial, ex. `MG2026001388` — dá UF de graça), **curso(s) aceitos** (serve de pseudo-título e já é o próprio filtro de TI, já que a busca é por curso), **empresa**, **local/cidade**. **Não há seletor de tipo de vaga (estágio/aprendiz/efetivo)** na página [V] — o site inteiro é só estágio (confirma o texto de #11, *"Sua busca gerou N vagas de estágio"*), então o filtro "é estágio?" é **sempre verdadeiro por construção da fonte**, sem precisar de campo.

**Conclusão:** os quatro dados pedidos pelo ticket (**título, empresa, local, se é TI**) **já vêm completos na listagem, sem login** [V]. "Se é estágio/júnior" também está resolvido, mas por **construção da fonte** (100% estágio, sem distinção de senioridade) em vez de por campo. O que falta sem login é só bolsa, descrição e horário — cosmético para uma notificação, não bloqueante.

#### Veredito atualizado
As três lacunas de #11 fecham: **752 vagas nacionais** (novo dado), paginação resolvida via `onSeeMoreClick`, `onCursoChange` explicado e confirmado irrelevante, e a listagem pública confirmada suficiente para notificar sem precisar de login. Isso reforça a posição da Agiel na recomendação de #11 (5ª fonte, condicional a Brasília continuar seca) — o custo de implementação cai porque não é preciso lidar com login para o caso de uso do bot (notificar, não candidatar).

---

### Companhia de Estágios — **[V] `carreira.ciadeestagios.com.br` é funil de cadastro de candidato, não portal de vagas; não existe API de listagem porque não existe listagem**

Pergunta de #11: existe uma API de vagas por trás do portal Next.js/Turbopack `carreira.ciadeestagios.com.br`? Resposta: **não há evidência de que exista, porque o site não tem função de listar vagas — é um formulário de cadastro**.

#### Reconfirmação do sitemap de programas — **[V]**
```
GET https://www.ciadeestagios.com.br/sitemap-programas-de-estagio.xml → HTTP 200
```
**104 `<loc>` distintos** [V, recontado], `<lastmod>` mais recente **2026-08-12** [V] — mesmos números de #11, sem mudança em 2 dias.

#### `carreira.ciadeestagios.com.br` — **[V] Next.js App Router + Turbopack, sem `_buildManifest.js` (isso é normal no App Router, não Pages Router)**

A técnica sugerida pelo ticket ("ler `_buildManifest.js`") **não se aplica aqui**: `_buildManifest.js` é artefato do **Pages Router** antigo do Next.js, que expõe um mapa de rota→chunk explícito. O App Router moderno (que é o que este site usa — confirmado pelos componentes `ClientPageRoot`, `OutletBoundary`, `MetadataBoundary` no payload RSC) [V] **não gera esse arquivo**; as rotas ficam embutidas em Server Components streamados, sem um manifesto único e legível.

**Testei a técnica equivalente**: baixei os 16 chunks JS/CSS referenciados no `<head>` da home (via `curl`, ~2,3 MB de JS ao todo) [V] e varri por padrões de rota (`"/api/...`", `"/vagas..."`, `"/oportunidades..."`, `"vaga"`, `"oportunidade"`, `"programa"`). **Resultado:**
- Só achei **um** endpoint de API real: `/api/search` (RTK Query, `reducerPath:"api/search"`), que serve **autocomplete de endereço** (`getAddress`, com params `address/state/city`) para o formulário de cadastro — não é vaga [V].
- As poucas ocorrências de "vaga" no bundle são **strings de i18n da UI de cadastro** (*"página de vagas"*, *"vaga dos sonhos"*, *"tem tudo pra ser sua"*) — texto de marketing do funil, não dados de vaga [V].

**Testei as rotas diretamente** [V]:

| Rota | HTTP |
|---|---|
| `/` | 200 |
| `/cadastro` | **200** |
| `/login` | 404 |
| `/vagas` | 404 |
| `/oportunidades` | 404 |
| `/programas` | 404 |
| `/api/vagas` | 404 |
| `/api/oportunidades` | 404 |
| `/api/jobs` | 404 |
| `/robots.txt` | 404 |
| `/sitemap.xml` | 404 |

**Só existem duas rotas: `/` e `/cadastro`.** Isso é consistente com o texto da própria home ("Companhia de Estágios... vagas abertas em programas de Jovem Aprendiz, Estágio e Trainee") funcionando como **landing page que empurra o candidato para `/cadastro`**, de onde ele é distribuído aos hotsites dos programas — o mesmo padrão de redirect já confirmado em #11 para as páginas `/vagas/<empresa>/` do site institucional.

#### Autenticação — **[V] não se aplica: não há o que listar sem login, porque não há listagem alguma no subdomínio.**

#### Veredito
**Não existe API do portal `carreira.` porque não existe portal de vagas ali** — é uma tela de captura de lead (nome, e-mail, currículo) que direciona o candidato para fora. A única fonte de sinal de "vaga nova" continua sendo o **sitemap institucional com `lastmod`** (104 programas), já mapeado em #11. **Como medir o que falta** (quantos dos 104 são de TI, quantos aceitam DF/remoto): como o conteúdo real mora em hotsites externos por empresa (ex.: `ericsson`, `cnh`, `cpfl`, `zurich` nos slugs), a única forma seria abrir cada um dos 104 hotsites individualmente e classificar à mão — não é automatizável a partir da Companhia de Estágios, então isso vira 104 fontes de "empregador único" na prática, o que não compensa. **A fonte, para fins de coleta automatizada, se resume ao sitemap com `lastmod` — sinal de "programa novo/atualizado", sem conteúdo estruturado por trás.**

---

### Remotar — **[V] API pública encontrada via `_buildManifest.js`; 6.388 vagas, categorias e tags de TI/estágio/júnior estruturadas, foco 100% remoto**

A técnica sugerida pelo ticket funcionou, mas em duas etapas: o `_buildManifest.js` deu a **rota da página** (`/search/jobs`), não a API — que estava num host totalmente diferente (`api.remotar.com.br`), achado por tentativa direta a partir de uma pista no `og:image` da home (`remotar-front.herokuapp.com`).

#### Acesso técnico — **[V]**

`remotar.com.br` é Next.js **Pages Router com export estático** (`"nextExport":true` no `__NEXT_DATA__`) [V] — front 100% client-rendered, sem SSR nem API routes locais. O `robots.txt` continua **404** (não existe) [V, reconfirmado].

```
GET https://remotar.com.br/_next/static/brz-vIeaMBoOqWEwnJSPw/_buildManifest.js → 200
```
Mapeia a rota `/search/jobs` para o chunk `pages/search/jobs-c1df1d4114e8b825.js` [V]. Baixei esse chunk e os chunks compartilhados que ele referencia (~150 KB de JS) procurando a URL da API — **não achei nenhuma URL absoluta neles** (só links de redes sociais) [V]. A API não está inline nesses chunks; **não consegui rastrear o import exato do cliente HTTP**. O que resolveu foi um atalho: o `og:image` da própria página aponta para `https://remotar-front.herokuapp.com/default-card.png`, sinal de que o backend histórico roda em Heroku sob o nome `remotar-*`. Testei variações e **`https://api.remotar.com.br/jobs` respondeu 200** [V] de primeira.

```
GET https://api.remotar.com.br/jobs
→ HTTP 200, JSON {"meta":{"total":6388,"per_page":50,"current_page":1,"last_page":128,...},"data":[...]}
```
Sem login, sem token, sem header especial [V]. 10 requisições seguidas → 10/10 HTTP 200 [V], sem rate limit visível. `api.remotar.com.br/robots.txt` → 404 JSON de rota inexistente (`E_ROUTE_NOT_FOUND`) — API sem robots, típico de backend puro sem frontend estático [V].

**Endpoints irmãos, também públicos** [V]: `GET /categories` (21 categorias) e `GET /tags` (24 tags, com emoji no nome).

#### Filtros — **[V] validados contra baseline, com uma armadilha real pega em flagrante**

| Param | Teste | Resultado |
|---|---|---|
| `categoryId=13` (Programação) | vs. total 6.388 | **1.948** — filtra de verdade |
| `categoryId=99999` (inexistente) | canário | **0** — erra para menos, não ignora. **Não é a armadilha do Sólides**: parâmetro/valor errado aqui dá zero, não "tudo" |
| `tagId=10` (🐣 Estágio) | vs. total | **200** |
| `tagId=17` (🐥 Júnior) | vs. total | **739** |
| `categoryId=13&tagId=10` (Programação + Estágio) | | **21** |
| `categoryId=13&tagId=17` (Programação + Júnior) | | **114** |
| `type=remote` | vs. total | **5.095** (79,7% do total — site é majoritariamente remoto por natureza) |
| `state=DF` / `uf=DF` | vs. total | **6.388 — IGNORADO SILENCIOSAMENTE, a armadilha do ticket se confirmou aqui** ⚠️ |

⚠️ **Armadilha confirmada, exatamente como o ticket avisou**: `state=DF` e `uf=DF` devolvem o total sem filtrar (6.388, idêntico ao baseline) [V] — o parâmetro certo para localização **não foi descoberto** (o `job.city`/`job.state` do objeto vêm `null` na maioria das vagas remotas, então filtro geográfico é provavelmente pouco útil mesmo — a Remotar é focada em remoto por proposta de produto, não uma fonte de DF).

**Categorias de TI e soma parcialmente inconsistente** [V]: somando individualmente `categoryId` de Data Science/Analytics (4)=697, DevOps (7)=265, QA (8)=201, SysAdmin (9)=193, Programação (13)=1.948, Programação Mobile (14)=115 → soma = **3.419**. Testando os seis juntos como `categoryId=4,7,8,9,13,14` (formato CSV) → **3.252** — **não bate com a soma individual** (diferença de 167, ~5%). **Não investiguei a causa** (dedup de vaga com múltiplas categorias? parsing parcial do CSV?); **como medir**: testar `categoryId[]=4&categoryId[]=7...` (array), que aqui deu **HTTP 500** [V] — a API não aceita esse formato — ou paginar cada categoria individualmente e deduplicar por `id` de vaga, que é o caminho mais seguro de qualquer forma.

#### Cobertura — **[V]**

| Corte | Total |
|---|---|
| total | **6.388** |
| `type=remote` | 5.095 |
| TI (6 categorias, soma individual) | 3.419 |
| TI (CSV, não confiável) | 3.252 |
| `tagId=10` Estágio (todas áreas) | 200 |
| `tagId=17` Júnior (todas áreas) | 739 |
| **Programação + Estágio** | **21** |
| **Programação + Júnior** | **114** |

Amostra real de `categoryId=13&tagId=10` (Programação + Estágio, 21 registros, todos exibidos) [V]: **100% vagas reais de TI**, sem falso positivo — *"Estágio de Desenvolvimento \| C# ou Go (Golang) + Angular"*, *"Estagiário(a) de Inteligência Artificial"*, *"Estágiario Blue Team"*, *"Estágio em Engenharia de Integrações SAP"*, todas `type: remote`, a maioria com `city`/`state` nulos (remoto puro), `createdAt` variando de **2025-12-02 a 2026-08-12** [V] — dá para estimar vazão diretamente por essa data.

Não testei as outras 5 categorias de TI (DevOps, QA, SysAdmin, Data Science, Programação Mobile) cruzadas com Estágio/Júnior individualmente — **não medido a fundo**; como medir: repetir a mesma query trocando `categoryId`.

#### Campos — **[V] muito ricos**
`id`, `companyId`, `title`, `subtitle`, `description` (HTML), `type` (`remote`/outros valores não vistos), `city`/`state`/`country` (majoritariamente `null` em vaga remota), `expiresAt`/`expires`/`expired`, `externalLink` (candidatura externa, ex. `*.inhire.app`), `isExternalLink`, `active`, **`createdAt`/`updatedAt`** (ISO com timezone), `thumbnailUrl`, `integrationSource` (ex. `"inhire"` — revela que parte do catálogo vem agregado de outros ATS), `jobSalary` (`from`/`to`/`currency`/`type`, majoritariamente `"uninformed"`), `jobTags[]` (relação para `tags`, incluindo Estágio/Júnior/Remoto/Jovem Aprendiz — **campo estruturado para excluir jovem aprendiz por tag**, algo que o CONTEXT.md pede e poucas fontes do inventário oferecem), `jobBenefits[]`, `jobRequirements[]` (texto + `mandatory` boolean).

Identidade: `id` inteiro [V]. **Tem `createdAt` real** — resolve novidade sem diff.

#### ToS / robots
`remotar.com.br/robots.txt` → 404 (não existe, reconfirmado) [V]. `api.remotar.com.br/robots.txt` → 404 de rota (API pura, sem noção de robots) [V]. Nenhuma proibição explícita nem permissão explícita — mesma zona cinzenta de outras fontes internas do inventário. Não li ToS textuais [P].

#### Estabilidade
API separada do front, hospedada historicamente em Heroku (`*.herokuapp.com` nos assets, embora a API ativa já esteja em domínio próprio `api.remotar.com.br`) [V]. Contrato de paginação clássico (`meta.total/per_page/current_page/last_page`), sem versionamento explícito no path — quebra seria silenciosa só no caso já flagrado (`state`/`uf` ignorados); nos demais parâmetros testados, erro dá zero, o que é mais seguro que a maioria das fontes do inventário [P].

#### Veredito
**A melhor fonte nova encontrada nesta rodada para o eixo "remoto Brasil"** — que é justamente o eixo mais fraco da Gupy segundo a parte 1. 21 vagas de Programação+Estágio e 114 de Programação+Júnior, **100% remoto por natureza do produto**, com categorias e tags estruturadas (inclusive uma tag dedicada a excluir Jovem Aprendiz) e `createdAt` para detecção de novidade sem diff. Ponto fraco: função de localização (DF) não funciona e não é o objetivo do site. Candidata forte ao roteiro de crescimento, ao lado do Sólides, para o recorte remoto.

---

### Eureca — **[V] os 81 programas varridos por completo; TI residual e sem remoto**

Pergunta de #11: dos 81 "programas" da API pública já localizada, quantos são de TI, remotos, e/ou aceitam Brasília/DF? Resposta: varri os 81 (não uma amostra) trazendo tudo numa página só.

#### Acesso técnico — **[V]**
```
GET https://candidate-api.eureca.me/opportunities?pageSize=200
→ HTTP 200, {"items":[...81 itens...],"total":81,"page":1,"pageSize":200}
```
Com `pageSize=200` (maior que o total) veio tudo numa requisição só, confirmando os 81 registrados em #11 [V].

#### Cobertura completa — **[V]**

| Corte | N |
|---|---|
| total de programas | **81** |
| `workModel=hibrido` | 53 |
| `workModel=presencial` | 27 |
| `workModel=remoto` | **1** (mas é *"Comunidade de Talentos de Engenharia"* — banco de talentos genérico, não vaga de TI) |
| **TI pelo nome** (revisado item a item, não regex) | **5** |
| **TI + remoto** | **0** |
| **TI tocando Brasília/DF** | **1** |

Os 5 de TI, inspecionados individualmente [V]:

| Nome | `workModel` | `locations.states` | `contractTypeKey` | `createdAt` |
|---|---|---|---|---|
| Estágio em Dados e Analytics | híbrido/presencial | **RJ, SP, DF** | internship | 2026-07-14 |
| Estágio em Tecnologia | híbrido/presencial | RJ, SP | internship | 2026-07-14 |
| Tecnologia e Dados | híbrido | SP (+34 cidades da grande SP) | internship | 2026-07-31 |
| Trainee em Tecnologia e Digital | presencial | vazio (não informado) | trainee | 2026-07-27 |
| Trainee em Tecnologia da Informação | híbrido | vazio (não informado) | trainee | 2026-08-03 |

**Só "Estágio em Dados e Analytics" toca Brasília** — é uma vaga multi-localização (RJ/SP/DF simultâneos) [V]. **Nenhuma é 100% remota**: as duas com localização vazia (`states: []`) não têm `workModel=remoto`, então "vazio" aqui parece significar "não preenchido pela empresa", não "aceita qualquer lugar" — **não confirmei essa leitura consultando a descrição completa** [não medido a fundo, mas a inconsistência workModel="hibrido"/"presencial" com locations vazio sugere dado incompleto na origem, não remoto real].

⚠️ Nota de metodologia: em #11 o item inspecionado tinha `locations` vazio e por isso a filtragem geográfica foi marcada como "precisa checagem item a item" — **essa checagem foi feita agora, nos 81 itens completos**, não numa amostra.

#### Campos confirmados adicionais — **[V]**
`contractTypeKey` (`internship`/`trainee`/outros não vistos), `createdAt` presente em 100% dos itens (formato `YYYY-MM-DD HH:MM:SS.ffffff+00`) [V], `publishedAt` **veio `null` em todos os 81 itens** [V] (não só no item de #11) — o campo existe no schema mas não é populado; `createdAt` é o único sinal de recência confiável.

#### Veredito atualizado
A lacuna fecha: **5 de 81 são de TI, zero remotas, uma toca Brasília** (por ser multi-localização, não por ser especificamente do DF). Confirma a leitura de #11 — mesmo bucket de "catálogo de programas corporativos" de baixo volume e baixa relevância para o recorte do Luiz. Não muda a recomendação: fica fora da largada, candidata a fase 2 "mandar tudo, sem filtro" junto com Cia de Talentos e Cia de Estágios.

---

## Prioridade 3 — medições em aberto sobre fontes já escolhidas

### Sólides — **[V] `occupationAreas=tecnologia` perde vaga real, com prova concreta**

Pergunta de #11: quanto o filtro de área "tecnologia" deixa passar por fora? O princípio do projeto ("coleta larga, entrega filtrada") depende dessa resposta — se o filtro de origem descarta vaga de TI mal categorizada, ele não deveria ser aplicado na coleta.

#### Método — **[V]**
1. Baixei **todos os ids** de `contractsType=estagio&occupationAreas=tecnologia` (28 páginas, **266 ids únicos**, contra `count=272` no envelope — pequena instabilidade de paginação, não investigada a fundo) [V].
2. Varri **400 vagas** de `contractsType=estagio` **sem filtro de área** (40 páginas × 10) [V] e apliquei um regex de TI generoso sobre o `title`.
3. Comparei: toda vaga que o regex marcou como TI e **não** está no conjunto de ids do passo 1 é candidata a "TI perdida pelo filtro de área".

#### Resultado — **[V] achado positivo, com prova nomeada**

Nos 400 títulos amostrados, o regex achou 13 candidatas a TI; 8 IDs únicos não apareciam no conjunto `occupationAreas=tecnologia`. Inspecionando cada um pelo `occupationAreas` real do objeto [V], a maioria era falso positivo do meu próprio regex (*"Estágio em Engenharia de Desenvolvimento de Processos e Montagem"*, *"Estagiário de Legalização – Desenvolvimento Imobiliário"*, *"Estágio Comercial"* — nenhuma é TI de verdade). Mas **uma achou o que a pergunta pedia**:

```json
{"id": 899856, "title": "ESTÁGIO DE TI", "occupationAreas": [{"id": 349581, "name": "Administrativo"}], "companyName": "PAVCON CONSTRUTORA LTDA", "state": "PI"}
```
**Uma vaga literalmente chamada "ESTÁGIO DE TI" está catalogada como `occupationAreas: Administrativo` na origem** [V] — prova direta de que `occupationAreas=tecnologia` **descarta vaga real de TI por erro de categorização da empresa que publicou**, exatamente o risco que motivou a pergunta.

(A outra candidata forte, *"TÉCNICO DE TESTES (ESTÁGIO)"*, está sob `occupationAreas: Produção`, numa fábrica de equipamentos eletroeletrônicos — inspecionei e é teste de linha de produção industrial, não QA de software; **não conto essa como leak**, é acerto da categorização de origem.)

#### Taxa estimada — **[V] ordem de grandeza, não número exato**
**1 miscategorização confirmada em 400 vagas de estágio amostradas** (0,25%). Extrapolando linearmente para as **2.876 vagas de estágio ativas** (contagem reconfirmada hoje, era 2.869 em #11 — variação normal de 2 dias) [V], a estimativa é de **~7 vagas de estágio de TI escondidas fora do filtro de área em todo o portal**, num universo de ~272 que o filtro já captura — ou seja, **o filtro de área perde algo em torno de 2–3% do volume de TI que existe de fato**, pela extrapolação desta amostra. **Não é uma medição exaustiva** (analisei 400 de 2.876, ~14% do universo); como medir com precisão: rodar a mesma comparação contra os 2.876 completos (288 páginas) e classificar por regex + revisão manual de todos os candidatos, não só uma amostra.

#### Conclusão para o princípio do projeto
**Confirma a preocupação do ticket**: o filtro de área da Sólides tem vazamento real, não hipotético. Para a v1 (Gupy, sem Sólides ainda) isso não muda nada agora, mas quando o Sólides entrar como fonte, a recomendação é: **coletar sem `occupationAreas=tecnologia` e aplicar o filtro de TI localmente** (regex sobre título, igual às outras fontes sem campo estruturado de área), aceitando o custo de mais falsos positivos em troca de não perder vagas reais como a `899856` — coerente com "coleta larga, entrega filtrada" e com a preferência já registrada em CONTEXT.md por falso positivo em vez de falso negativo.

---

### Nube — **[V] discrepância isolada dentro da própria API: o contador de metadado não bate com o array que a mesma resposta devolve**

Pergunta de #11: por que o portal anuncia milhares de vagas a mais do que a API anônima devolve?

#### Método e achado — **[V]**

Chamei o mesmo endpoint já mapeado em #11 e, desta vez, **li a resposta inteira em vez de só contar o array principal**:

```
GET https://www.nube.com.br/api/portal/buscar_filtro_vagas → HTTP 200
```

A resposta tem `param.lista_ids_vaga` (array de ids) **e também** `param.offset` e `param.dados_busca`, que eu não tinha inspecionado a fundo em #11. Hoje:

| Campo da própria resposta | Valor |
|---|---|
| `param.lista_ids_vaga` (tamanho do array) | **3.310** |
| `param.dict_por_id_vaga` (tamanho do dicionário, um por vaga) | **3.310** — bate com o array |
| `param.offset.total` | **6.494** |
| `param.dados_busca.texto_vagas_abertas` (HTML embutido) | *"**6494** Vagas abertas em **2515** Empresas"* |

**A mesma chamada, na mesma resposta JSON, contém dois números que não batem entre si**: o array de vagas de verdade tem 3.310 entradas, mas o campo de metadado `offset.total` (e o texto que o portal exibe, extraído do mesmo campo) diz 6.494. **Isso não é uma vaga "atrás de login" — é um contador que não está sincronizado com os dados que a própria API está devolvendo, na mesma resposta.** Os números individuais mudaram desde #11 (era 3.629/6.443, agora 3.310/6.494 — dois dias de flutuação normal), mas **a proporção da discrepância (quase 2×) se manteve**, o que reforça que é estrutural, não um bug pontual.

Testei a hipótese alternativa "o contador soma vaga×filial/reabertura, a lista devolve deduplicado" olhando o objeto de cada vaga em `dict_por_id_vaga` — não há campo de quantidade de posições nem de filial dentro do objeto [V], então **não consegui confirmar a causa exata**, só isolei **onde** ela mora: dentro da resposta da própria API pública, não numa segunda fonte de dados escondida atrás de autenticação.

⚠️ **Consequência prática direta para um coletor**: se alguém implementasse a Nube usando `offset.total` como "quantas vagas existem" (um campo tentador, porque é exatamente o rótulo que parece a resposta certa), a contagem estaria **quase o dobro** do que o coletor de fato consegue enumerar. **A contagem confiável é o tamanho de `lista_ids_vaga`/`dict_por_id_vaga`, não `offset.total`.** É a mesma classe de armadilha do par `totalVagas`/`totalRegistro` da Empregare (ver seção Empregare, Prioridade 1) — dois contadores dentro da mesma resposta, só um confiável, e o nome mais óbvio (`total`) não é o certo.

#### Não consegui medir
A causa exata da diferença entre os dois contadores (vaga×filial? reabertura? tipo de vaga fora do filtro padrão da UI?). **Como medir**: pedir ao próprio backend da Nube (via engenharia reversa mais profunda do componente Vue, ou testando parâmetros não documentados de `id_status_vaga`/tipo de registro) o que compõe o `offset.total`; ou, mais simples, abrir a página com um browser real e um proxy de rede para ver se existe uma segunda chamada de API que a `buscar_filtro_vagas` não cobre. Não fiz isso porque a Nube já está descartada por volume irrelevante no recorte do Luiz (13 vagas home office no Brasil inteiro, 2 de TI no DF, medido em #11) — mesmo que a causa se resolvesse a favor de mais vagas, é pouco provável que mude esse veredito, já que a proporção de TI/remoto medida em #11 não teria razão para mudar.

---

## Prioridade 4 — fontes ainda intocadas

### InfoJobs — **[V] lacuna fechada: categoria de TI estruturada encontrada, com contagem real; armadilha de localização confirmada**

A parte 1 tinha verificado acesso (HTML estático, sem login) mas não tinha conseguido medir volume de TI/DF/remoto. Fechei a lacuna.

#### Acesso — **[V] reconfirmado, sem login**
```
GET https://www.infojobs.com.br/empregos.aspx?palabra=estagio → HTTP 200
```
`robots.txt` continua liberando busca, só bloqueia páginas institucionais e `/static/` legado [V, reconfirmado].

#### Achado principal: categoria estruturada de TI — **[V]**

A página de resultados tem um **facet de área** com contagem por categoria, cada uma com id numérico estável e URL canônica própria:

```
categoria=74 → "Informática, TI, Telecomunicações"
URL canônica: empregos-de-informatica-ti-telecomunicacoes.aspx
```
Confirmado batendo em duas rotas diferentes [V]:
- `vagas-de-emprego-estagio.aspx?categoria=74` (base já filtrada por estágio) → **"109 Vagas"** no header, facet interno mostra **112** — pequena flutuação normal de segundos entre a carga do facet e do header.
- `empregos.aspx?categoria=74` (todas as senioridades) → **3.050 Vagas**, com facet de `ManagerialLevel` (senioridade) mostrando **Estagiário: 149**.

As duas contagens de "TI + estágio" (112 vs. 149) não batem entre si porque vêm de bases de filtro diferentes (uma parte de "toda vaga de estágio, filtra por categoria"; outra parte de "toda vaga de TI, filtra por senioridade") — **provável explicação: os dois filtros (`categoria` e `im`) não são exatamente comutativos na indexação do site, ou há atraso de cache entre facets**. Não investiguei qual dos dois é mais correto; **como medir**: repetir a mesma consulta combinando os dois parâmetros ao mesmo tempo (`empregos.aspx?categoria=74&im=1`) e usar esse número como definitivo.

**Modalidade de trabalho, cruzada com TI+estágio** [V] (facet dentro de `vagas-de-emprego-estagio.aspx?categoria=74`): **Presencial 94, Híbrido 14, Home office 4** — soma 112, bate com o facet de categoria. **Só 4 vagas de TI remotas em estágio no Brasil inteiro**, medido diretamente, sem regex.

**Não existe nível "Júnior" na senioridade estruturada** [V] — a lista completa de `ManagerialLevel` é: Estagiário, Operacional, Auxiliar, Assistente, Trainee, Técnico, Analista, Encarregado, Supervisor, Consultor, Especialista, Coordenador, Gerente, Diretor. "Júnior" no InfoJobs cai dentro de "Analista" misturado com pleno/sênior, ou precisa ser pego por regex no título — mesmo fallback que o CONTEXT.md já prevê para fontes sem campo estruturado.

#### Armadilha de localização — **[V] confirmada, exatamente como o ticket avisou**

| Parâmetro testado | Resultado |
|---|---|
| `empregos.aspx?palabra=estagio` (baseline) | **3.481 Vagas** |
| `empregos-em-brasilia.aspx?palabra=estagio` (slug textual) | **3.481 — idêntico ao baseline, ignorado** |
| `empregos.aspx?palabra=estagio&provincia=Distrito+Federal` (texto) | **3.481 — idêntico, ignorado** |
| `empregos.aspx?palabra=estagio&provincia=7` (numérico) | **65 — filtra de verdade** |

`provincia` só filtra quando recebe um **id numérico**; texto (mesmo que pareça o formato certo, como o nome do estado ou o slug de URL "em-brasilia") **é ignorado silenciosamente e devolve tudo** — a armadilha do ticket, pega em flagrante de novo (terceira vez no inventário: Sólides, Nube com `offset.total`, e agora InfoJobs).

⚠️ **Não consegui confirmar que `provincia=7` é de fato Distrito Federal** — inspecionei os cards de resultado da consulta filtrada e o primeiro item trazia local **"Todo Brasil"** (vaga remota/nacional), o que não prova nem desmente a hipótese. **Não encontrei o `<select>` ou lista de ids de UF na página estática** (o widget de localização usa autocomplete AJAX, não uma lista fixa no HTML) [V]. **Como medir:** capturar a chamada AJAX do autocomplete de cidade/UF (input `id="city"` visto no HTML, com `data-idlocation2`/`data-idlocation3`) digitando "Brasília" num browser real, ou testar outros ids pequenos (1–27, plausível para 26 estados + DF) e comparar os cards retornados por cidade mencionada no texto.

#### Veredito
Lacuna fechada com números reais: **~110–150 vagas de TI em estágio no Brasil** (dependendo de qual dos dois filtros é o correto), das quais **só 4 remotas**. Fonte de acesso fácil (HTML estático, sem JS necessário para os facets, que já vêm no HTML inicial) com categoria de TI estruturada e confiável — melhor do que regex de título. Ponto fraco: sem filtro de DF confirmado e sem senioridade "júnior" nativa. Não é candidata óbvia a fonte prioritária (volume de TI é pequeno e comparável ao Sólides/Empregare, sem vantagem clara), mas é tecnicamente viável e barata de implementar.

---

### Glassdoor — **[V] confirmado bloqueio anti-bot; não é viável a custo zero**

A parte 1/2 encontrou `HTTP 403` na home com UA de Chrome. Reconfirmei e li o `robots.txt` completo, que ficou pendente.

#### Acesso — **[V] 403 reconfirmado, com e sem UA de navegador**
```
GET https://www.glassdoor.com.br/ → HTTP 403 (UA Chrome desktop)
GET https://www.glassdoor.com.br/ → HTTP 403 (UA curl default)
GET https://www.glassdoor.com.br/Vaga/index.htm → HTTP 403
```
[V]. O corpo da resposta 403 é uma página de bloqueio genérica (~240 KB), não um captcha interativo capturável por requisição simples [V]. Testei 3 variações de User-Agent (Chrome desktop, Googlebot, e sem header) — **as três resultaram em 403** [V], o que descarta a hipótese simples de "só falta UA de navegador".

#### robots.txt — **[V] lido por completo desta vez**
```
User-agent: *
Disallow: /member/
Disallow: /Salary-Estimate/
... (~40 regras Disallow para páginas autenticadas, filtros de busca com parâmetros de sessão, etc.)
Disallow: /Vaga/  ← rota de vaga individual está BLOQUEADA
Sitemap: https://www.glassdoor.com.br/sitemap/sitemap-index.xml
```
[V, lido integralmente]. Diferente do que a leitura parcial de #11 sugeria, o robots **não é permissivo por padrão para vagas** — a rota de vaga (`/Vaga/`) e a maior parte da busca com parâmetros estão em `Disallow` explícito. Mesmo que o 403 não existisse, o robots já desaconselharia raspar vagas.

#### Veredito
**Fora, com alta confiança.** Bloqueio anti-bot ativo (403 em toda tentativa, independente de UA) **e** robots explicitamente restritivo para a rota de vaga. Contornar exigiria navegador headless com fingerprinting realista e provavelmente rotação de IP — infraestrutura incompatível com o orçamento de R$ 0/mês do projeto. Mesmo perfil do Indeed, já descartado na parte 1. Não vale revisitar sem mudança de orçamento.

---

### EstágioTrainee — **[V] site Wix confirmado; API de e-commerce Wix encontrada, mas não serve vagas — é site institucional sem mural de vagas navegável**

#### Acesso — **[V]**
```
GET https://www.estagiotrainee.com/ → HTTP 200, 770 KB (reconfirmado)
GET https://www.estagiotrainee.com/robots.txt → HTTP 200, Allow: / (Wix auto-gerado, reconfirmado)
```

Sites Wix expõem rotas de API previsíveis (`_functions/`, `_api/`) quando o dono usa Velo (o runtime de backend do Wix) ou apps de e-commerce/coleções dinâmicas. Testei as mais comuns [V]:

| Rota | HTTP |
|---|---|
| `/_functions/` | 404 |
| `/_api/wix-ecommerce-storefront-web/v1` | 404 |
| `/_api/dynamicpages-router` | 404 |
| `/vagas` | 404 |
| `/oportunidades` | 404 |
| `/blog` | **200** |

**Não há rota de vaga alguma.** Inspecionei o texto renderizado (SSR) da home [V]: o site é um **blog/conteúdo institucional sobre carreira e processos seletivos de programas de trainee/estágio de empresas grandes** (o nome é enganoso) — artigos do tipo "Programa de Trainee X abre inscrições", não uma listagem estruturada de vagas. Não achei em nenhuma página um padrão de card de vaga com id, empresa, local.

#### Veredito
**Não é uma fonte de vagas — é um site de conteúdo/blog sobre processos seletivos**, apesar do nome sugerir mural de vagas. Sem estrutura de dados para coletar. Fora, e a razão é de conteúdo, não de acesso técnico (parecido com o caso da CIEE, mas em sentido inverso: aqui não há nem vaga para filtrar).

---

### Senado Federal (programa de estágio) — **[V] edital periódico, não fluxo contínuo; coletor dedicado não compensa**

#### Achado — **[V]**

Primeira tentativa (`/institucional/rh/estagio`) deu 404 [V] — a URL certa, achada por tentativa direta, é:
```
GET https://www12.senado.leg.br/institucional/estagio → HTTP 200, 72 KB
```
A página institucional descreve o **Programa de Estágio do Senado Federal** ("estágios de nível superior, que promovam a integração entre os âmbitos acadêmico e profissional") com menu de seção **Características / Candidato / Instituições de Ensino / Perguntas Frequentes / Regulamento** [V]. **Não há vitrine de vagas abertas nem lista de áreas com contagem** na página — é conteúdo institucional estático (regulamento, contato, declaração de nepotismo), não um mural de oportunidades [V]. Não encontrei API, JSON ou feed. A subrota `/institucional/estagio/candidato` testada deu 404 [V] — não persegui achar a URL certa de cada subseção, dado que a resposta à pergunta do ticket já estava clara pela estrutura da página principal.

Pelo formato da página (regulamento + processo formal, sem lista de vagas ativas navegável), a leitura mais provável é que o programa funcione por **edital de processo seletivo publicado periodicamente** (padrão comum de órgão público, já visto de forma explícita na Super Estágios via os lotes do TRE-DF em #11) — mas **não confirmei isso lendo um edital real** [P, não confirmado diretamente]. Não medi a periodicidade (quantos editais por ano) nem se há recorte por área dentro do edital — **não medido a fundo**: como medir, seria achar a página/seção que lista os editais vigentes e passados (não localizada nesta sessão) e contar a cadência ao longo de um ano.

#### Resposta à pergunta do ticket: vale um coletor dedicado a um empregador só?
**Não.** Além de ser fonte única (viola a lógica de agregador do bot, que já lida com múltiplas fontes via diff de snapshot), o padrão de publicação é **edital esporádico**, não fluxo — o mecanismo de detecção de novidade do bot (diff contra snapshot anterior) é desenhado para vagas que aparecem e desaparecem individualmente, não para um evento raro de "abriu processo seletivo anual". Monitorar isso é mais parecido com "avisar quando uma página muda" (change detection num único URL) do que com o modelo de coleta do bot. Se o Luiz quiser isso, a forma certa não é uma fonte de vagas — é um monitor de página separado, fora do escopo do coletor atual.

---

### BairesDev — **[V] confirmado: perfil pleno/sênior, quase nada de estágio/júnior; coletor dedicado não compensa**

#### Achado — **[V]**
```
GET https://www.bairesdev.com/careers/ → HTTP 301 → /join-us/
GET https://www.bairesdev.com/join-us/ → HTTP 200, 275 KB
```
A página de carreiras é renderizada como Next.js (payload RSC visível no HTML) e **não lista vagas na própria página** — é uma landing page institucional de "trabalhe conosco" [V]. Testei `/careers/job-opportunities/`, `/job-opportunities/`, `/careers/jobs/` como candidatos a listagem — **os três deram 404** [V]; não localizei a rota real de listagem de vagas nesta sessão.

O texto renderizado da página (extraído do HTML, sem JS) **confirma o posicionamento de marca**: menção repetida (12×) a **"Top 1% Talent"**, textos como *"Hire Software Developers — Top 1% Talent"*, foco em "elite network" de desenvolvedores experientes para clientes internacionais [V]. Busquei ocorrências de "intern"/"estágio"/"júnior"/"entry-level" no HTML — a única ocorrência de "intern" veio de **"internal processes"**, não de "internship" [V]. **Nenhuma menção a estágio, júnior ou trainee em toda a página.**

#### Resposta à pergunta do ticket: vale um coletor dedicado a um empregador só?
**Não, por dois motivos independentes**: (1) mesmo problema estrutural do Senado — fonte de empregador único não se encaixa no modelo de agregador do bot; (2) **mesmo que se encaixasse, o conteúdo da BairesDev não é o que o Luiz procura** — é uma empresa que declara publicamente focar em talento sênior. Descarte duplo, mais forte que o caso do Senado (que ao menos tem vagas de estágio de verdade, só que raras).

---
