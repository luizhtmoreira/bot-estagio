# Inventário de fontes de vagas

Type: research
Status: resolved
Blocked by: —
Parent: [Mapa: Bot de vagas de estágio/júnior em TI](../map.md)

## Question

Quais fontes de vagas de **estágio e júnior em TI** no Brasil são viáveis para coleta automatizada diária, e qual o custo/risco de cada uma?

Para cada fonte candidata (LinkedIn, Gupy, Programathor, Trampos, Vagas.com, Indeed, Solides/Vagas de ATS, InfoJobs, Catho, agregadores tipo RemoteOK/We Work Remotely, repositórios de vagas no GitHub, canais públicos de Telegram), levantar:

1. **Acesso técnico**: existe API pública? API interna/JSON acessível sem login? HTML estático parseável? Ou exige navegador headless com JS?
2. **Autenticação**: precisa de login? Se sim, o login pode ser automatizado sem risco à conta?
3. **Termos de uso**: o ToS proíbe scraping explicitamente? Qual o risco real (bloqueio de IP, banimento de conta, exposição legal)? Existe `robots.txt` relevante?
4. **Cobertura**: a fonte tem volume real de estágio/júnior de TI em (a) remoto Brasil e (b) Brasília/DF? Estimativa de vagas/semana.
5. **Campos disponíveis**: quais dados a fonte expõe por vaga (título, empresa, local, modalidade, data de publicação, link, id estável). Isso alimenta diretamente o ticket de identidade de vaga.
6. **Estabilidade**: a fonte tem histórico de mudar estrutura com frequência?

**Sub-pergunta embutida:** o que muda ao incluir vagas **júnior** além de estágio? Só volume, ou algumas fontes são exclusivas de um ou de outro?

**Entregável:** um comparativo em Markdown com recomendação de 2–3 fontes iniciais e o motivo de descartar as demais. Não decidir sozinho — a decisão é do ticket "Fechar fontes e stack".

## Answer

Comparativo completo em [`research/01-fontes.md`](../research/01-fontes.md). Método: ~60 requisições HTTP reais contra as fontes, cada achado marcado `[V]` verificado ou `[P]` presumido.

### Fontes viáveis

**Gupy — API JSON pública, sem login.** O endpoint que circula em tutoriais (`portal.api.gupy.io`) está morto (404). O real é `https://employability-portal.gupy.io/api/v1/jobs`, descoberto lendo os chunks JS do bundle Next.js. Sem token, sem rate limit observado (30 requisições seguidas → 30× HTTP 200). Filtros `type=vacancy_type_internship`, `workplaceType=remote`, `state=Distrito Federal`; devolve `pagination.total` e `publishedDate`. Medido: 49 estágios remotos ativos, 47 estágios no DF, 46 júniors remotos → **~3–4 vagas de TI novas/dia** no recorte.

**Programathor — HTML estático.** `robots.txt` convidativo. Única fonte com **senioridade e tipo de contrato como campo estruturado** (`?expertise=Júnior`, `?contract_type=Estágio`). JSON-LD com `datePosted` nas páginas de detalhe.

**Vagas.com — cobre o buraco de Brasília.** 58 vagas de TI em Brasília. Importante: a Gupy tem **zero** júnior de TI no DF, então essa fonte não é redundante. O `<h1>` traz o total, o que dá um canary de quebra de graça.

**GitHub (repos de vagas) — complemento opcional.** Volume péssimo (4 vagas júnior/estágio em 90 dias nos repos ativos; 3 de 9 repos testados nem existem, outros 3 parados desde 2023–24), mas custo e risco quase zero.

**Telegram (`t.me/s/<canal>`) — técnica verificada.** Dos 5 canais testados, 2 mortos há 4 e 7 meses; **CafeinaVagas** ativo e no alvo (`#estagio` em 14 dos últimos 20 posts).

### Descartadas

- **LinkedIn** — o endpoint `jobs-guest` funciona sem login (e tem uma pegadinha: `location=Brasil` é ignorado em silêncio e devolve vagas de Miami; o correto é `Brazil`). **Não usar mesmo assim:** `robots.txt` tem `Disallow: /jobs-guest/` literal e o cabeçalho proíbe acesso automatizado.
- **Indeed** — 403 na primeira requisição.
- **RemoteOK / We Work Remotely** — descartados com medição: 2 menções a "Brazil" em 100 vagas; zero no feed inteiro do WWR.

### Ordem recomendada

Gupy (JSON, começa fácil) → Programathor (primeiro scraper de HTML, resolve o júnior) → Vagas.com (cobre Brasília).

### O achado que mais afeta o design

**Estágio é um campo de banco; júnior é uma palavra no título.** Na Gupy, `vacancy_type_internship` é confiável e estruturado. Não existe equivalente para júnior — a senioridade só aparece no texto do título. Consequência: **vaga júnior sem "júnior" no título é invisível**, e o tamanho desse buraco não foi possível dimensionar. É a maior incerteza do relatório.

Recomendação do relatório: tratar como **dois pipelines com regras de filtro distintas**, não como um `OR` num filtro só. Isso vai direto para o ticket de modelo de domínio.

### Limites declarados

Onde não foi possível medir — LinkedIn, InfoJobs, e a **sobreposição entre fontes** (quantas vagas aparecem em duas delas) — o relatório diz que não mediu e explica como medir. Seis perguntas abertas ficaram registradas para o ticket de decisão.
