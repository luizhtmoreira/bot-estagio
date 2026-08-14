# Inventário de fontes de vagas — estágio e júnior em TI (Brasil)

Ticket: [01-inventario-de-fontes](../issues/01-inventario-de-fontes.md) · Mapa: [Bot de vagas](../map.md)
Data da apuração: **2026-08-14**. Perfil-alvo: estágio **e** júnior, qualquer área de TI, **remoto Brasil** + **presencial/híbrido em Brasília/DF**, orçamento **R$ 0/mês**, entrega no **Telegram**.

## Como ler este documento

Toda afirmação está marcada:

- **[V]** — **VERIFICADO** nesta sessão, com requisição HTTP real feita por mim em 2026-08-14. Códigos de status, contagens e campos vêm da resposta que eu recebi.
- **[P]** — **PRESUMIDO**: inferência, leitura de ToS/robots, ou conhecimento prévio. Não medi.

Números de volume só aparecem quando eu de fato os contei. Onde não consegui medir, digo isso explicitamente e digo **como medir**.

**Aviso sobre os números:** todas as contagens são um *snapshot de um dia*. "N publicadas nos últimos 7 dias" é o melhor proxy de fluxo que consegui tirar de uma única coleta — não é média histórica. A medição honesta de vazão exige rodar o coletor por 2–3 semanas e contar IDs novos por dia; isso é trabalho do próprio bot, não desta pesquisa.

**Classificação "é TI?":** onde eu digo "TI" apliquei um regex sobre o **título** da vaga (desenvolv|program|software|dados|infra|devops|cloud|redes|suporte|QA|test|sistemas|back/front/fullstack|linguagens|segurança da informação|…). É um filtro grosseiro: erra para menos (vaga de TI com título genérico) e para mais ("Estágio em Contabilidade: Dados e IA" entrou). Trate como ordem de grandeza.

---

## 1. Gupy (portal público) — `employability-portal.gupy.io`

### 1.1 Acesso técnico — **[V] API JSON interna, sem login, sem token**

O `portal.gupy.io` é um Next.js client-rendered: o HTML entregue **não contém as vagas** e **não tem `__NEXT_DATA__`** com o resultado [V]. Achei o endpoint real lendo os chunks JS do próprio bundle (`/_next/static/chunks/*.js`), onde está o construtor de query.

O host `portal.api.gupy.io` (que circula em tutoriais antigos) responde **404 nginx** hoje [V]. O host correto é:

```
GET https://employability-portal.gupy.io/api/v1/jobs?jobName=<termo>&limit=100&offset=0
```

Resposta **HTTP 200**, JSON `{"data": [...], "pagination": {"total": N, "limit": L, "offset": O}}` [V].

Parâmetros confirmados por leitura do bundle + teste real [V]:

| Param | Valores testados | Observação |
|---|---|---|
| `jobName` | texto livre | busca no título |
| `type` | `vacancy_type_internship`, `vacancy_type_effective`, `…apprentice`, `…trainee`, `…temporary`, `…freelancer`, `…volunteer`, `…outsource`, `…talent`, `…summer`, `…lecturer`, `…intermittent`, `…parter` | lista extraída do bundle |
| `workplaceType` | `remote`, `on-site`, `hybrid` | |
| `state` | `Distrito Federal` (nome por extenso) | |
| `city` | `Brasília` | |
| `limit` / `offset` | testei `limit=100`, offset paginado | |
| `badge`, `isPWD` | flags | |

Endpoint irmão: `/api/v1/jobs/companies` [P — visto no bundle, não testei].

Não precisa de header especial: funciona **com `User-Agent: python-requests/2.31` e até com um UA inventado (`MeuBotVagas/1.0`)** — HTTP 200 nos dois casos [V]. Mandei `Origin: https://portal.gupy.io` nos testes principais, mas ele não é obrigatório [V].

### 1.2 Autenticação — **[V] nenhuma.** Sem cookie, sem token, sem conta. Zero risco de banimento de conta porque não há conta envolvida.

### 1.3 Termos de uso / robots

- `https://portal.gupy.io/robots.txt` = `User-agent: * / Disallow:` — ou seja, **libera tudo** [V].
- ToS de candidatos ("Recrutamento e Seleção") contém a cláusula: *"agregar, copiar ou duplicar partes do Gupy Recrutamento e Seleção, incluindo oportunidades de trabalho expiradas"* como conduta proibida [V, via fetch da página de termos]. Não há menção literal a "scraping", "robô" ou "crawler" [V].
- **Leitura honesta do risco:** existe uma tensão real. O robots.txt libera, mas o ToS proíbe "agregar/copiar". A cláusula está no contrato de uso da *plataforma de R&S* — cuja aceitação acontece ao criar conta/candidatar-se, o que o bot não faz. Mitigadores: uso pessoal, não-comercial, sem republicação pública, link de volta para a vaga original, volume baixo. **Não sou advogado; isto não é parecer jurídico.** [P]
- Risco prático de bloqueio: **baixo**. Fiz **30 requisições seguidas sem pausa** contra o endpoint (300 vagas paginadas) — **30/30 HTTP 200 em 33s**, nenhum 429, nenhum captcha [V].

### 1.4 Cobertura — **[V], medida hoje**

`pagination.total` para consultas específicas (número total de vagas ativas no portal, não só as retornadas):

| Consulta | Total ativas | Publicadas ≤7d | TI pelo título | TI **e** ≤7d |
|---|---|---|---|---|
| todas as vagas do portal | **82.023** | — | — | — |
| `type=internship` (Brasil todo) | **2.915** | — | — | — |
| `type=internship&workplaceType=remote` | **49** | 18 | 29 | **10** |
| `type=internship&state=Distrito Federal` | **47** | 10 | 25 | **7** |
| `jobName=junior&workplaceType=remote` | **46** | 15 | 21 | **9** |
| `jobName=junior&state=Distrito Federal` | **11** | 6 | 0 | **0** |
| `jobName=junior` (Brasil todo) | 1.079 | — | — | — |
| `state=Distrito Federal` (tudo) | 1.467 | — | — | — |
| `jobName=desenvolvedor&workplaceType=remote` | 270 | — | — | — |

**Vazão estimada para o perfil do Luiz: ~3 a 4 vagas novas de TI por dia**, somando estágio-remoto + estágio-DF + júnior-remoto (26 vagas TI publicadas em 7 dias nos três recortes) [V, snapshot único — ver aviso acima].

Exemplos reais colhidos: *"Estágio em desenvolvimento Web"* (Instituto Eldorado, remoto), *"Estágio em Testes de Software"*, *"Estagiário(a) Suporte TI"* (DF), *"Analista de Suporte de TI Junior"*, *"React / Java Full-Stack Developer | Júnior (Remote)"*, *"Engenheiro de dados Junior"* [V].

### 1.5 Campos disponíveis — **[V], objeto real capturado**

```json
{
  "id": 12024455,
  "companyId": 40033,
  "name": "Estágio em desenvolvimento Web",
  "description": "…texto completo em HTML-ish…",
  "careerPageId": 85975,
  "careerPageName": "Instituto de Pesquisas ELDORADO",
  "careerPageLogo": "https://attachments.gupy.io/...",
  "careerPageUrl": "https://institutoeldorado.gupy.io/...",
  "type": "vacancy_type_internship",
  "publishedDate": "2026-08-14T17:45:12.862Z",
  "applicationDeadline": "2026-10-09",
  "isRemoteWork": true,
  "city": "", "state": "", "country": "Brasil",
  "jobUrl": "https://institutoeldorado.gupy.io/job/<base64>?jobBoardSource=gupy_portal",
  "badges": {"friendlyBadge": true, "isPWD": false},
  "workplaceType": "remote",
  "disabilities": false,
  "skills": []
}
```

Para o ticket de **identidade de vaga**: `id` é inteiro, estável e global no portal — é a chave natural. `publishedDate` com timestamp permite "é nova?" sem depender de diff. `applicationDeadline` dá um sinal de expiração *previsto*, independente do sumiço observado. Note que **em vaga remota `city` e `state` vêm vazios** [V] — o filtro de localidade só funciona para presencial/híbrido, e "remoto" tem que sair de `workplaceType`/`isRemoteWork`.

Ausências relevantes: **não há campo de senioridade** e **não há salário** [V]. Júnior só pode ser detectado por texto (ver §11).

### 1.6 Estabilidade

- Estrutural: o endpoint mudou de host historicamente (`portal.api.gupy.io` → `employability-portal.gupy.io`) — isso é evidência direta de que **APIs internas quebram** [V, o 404 do host antigo é o próprio dado].
- Mas: por ser JSON com contrato estável (`data`/`pagination`), a quebra é **ruidosa** (404 / KeyError), não silenciosa. Muito melhor que HTML, onde a quebra vira "0 vagas hoje" [P].
- Frequência esperada de quebra: **baixa, mas não nula** — talvez 1x por ano ou dois [P, não tenho série histórica].

---

## 2. Programathor — `programathor.com.br`

### 2.1 Acesso técnico — **[V] HTML estático, sem JS**

`GET https://programathor.com.br/jobs` → **200**, ~220 KB, **15 vagas por página** em blocos `<div class="cell-list">` com `<a href="/jobs/<id>-<slug>">` [V]. Paginação `?page=N` funciona e devolve conjuntos distintos de IDs [V].

Filtros por querystring, extraídos do próprio HTML [V]:

```
/jobs?contract_type=Estágio      (urlencoded: Est%C3%A1gio)
/jobs?expertise=Júnior           (urlencoded: J%C3%BAnior)
/jobs?remoto=true
/jobs?accepts_outer_candidates=true
/jobs?company_type=Startup|Grande+empresa|Pequena/média+empresa
/jobs-<tecnologia>               (ex: /jobs-python, /jobs-front-end)
```

⚠️ **Combinar dois filtros deu HTTP 302** (`?expertise=Júnior&remoto=true` redirecionou e perdeu o resultado) [V]. Coletar cada filtro separado e cruzar em casa.

Cada página de detalhe tem **JSON-LD `JobPosting`** com `datePosted` (ex.: `"datePosted": "2026-07-31"`) [V] — a data **não** aparece no card da listagem, então saber a idade da vaga exige 1 request por vaga.

### 2.2 Autenticação — **[V] nenhuma** para listar e ver detalhe. Só candidatar exige conta.

### 2.3 ToS / robots

`robots.txt` [V]:
```
User-agent: *
Disallow: /admin/  /user/  /users/  /company/
Sitemap: https://programathor.com.br/sitemap.xml
```
`/jobs` e `/jobs/*` **não estão bloqueados**, e o sitemap lista `/jobs` com `changefreq: daily` — é convite explícito a crawler [V]. Não li os ToS textuais [P: presumo cláusula genérica anti-abuso, como quase todo site].

Site está atrás de **Cloudflare** (vi `rocket-loader.min.js` injetado) [V], mas passou com `python-requests/2.31` e com UA inventado — **sem challenge** [V]. Risco de bloqueio: baixo em volume educado; Cloudflare pode endurecer a qualquer momento [P].

### 2.4 Cobertura — **[V], contada por paginação exaustiva**

| Filtro | Vagas únicas encontradas | Páginas percorridas |
|---|---|---|
| `/jobs` (todas) | 594 | parei no teto de 40 páginas |
| `?expertise=Júnior` | **597** | parei no teto de 40 |
| `?contract_type=Estágio` | **450** | 31 (esgotou) |

**Não confio nesses números como "vagas abertas hoje".** A lista de Estágio inclui IDs muito antigos (`13029`, `29113`) ao lado de IDs atuais (`33705`) — forte indício de que **vagas encerradas continuam listadas** [V, a evidência é a distribuição de IDs]. O site **não exibe contador total** [V].

**Como medir de verdade:** paginar `?contract_type=Estágio` e `?expertise=Júnior` completos, buscar o `datePosted` do JSON-LD de cada detalhe, e contar só as dos últimos 30 dias. São ~1.000 requests de detalhe — factível uma vez, caro por dia. Alternativa barata: coletar só as 3 primeiras páginas por filtro diariamente (IDs vêm ordenados por recência na listagem sem filtro) e tratar ID novo = vaga nova.

Cobertura **100% TI** (é um board de dev) [V — é a proposta do site]. Cobertura de **Brasília especificamente: fraca** [P] — o board é dominado por São Paulo e remoto; não há filtro de cidade na querystring que eu tenha encontrado [V].

### 2.5 Campos disponíveis — **[V]**

Da listagem: título, empresa, localidade/modalidade (`Remoto`, `são paulo (Híbrido)`), porte da empresa, senioridade (`Júnior`/`Pleno`/`Sênior`), tipo de contrato (`CLT`/`PJ`/`Estágio`), stack (tags de tecnologia), logo, e o link `/jobs/<id>-<slug>`.

Do detalhe (JSON-LD + HTML): tudo acima + `datePosted`, descrição completa, salário quando informado ("Não especificado" é comum), detalhe do híbrido ("3 dias presenciais/semana"), aceita candidato de outra cidade.

**Senioridade explícita e tipo de contrato explícito são o grande diferencial desta fonte** — é a única do inventário que entrega "Júnior" e "Estágio" como *campo*, não como palavra no título [V]. Identidade: `id` numérico no path, estável.

### 2.6 Estabilidade

HTML server-rendered Rails clássico, marcação Bootstrap (`panel`, `cell-list`, `col-md-9`) — visual e estrutura mudam pouco [P]. Risco: qualquer redesign quebra os seletores **silenciosamente** (retorna 0 vagas, não erro). Mitigação obrigatória: alarme de "0 resultados" tratado como falha, não como ausência de vagas.

---

## 3. Vagas.com.br

### 3.1 Acesso técnico — **[V] HTML estático parseável**

`GET https://www.vagas.com.br/vagas-de-<termo>` → **200**, HTML com os cards já renderizados e **`<h1>` contendo o total** [V]:

- `/vagas-de-estagio-ti` → `"16 vagas de emprego para estagio ti"`, 16 links [V]
- `/vagas-de-ti-em-brasilia` → `"58 vagas de emprego para ti em brasilia"`, 40 links na página [V]
- `/vagas-de-estagio-em-brasilia` → `"49 vagas de emprego para estagio em brasilia"`, 40 links [V]
- `/vagas-de-junior-ti` → `"42 vagas de emprego para junior ti"`, 40 links [V]

Tem **JSON-LD** nas páginas [V]. Links de vaga no formato `/vagas/v2783038/programa-de-estagio-b3-2026` → **`v<id>` é identidade estável** [V].

⚠️ **Paginação não resolvida.** `?pagina=2` retorna a página mas com **0 cards** [V]; não achei endpoint AJAX (`?ajax=1` e `/ajax/carregar-mais-vagas/…` falharam — 200 vazio e 301) [V]. Página 1 entrega até 40 resultados, o que **cobre 3 das 4 buscas acima inteiras**. Para buscas maiores, a paginação precisa ser investigada com um navegador olhando a aba Network [P: é quase certamente infinite scroll via XHR].

Também não achei URL de filtro "remoto" — `/teletrabalho/vagas-de-ti` retornou 0 cards [V].

### 3.2 Autenticação — **[V] nenhuma** para listar.

### 3.3 ToS / robots — **este é o ponto delicado, e é interessante**

`robots.txt` [V]:
- Bloco `User-Agent: *`: `Allow: /` com `Disallow:` apenas em `/auth/ /api/ /v1/ /users/ /token/ /servicos/ /social/ /move_to /vagas/pesquisas /suporte /mapa-de-carreiras/cargo/`. **As páginas de busca (`/vagas-de-…`) e as vagas (`/vagas/v…`) estão liberadas** [V].
- Bloco Cloudflare com Content Signals: `Content-Signal: search=yes, ai-train=no, use=reference` [V].
- **Lista longa e explícita de bots de IA bloqueados (`Disallow: /`)**, incluindo `ClaudeBot`, `Claude-Web`, `anthropic-ai`, `GPTBot`, `CCBot`, `PerplexityBot`, `Bytespider`, `Google-Extended`, `Diffbot`, `MistralAI-User` etc. [V]

**Interpretação:** o site distingue *indexar/consultar* (permitido) de *treinar IA* (proibido). Um bot pessoal que lê a busca, extrai título/link e manda no Telegram cai no primeiro caso — está dentro do `Allow: /` do `User-Agent: *`, e "use=reference" combina com "eu mando o link de volta". **Não** use um UA que se pareça com bot de IA. Declare um UA próprio e honesto. [P — é minha leitura do robots, não uma autorização]

Passou com `python-requests/2.31` e com UA inventado — 200 nos dois [V].

### 3.4 Cobertura — **[V] boa em Brasília, fraca em "remoto"**

58 vagas de TI em Brasília e 49 de estágio em Brasília são números **substancialmente melhores que os da Gupy no DF** [V]. Vagas.com é forte em empresas tradicionais, que é justamente onde estão as vagas presenciais de Brasília. Card traz data relativa ("Há 2 dias") [V].

Não medi quantas dessas 58/49 são de fato estágio/júnior **em TI** — o cruzamento título×TI×senioridade exigiria buscar página a página. **Como medir:** coletar `/vagas-de-ti-em-brasilia` e `/vagas-de-estagio-em-brasilia`, intersectar por `v<id>`, e aplicar o filtro de senioridade no título.

### 3.5 Campos — título, empresa, resumo da descrição, cidade/UF, restrição de candidatura ("aceita apenas candidaturas de RJ"), data relativa, link com id `v<n>`, JSON-LD no detalhe [V]. **Sem senioridade estruturada** [V].

### 3.6 Estabilidade — HTML server-rendered, marcação estável há anos [P]. Cloudflare na frente [V]. A dependência de `<h1>` para o total e de classes CSS para os cards é frágil da mesma forma que Programathor.

---

## 4. LinkedIn — endpoint `jobs-guest`

### 4.1 Acesso técnico — **[V] funciona, sem login**

```
GET https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search
    ?keywords=<termo>&location=Brazil&f_TPR=r86400&f_WT=2&start=0
```
→ **HTTP 200**, fragmento HTML com **10 `<li>` por chamada** [V]. Cada card tem `data-entity-urn="urn:li:jobPosting:4454367151"` (**ID estável**) e `<time datetime="2026-08-14">` [V].

Detalhes que descobri testando [V]:
- `location=Brasil` (português) **é ignorado silenciosamente** — devolveu vagas de *Miami, FL*. Com `location=Brazil` (inglês) ou `geoId=106057199` funciona corretamente.
- `f_TPR=r86400` = últimas 24h; `f_WT=2` = remoto. Paginação por `start=`.
- Resultados reais colhidos: *"Estágio Superior em TI – Gestão de Redes"* (Niterói), *"Estagiário(a) de Infraestrutura"* (Chaintech, **Brasília, Federal District**), *"Desenvolvedor(a) Full Stack Júnior"* (Claro), *"Desenvolvedor Jr"* (Tag.vc, "4 hours ago") [V].

### 4.2 Autenticação — nenhuma para este endpoint [V]. **Isso é o que o torna tentador e o que o torna um risco assimétrico**: sem conta, o pior caso é bloqueio de IP, não banimento. Mas se alguém "melhorar" isso depois com cookie `li_at`, o pior caso vira **perda da conta pessoal do LinkedIn** — o ativo profissional mais caro do usuário. [P]

### 4.3 ToS / robots — **[V] proibido de forma inequívoca**

`https://www.linkedin.com/robots.txt`, topo do arquivo:
> *"The use of robots or other automated means to access LinkedIn without the express permission of LinkedIn is strictly prohibited."*

E, verificado por grep no arquivo:
- `User-agent: * → Disallow: /` (bloqueio total para qualquer agente não-listado) [V]
- `Disallow: /jobs-guest/` — **o endpoint que funciona é nominalmente proibido** [V]

Ou seja: aqui não há ambiguidade interpretativa como na Gupy. O robots.txt nomeia o caminho. Risco prático: bloqueio de IP e challenge são comuns; o caso *hiQ v. LinkedIn* trata de dados públicos nos EUA e **não** é salvo-conduto no Brasil [P].

### 4.4 Cobertura — **a maior de todas, disparado** [P — não consegui obter total; o endpoint devolve 10 por vez sem contador]. É a única fonte que agrega Gupy + Solides + ATS próprios + recrutadores autônomos ao mesmo tempo.

**Como medir:** paginar `start=0,10,20,…` com `f_TPR=r86400` até vir vazio, para cada combinação de keyword. Não fiz porque paginar agressivamente é exatamente o comportamento que dispara bloqueio.

### 4.5 Campos — título, empresa, localidade (string livre, ex. "Brasília, Federal District, Brazil"), `datetime` de publicação, "Actively Hiring", URN estável, link para `/jobs/view/<id>` [V]. Sem senioridade estruturada, sem modalidade explícita no card (vem do filtro `f_WT`) [V].

### 4.6 Estabilidade — endpoint não-documentado que o LinkedIn muda quando quer, e que já ganhou throttling agressivo mais de uma vez [P]. É a fonte mais provável de quebrar.

---

## 5. InfoJobs Brasil

- **Acesso [V]:** `GET https://www.infojobs.com.br/empregos.aspx?palabra=estagio+ti` → **200**, ~234 KB, **HTML estático com 20 vagas** em links `/vaga-de-<slug>__<id>.aspx` [V]. `__11893569` = **ID estável** [V]. Passou com `python-requests` e UA inventado [V].
- **Autenticação [V]:** nenhuma para listar.
- **robots.txt [V]:** só bloqueia páginas institucionais (`/static/Avisolegal.aspx`, etc.). **A busca não está bloqueada.**
- **Cobertura:** não medi o total (não achei contador na página) [V — a regex de "N vagas" não casou]. Resultados reais incluíam *"Estagiário TI"* (SP) e *"Analista BI Jr"* [V]. **Suspeita [P]:** volume nacional decente, **Brasília fraca**, e sobreposição alta com Vagas.com. **Como medir:** rodar a busca com `&provincia=` para DF e contar os `__<id>` distintos em 3 dias seguidos.
- **Campos [P/V]:** título, empresa, cidade, id no slug [V]. Salário e data provavelmente no detalhe [P, não abri detalhe].
- **Estabilidade [P]:** ASP.NET clássico, marcação envelhecida = raramente muda. Ponto a favor.

---

## 6. Indeed Brasil — **[V] bloqueado**

`GET https://br.indeed.com/jobs?q=estagio+ti&l=Brasilia` com UA de Chrome → **HTTP 403** [V]. Cloudflare/anti-bot ativo, sem negociação.

`robots.txt` [V]: no bloco `User-agent: *` há `Disallow: /viewjob?`, `Disallow: /rss`, `Disallow: /*?rss`, `Disallow: /api/getrecjobs` — **as páginas individuais de vaga estão explicitamente bloqueadas**, e há um bloco separado que aplica `Disallow: /jobs`, `Disallow: /q-`, `Disallow: /viewjob` a ~20 bots de IA (`GPTBot`, `ClaudeBot`, `CCBot`, `anthropic-ai`, `Scrapy`, …) [V].

Cobertura seria excelente. **Não importa: é 403 na primeira requisição.** Contornar isso exige headless browser + rotação de IP residencial, o que custa dinheiro (viola R$ 0/mês) e é a definição de "burlar controle de acesso".

**Descartado.**

---

## 7. Catho

- **Acesso [V]:** `GET https://www.catho.com.br/vagas/estagio-ti/` com UA de browser → **200**, 295 KB, **17 links de vaga** parseáveis [V]. Funcionou, ao contrário do Indeed.
- **robots.txt [V]:** bloco `User-agent: *` traz `Disallow: /buscar/vagas/` — o path que eu usei (`/vagas/…`) **não** está na lista, mas a intenção do site é claramente restringir busca automatizada. Curiosamente, o arquivo tem um bloco `Allow: /` nomeando `GPTBot`, `Claude-Web`, `anthropic-ai`, `PerplexityBot` etc. — o oposto do Vagas.com [V].
- **Cobertura [P]:** grande, mas a Catho é um jardim murado: muita vaga tem empresa oculta, descrição truncada e exige assinatura paga para ver o essencial. Para um bot que só notifica, isso degrada muito o valor do alerta.
- **Veredito:** tecnicamente acessível, mas **baixo valor por vaga** e ToS hostil. Fica na reserva, não na largada.

---

## 8. Trampos.co

- **Acesso [V]:** `GET https://trampos.co/oportunidades/` → **200**, mas **0 links de vaga no HTML** — é um SPA Ember (`frodo-*.js`, `vendor-*.js` no CDN) [V]. HTML estático inútil.
- **API [V]:** `https://trampos.co/api/opportunities` existe e responde **200** com `{"error":"No autorizado","api_key":null,"api_secret":null}` — **API real, com chave, e eu não tenho chave** [V]. `/api/v1/opportunities` e `/oportunidades/api/search` → 404 [V]. `oportunidades.json` → 500 [V].
- **robots.txt [V]:** permissivo (`Disallow:` vazio, só `/admin/` bloqueado).
- **Veredito:** ou consegue a `api_key` (pode ser gratuita mediante cadastro — **não verifiquei**), ou precisa de headless browser. Cobertura de TI é média e mistura muito Comunicação/Marketing. **Descartado da largada**; a pista da `api_key` vale 15 minutos de investigação futura.

---

## 9. Coodesh, GeekHunter, Sólides, 99jobs, Remotar

Rodada de sondagem [V, todos testados hoje]:

| Fonte | Resultado | Veredito |
|---|---|---|
| **Coodesh** (`coodesh.com/jobs`) | 200, 98 KB, **0 links de vaga no HTML** — SPA. `api.coodesh.com` existe mas `/v1/jobs`, `/api/v1/jobs`, `/v1/vacancies` → **404 com `{"message":"Cannot GET …"}`** (NestJS) [V] | API existe, path desconhecido. Achável lendo o bundle JS. Volume de estágio é baixo [P]. Fora da largada. |
| **GeekHunter** (`/vagas`) | 200, 302 KB [V] | Modelo é *reverso*: empresas buscam candidatos; não há mural navegável de vagas para bot. Além disso é focado em pleno/sênior [P]. Descartado. |
| **Sólides Vagas** (`vagas.solides.com.br`) | 200 na home; `/api/vagas` → **404 com página "Falha ao carregar página"** [V] | Segundo maior ATS do Brasil depois da Gupy. Vale uma segunda investida (achar o endpoint no bundle, como fiz na Gupy). **Melhor candidata a "4ª fonte"** [P]. |
| **99jobs** (`/oportunidades`) | 200, 37 KB [V] | Não investiguei parseabilidade. Volume de TI presumidamente pequeno [P]. |
| **Remotar** (`/vagas`) | **404** [V] | Path errado; site existe. Não persegui. |

---

## 10. Agregadores internacionais e repositórios GitHub

### 10.1 RemoteOK — **[V] API pública funciona, e é irrelevante**

`GET https://remoteok.com/api` → **200**, 371 KB, JSON com **100 vagas** e campos ricos (`id`, `slug`, `epoch`, `date`, `company`, `position`, `tags`, `description`, `location`, `apply_url`, `salary_min`, `salary_max`, `url`) [V]. O próprio JSON traz os termos: exige **link de volta com `follow`** e menção à fonte, sob pena de suspensão do acesso [V].

**Mas:** das 100 vagas, **2 mencionam Brazil** e as 7 classificadas como junior/intern são *"Room Attendant"*, *"Surveyor I"*, *"barber"*, *"factory labourer"*, *"Junior Crypto Trader"* [V]. Zero valor para estágio de TI no Brasil.

### 10.2 We Work Remotely — **[V] RSS funciona, e é irrelevante**

`GET https://weworkremotely.com/categories/remote-programming-jobs.rss` → **200**, 226 KB, **25 `<item>`** com `<title>`, `<region>`, `<category>`, `<description>` [V]. **Zero ocorrências de "Brazil" ou "Brasil" no feed inteiro** [V]. Primeira vaga: "Airtable: Senior Solutions Architect". É um board sênior, US-centric.

**Ambos descartados com evidência medida, não por intuição.** O eixo "remoto Brasil" do Luiz significa *empresa brasileira contratando remoto*, não *remote-first global em inglês* — são mercados diferentes.

### 10.3 Repositórios GitHub de vagas — **[V] técnica ótima, volume insuficiente**

A Issues API do GitHub é o acesso mais limpo de todo o inventário: JSON oficial, documentado, `state`, `created_at`, `labels`, `title`, `html_url`, id estável. Sem token: **60 req/hora** [V, medido no `/rate_limit`]; com PAT gratuito, 5.000/h [P].

Medição real de hoje [V]:

| Repo | Stars | Issues abertas | Criadas ≤30d | Criadas ≤90d | Júnior/estágio ≤90d |
|---|---|---|---|---|---|
| `backend-br/vagas` | 7.954 | 37 | **42** | 100+ | **3** |
| `frontendbr/vagas` | 15.370 | 27 | **17** | 33 | **1** |
| `dotnetdevbr/vagas` | 503 | 14 | 10 | 16 | **0** |
| `react-brasil/vagas` | 3.135 | 10 | — | — | último push **2024-01** [V] |
| `androiddevbr/vagas` | 836 | 4 | — | — | último push **2023-01** [V] |
| `qa-brasil/vagas` | 757 | 17 | — | — | último push **2023-08** [V] |
| `soujava/vagas`, `python-brasil/vagas`, `datascience-brasil/vagas` | — | — | — | — | **404 — não existem** [V] |

Os labels são estruturados e úteis (`['Pleno','CLT','PJ','Remoto','Alocado','São Paulo','Híbrido']`) [V] — dá para filtrar remoto/senioridade direto no label.

**O veredito é o número da última coluna: 4 vagas júnior/estágio em 90 dias, somando os três repos ativos.** Isso é ~1 vaga a cada 3 semanas. Não sustenta um bot diário sozinho.

**Mas é a fonte de menor custo e menor risco do inventário inteiro** (API oficial, sem ToS hostil, sem anti-bot, sem HTML frágil). O papel dela é **complementar**: adicionar cobertura de vagas que não passam por ATS, a custo quase zero.

---

## 11. Canais públicos de Telegram — **[V] técnica confirmada, canais precisam de curadoria**

A técnica: `https://t.me/s/<canal>` devolve o *preview web* do canal em **HTML estático**, sem API, sem token, sem entrar no canal [V]. Cada post vem em `tgme_widget_message_wrap` com `data-post="Canal/1234"` (**ID estável**) e `<time datetime="...">` [V]. Devolve os **~20 posts mais recentes** [V].

Canais testados hoje:

| Canal | HTTP | Posts | Post mais recente | Veredito |
|---|---|---|---|---|
| **`t.me/s/CafeinaVagas`** ("Iniciantes em TI") | 200 | 20 | **2026-08-13** [V] | **Ativo e no alvo exato.** Hashtags mais frequentes nos 20 posts: `#estagio` (14×), `#remoto` (9×), `#hibrido` (7×), `#dados` (5×), `#presencial` (5×), `#tecnologia` (5×) [V]. ~20 posts em 30 dias ≈ **5/semana**. Posts já vêm taggeados por modalidade e UF. |
| `t.me/s/VagasBRTI` ("Vagas de TI Brasil", mantido pelo PHPDF) | 200 | 20 | **2026-04-13** — 4 meses parado [V] | Tags: `#pj`, `#pleno`, `#remoto`, `#sap`, `#docker` — perfil sênior/PJ [V]. Morto. |
| `t.me/s/vagaumdev` | 200 | 20 | **2026-01-12** — 7 meses parado [V] | Morto. |
| `t.me/s/canalcasadodev` | 200 | 20 | recente [V] | Mistura conteúdo editorial com vagas (último post era artigo sobre IA) — ruído alto. |
| `t.me/s/backendbr` | 200 | 2 | — [V] | Pouco conteúdo no preview. |
| `t.me/s/tivagas`, `vagasdeti`, `vagastech`, `vagas_ti_brasil`, `frontendbr`, `vagasremotasbrasil` | **302** | 0 | — [V] | Não existem, ou são grupos (sem preview web), ou têm preview desabilitado. |

**Lição:** ~metade dos canais que aparecem em listas de blog está morta ou não é um canal. **Curadoria de canal é trabalho manual e precisa de re-verificação periódica** — um canal que parou de postar vira uma fonte que retorna "0 vagas hoje" para sempre, indistinguível de um scraper quebrado. Isso conecta direto ao item "Resiliência a quebra de fonte" do mapa.

**Contraponto forte:** o conteúdo é **texto livre não-estruturado**. Extrair título/empresa/link/modalidade de um post de Telegram cheio de emoji é parsing heurístico, muito mais frágil que qualquer HTML. E há **duplicação massiva** — esses canais em boa parte republicam vagas da Gupy e do LinkedIn [P].

---

## 12. Fontes não investigadas (e por quê)

- **CIEE** — `api.ciee.org.br/vagas/v1/vagas` responde **HTTP 401 `"Full authentication is required"`** [V]. API real, fechada. Portal exige conta de estudante [P]. Alto valor potencial para estágio; custo de entrada alto.
- **Nube** — site existe, mas `/vagas`, `/estagios`, `/vagas-de-estagio` todos **404** [V]. Não achei o path da busca. Presumo login-gated [P].
- **Abler** (`abler.com.br/vagas`) → **404** [V]. É ATS white-label; as vagas vivem em subdomínios de cliente, não num portal central [P].
- **ATS de página de carreira** (Greenhouse, Lever, Workable): `https://boards-api.greenhouse.io/v1/boards/<empresa>/jobs` → **200 com JSON completo, sem auth** [V, testado com `dropbox`]. `api.lever.co/v0/postings/<empresa>` também é público [V, o 404 que recebi foi porque `netflix` não usa Lever — o formato de erro `{"ok":false,"error":"Document not found"}` confirma que a rota existe]. **São as APIs mais limpas que existem** — mas exigem uma *lista curada de empresas*, e a esmagadora maioria das empresas brasileiras usa Gupy/Sólides, não Greenhouse/Lever. Vale como fase 2, se surgirem empresas-alvo específicas.
- **SINE / Empregabrasil, Trabalha Brasil** — Trabalha Brasil tem robots que bloqueia `ClaudeBot`/`GPTBot` mas libera bots de busca [V]. Volume de TI júnior baixo [P]. Não perseguido.

---

## 13. Sub-pergunta: o que muda ao incluir **júnior** além de estágio?

Não é só volume. **Muda a mecânica de filtragem, e essa é a descoberta que mais impacta o design do bot.**

**1. Estágio é um campo; júnior é uma palavra.** Na Gupy, `type=vacancy_type_internship` é um **enum do banco de dados deles** — a classificação é feita pela empresa que publicou, é confiável e completa [V]. Já "júnior" **não existe como campo** na Gupy [V]: só sobra `jobName=junior`, que casa no título. Isso quer dizer que toda vaga júnior cujo título não contém a palavra ("Desenvolvedor Java", "Analista de Suporte", "Pessoa Desenvolvedora Back-end") **é invisível** para esse filtro. Não sei o tamanho desse buraco — **é o maior desconhecido deste relatório**. Estimar exige amostrar N vagas `type=effective` e ler a descrição atrás de "1 ano de experiência" / "sem experiência". Aqui, sim, um classificador vale a pena — mas o mapa colocou "ranking por IA" fora de escopo, e concordo: **isso é v2**.

**2. Júnior traz falso positivo pesado.** `jobName=junior` sem filtro de área devolve *"Pessoa Advogada Júnior | Propriedade Intelectual, Tecnologia e Proteção de Dados"* e *"Analista de Desenvolvimento Imobiliário Júnior"* [V] — que casam com regex de TI por causa de "Tecnologia" e "Desenvolvimento". Já `type=internship` é ruidoso de outro jeito: devolve *"Estágio em Pedagogia"* e *"Estágio em Psicologia"* [V], que são fáceis de excluir. **O filtro de "é TI?" precisa ser mais esperto para júnior do que para estágio.**

**3. As duas categorias ficam em lugares diferentes.** Programathor tem **os dois como filtro estruturado** (`contract_type=Estágio`, `expertise=Júnior`) [V] — é a única fonte assim, e isso a torna desproporcionalmente valiosa apesar do volume modesto. GeekHunter é pleno/sênior e não serve para nenhum dos dois [P]. CIEE/Nube são **exclusivamente estágio** [P]. Repositórios GitHub e RemoteOK/WWR são majoritariamente pleno/sênior [V — ver §10]. O canal CafeinaVagas é o único do Telegram que se posiciona em "iniciantes" [V].

**4. Volume: júnior remoto ≈ estágio remoto.** Na Gupy: 49 estágios remotos vs. 46 júniors remotos ativos; 10 vs. 9 vagas de TI publicadas nos últimos 7 dias [V]. Praticamente **dobra** o fluxo. Já **em Brasília a assimetria é gritante**: 47 estágios ativos (25 TI pelo título) contra **11 júniors, dos quais ZERO de TI** [V]. Brasília é, pela Gupy, uma praça de estágio — vaga júnior de TI em Brasília ou não usa Gupy, ou não põe "júnior" no título, ou realmente não existe em volume relevante. **Essa é a razão mais forte para não depender só da Gupy no recorte DF** — e é exatamente onde o Vagas.com brilha (58 vagas de TI em Brasília [V]).

**Recomendação de escopo:** trate **estágio** e **júnior** como dois pipelines com regras distintas de filtro, não como um `OR` numa query. Estágio é um problema resolvido por campo estruturado; júnior é um problema de classificação de texto e vai ter recall ruim no v1 — e tudo bem, desde que isso seja uma decisão consciente e não uma surpresa.

---

## 14. Comparativo consolidado

| Fonte | Acesso | Login | robots/ToS | Cobertura remoto | Cobertura DF | Senioridade estruturada | Estabilidade | Custo |
|---|---|---|---|---|---|---|---|---|
| **Gupy** | **JSON [V]** | não | robots libera; ToS ambíguo | boa [V] | **boa p/ estágio, nula p/ júnior** [V] | estágio sim, júnior não [V] | média (host já mudou) | R$0 |
| **Programathor** | HTML estático [V] | não | robots libera + sitemap | boa [V] | fraca [P] | **estágio E júnior [V]** | média | R$0 |
| **Vagas.com** | HTML estático [V] | não | `*` liberado, IA bloqueada [V] | fraca [V] | **boa [V]** | não | média | R$0 |
| **LinkedIn guest** | HTML fragment [V] | não | **`Disallow: /jobs-guest/` [V]** | **excelente** | boa [V] | não | **baixa** | R$0 |
| **InfoJobs** | HTML estático [V] | não | busca liberada [V] | média [P] | fraca [P] | não | **alta** | R$0 |
| **GitHub Issues** | **API oficial [V]** | opcional | livre | boa | nula | labels [V] | **alta** | R$0 |
| **Telegram `t.me/s/`** | HTML estático [V] | não | livre | média [V] | média [V] | hashtags [V] | baixa (canal morre) | R$0 |
| **Indeed** | **403 [V]** | — | bloqueia vaga individual [V] | — | — | — | — | ✗ |
| **Catho** | HTML [V] | não p/ listar | `/buscar/vagas/` bloqueado [V] | média | média | não | média | dados truncados |
| **Trampos** | SPA; API com chave [V] | **api_key** | robots libera | fraca | fraca | não | — | ✗ |
| **Coodesh / Sólides** | SPA, API não localizada [V] | não | — | ? | ? | ? | — | investigar |
| **RemoteOK / WWR** | **API/RSS [V]** | não | exige backlink [V] | **irrelevante p/ BR [V]** | nula | não | alta | ✗ |
| **CIEE** | **API 401 [V]** | **sim** | — | nula | boa [P] | só estágio | — | alto atrito |
| **GeekHunter / 99jobs / Remotar / Nube / Abler** | não resolvido [V] | — | — | — | — | — | — | fora |

---

## 15. Recomendação: 3 fontes para começar

> A decisão é do ticket **"Fechar fontes e stack"**. O que segue é recomendação com justificativa, não decisão.

### 🥇 1. Gupy — `employability-portal.gupy.io/api/v1/jobs`

**Por quê:** é a única fonte do inventário que é **JSON de verdade, sem login, sem rate limit observado (30/30 requisições OK), com paginação e contador total, com `id` inteiro estável e `publishedDate` com timestamp** [V]. Ela sozinha resolve os dois eixos: `workplaceType=remote` e `state=Distrito Federal`. E entrega ~3–4 vagas de TI novas por dia no recorte do Luiz [V].

**Peso pedagógico (a regra "primeira vez é sua"):** começar por JSON é a escolha certa pedagogicamente. O Luiz digita o primeiro coletor sem ter que lidar com seletores CSS ao mesmo tempo — o problema é *chamar HTTP, parsear JSON, achar o id, guardar*. Puro e ensinável. O scraper de HTML (que é mais difícil) vem depois, como segunda ocorrência da técnica.

**Risco assumido:** a cláusula de ToS sobre "agregar/copiar" e o fato de a API poder mudar de host de novo. Mitigação: volume baixo, uso pessoal, sem republicação, e um alarme que grite quando o schema mudar.

### 🥈 2. Programathor — `programathor.com.br/jobs?contract_type=Estágio` e `?expertise=Júnior`

**Por quê:** é a **única fonte com senioridade e tipo de contrato como campo estruturado** [V]. Isso ataca frontalmente a fraqueza número 1 da Gupy (júnior não é filtrável) sem precisar de classificador de texto. É 100% TI, então o filtro "é TI?" some. HTML estático, sem JS, sem Cloudflare challenge, robots.txt convidativo com sitemap `changefreq: daily` [V]. E o detalhe traz JSON-LD `JobPosting` com `datePosted` [V] — parsing padronizado, não gambiarra.

**Peso pedagógico:** é o **primeiro scraper de HTML** do projeto — a técnica que o mapa mais quer que o Luiz digite. E ele começa no modo fácil (HTML estático, seletores simples), não no modo pesadelo.

**Risco assumido:** listagens parecem conter vagas encerradas [V] — o filtro por `datePosted` é obrigatório. Cobertura fraca de Brasília.

### 🥉 3. Vagas.com.br — `/vagas-de-ti-em-brasilia` + `/vagas-de-estagio-em-brasilia`

**Por quê:** exclusivamente para **cobrir o buraco de Brasília**. A Gupy dá 47 estágios e **zero júnior de TI** no DF; o Vagas.com dá **58 vagas de TI em Brasília e 49 de estágio em Brasília** [V]. Sem essa fonte, o eixo "presencial/híbrido em Brasília" do mapa fica descoberto — e é metade do requisito do usuário. O `<h1>` traz o total explícito [V], o que dá um **canary de graça**: se o `<h1>` sumir ou zerar, o scraper quebrou. Isso alimenta direto o item "Resiliência a quebra de fonte" do mapa.

**Risco assumido:** paginação não resolvida [V] — aceitável porque 3 das 4 buscas relevantes cabem na primeira página. E o robots bloqueia bots de IA nominalmente: **use um User-Agent próprio e honesto, nunca um que se pareça com `ClaudeBot`/`GPTBot`** [V].

### Complemento quase-grátis (opcional, fase 1.5)

**GitHub Issues API** em `backend-br/vagas` + `frontendbr/vagas`. Volume ridículo — 4 vagas júnior/estágio em 90 dias [V] — mas o custo de implementação é de ~20 linhas contra uma API oficial documentada, sem ToS hostil e sem HTML para quebrar. É a fonte com melhor razão risco/esforço do inventário, mesmo com o pior volume.

---

## 16. Por que as demais ficam de fora

| Fonte | Motivo do descarte |
|---|---|
| **LinkedIn** | Tecnicamente é a **melhor** fonte que existe — funcionou de primeira, sem login, com filtro de 24h e de remoto [V]. E é a única que eu recomendo **não usar**. O `robots.txt` nomeia `Disallow: /jobs-guest/` e o cabeçalho do arquivo proíbe acesso automatizado em texto explícito [V]. Não é zona cinzenta como a Gupy: é uma placa de "proibido" no caminho exato. Some a isso a fragilidade (endpoint não-documentado, o mais provável de quebrar) e o risco assimétrico: no dia em que alguém "melhorar" o coletor colando um cookie de sessão, o custo de errar deixa de ser um IP bloqueado e passa a ser a conta profissional do Luiz. **Reavaliar só se as três fontes escolhidas se mostrarem insuficientes na prática — e nunca com cookie de sessão.** |
| **Indeed** | **403 na primeira requisição** [V]. Contornar exige headless + IP residencial = custa dinheiro (viola R$ 0/mês) e configura burla de controle de acesso. |
| **Catho** | Acessível [V], mas empresa oculta e descrição truncada sem assinatura paga tornam o alerta pouco acionável. robots restringe busca. Reserva. |
| **RemoteOK / We Work Remotely** | Descartados **com medição, não com intuição**: 2 menções a "Brazil" em 100 vagas do RemoteOK, e **zero** no feed inteiro do WWR [V]. São boards sênior, globais, em inglês. O "remoto" que o Luiz quer é empresa brasileira contratando remoto — outro mercado. |
| **Trampos.co** | SPA; API real mas exige `api_key`/`api_secret` que não tenho [V]. Cobertura de TI diluída com Comunicação/Marketing. A pista da chave vale 15 min no futuro. |
| **Coodesh / Sólides / GeekHunter / 99jobs / Remotar** | SPAs cujo endpoint eu não localizei nesta sessão [V]. **Sólides é a mais promissora** (2º maior ATS do Brasil) e merece o mesmo tratamento que dei à Gupy — ler o bundle JS atrás do endpoint. GeekHunter é modelo reverso e pleno/sênior: descartada de vez. |
| **CIEE / Nube** | CIEE tem API real que responde **401** [V]; exige conta de estudante. Alto valor para estágio, mas atrito de autenticação incompatível com "bot que roda sozinho todo dia". |
| **Greenhouse / Lever / Workable** | APIs públicas e limpíssimas, confirmadas [V] — mas exigem lista curada de empresas, e o mercado brasileiro está na Gupy/Sólides. Fase 2, se aparecerem empresas-alvo. |
| **Telegram (canais)** | **Não descartado — adiado.** A técnica `t.me/s/<canal>` está verificada e funciona [V], e o **CafeinaVagas** é o canal mais alinhado ao perfil que encontrei (ativo em 2026-08-13, `#estagio` em 14 dos 20 últimos posts) [V]. Mas: texto livre com emoji é o parsing mais frágil de todos, há duplicação alta com Gupy/LinkedIn, e metade dos canais de listas públicas está morta [V — 2 dos 5 testados parados há 4 e 7 meses]. Entra depois que o pipeline estruturado estiver de pé e a deduplicação existir. |

---

## 17. Perguntas que ficaram abertas (para o ticket de decisão)

1. **Qual o tamanho do buraco "júnior sem a palavra júnior no título"?** É o maior desconhecido daqui. Medir: amostrar 200 vagas Gupy `type=vacancy_type_effective` de TI e ler a descrição atrás de sinais de entrada (0–2 anos, "sem experiência", "primeira oportunidade").
2. **Paginação do Vagas.com.** Resolver com a aba Network de um navegador; provavelmente é XHR de infinite scroll.
3. **Endpoint do Sólides Vagas.** Mesma técnica que usei na Gupy (ler `/_next/static/chunks/*.js`). Se existir, vira candidata forte a 4ª fonte.
4. **A `api_key` do Trampos é gratuita mediante cadastro?** 15 minutos de investigação.
5. **Vazão real.** Todos os números aqui são um snapshot de 2026-08-14. A medição honesta sai do próprio bot: contar IDs novos por dia, por fonte, durante 2–3 semanas. Recomendo instrumentar isso desde o primeiro dia — é o dado que vai dizer se 3 fontes bastam.
6. **Sobreposição entre fontes.** Não medi quanto Programathor e Vagas.com repetem o que a Gupy já tem. Importa para o ticket de deduplicação: se a sobreposição for alta, a identidade de vaga precisa ser (empresa + título normalizado), não só (fonte + id).
