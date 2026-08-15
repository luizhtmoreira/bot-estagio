# Inventário de fontes — parte 2: agentes de integração e demais fontes

Ticket: [10-agentes-de-integracao-e-demais-fontes](../issues/10-agentes-de-integracao-e-demais-fontes.md) · Parte 1: [01-fontes.md](./01-fontes.md) · Mapa: [Bot de vagas](../map.md)
Data da apuração: **2026-08-14**. Perfil-alvo: estágio **e** júnior, qualquer área de TI (incluindo **dados e backend Python**, por [09-objetivo-de-carreira](../issues/09-objetivo-de-carreira.md)), **remoto Brasil** + **presencial/híbrido em Brasília/DF**, orçamento **R$ 0/mês**.

## Como ler este documento

Mesma convenção da parte 1:

- **[V]** — **VERIFICADO** nesta sessão, com requisição HTTP real feita por mim em 2026-08-14.
- **[P]** — **PRESUMIDO**: inferência, leitura de ToS/robots, ou conhecimento prévio. Não medi.

Números de volume só aparecem quando eu de fato os contei. Onde não medi, digo isso e digo **como medir**.

**Aviso sobre os números:** todas as contagens são um *snapshot de um dia*. Contagem de "ativas" é o estoque, não o fluxo. "Publicadas ≤7d" é o melhor proxy de vazão que se tira de uma coleta só.

**Linha de base para comparar:** Gupy = **~3–4 vagas de TI novas/dia** no recorte (remoto BR + DF), 49 estágios remotos ativos, 47 estágios DF ativos, **zero júnior de TI em Brasília**.

**⚠️ Esta apuração foi interrompida por limite de contexto.** As fontes 12 a 16 do ticket estão **não investigadas** — ver seção final "Não investigado". Não há nada de memória neste documento: o que não foi medido está listado como não medido.

---

## Resumo executivo (o que muda)

Três descobertas que mexem no desenho do bot:

1. **A tese do ticket estava errada, e o dado é forte.** Os agentes de integração **não** dominam o estágio *de TI*. Eles dominam o estágio *administrativo*. Medido: CIEE tem 5.907 vagas e **67 de Informática (1,1%), ZERO em Brasília** [V]. Nube tem 3.629 e **40 de TI (1,1%), 1 em Brasília** [V]. É exatamente o cenário "5.000 vagas e 12 de TI" que o ticket pedia para detectar. O motivo estrutural: agente de integração é remunerado por convênio de contratação em massa (recepção, administrativo, atendimento) — TI vai direto para ATS da empresa.

2. **A exceção é Brasília, e são duas: Agiel e Super Estágios.** Agiel tem 26 vagas de TI no país e **7 delas no DF** (27%) [V]. Super Estágios tem 148 de TI e **9 no DF** [V], incluindo um lote do TRE-DF. Ambas são agências com forte presença no Centro-Oeste. Para o eixo "presencial em Brasília" — que a parte 1 identificou como o buraco da Gupy — isso é relevante.

3. **O achado maior do ticket não é um agente de integração: é o Sólides.** Achei a API pública (`apigw.solides.com.br/jobs/v3/portal-vacancies-new`), **73.355 vagas, sem login, sem token**, com **`seniorities` e `contractsType` como campo estruturado** — o que a parte 1 dizia existir só no Programathor. E ela mata o buraco de Brasília da Gupy: **409 vagas júnior em Brasília** contra **11 na Gupy (das quais zero de TI)** [V]. Isso fecha a pergunta aberta nº 3 da parte 1.

---

## Parte A — Agentes de integração

### 1. CIEE — **[V] API JSON pública encontrada; cobertura de TI péssima**

#### 1.1 Acesso técnico — **[V] JSON, sem login, sem token**

A parte 1 concluiu "API 401, fechada". **Isso estava certo sobre o endpoint errado.** `api.ciee.org.br/vagas/v1/vagas` de fato responde `401 {"message":"Full authentication is required"}` [V, reconfirmado hoje]. Mas esse não é o endpoint que a vitrine pública usa.

Achei o correto lendo o JS inline da página `portal.ciee.org.br/quero-uma-vaga/` (WordPress + jQuery, não Next.js — o código de busca está em texto claro no HTML):

```
GET https://api.ciee.org.br/vagas/vitrine-vaga/publicadas
    ?page=0&size=300&sort=codigoVaga,desc
```

→ **HTTP 200**, JSON no formato Spring Data Page: `{"content":[...], "totalElements":N, "totalPages":N, "pageable":{...}}` [V].

Parâmetros confirmados por leitura da função `getParametrosBusca()` + teste real [V]:

| Param | Valores | Observação |
|---|---|---|
| `tipoVaga` | `ESTAGIO`, `APRENDIZ` | `EFETIVO` → **HTTP 400** [V]. Só estágio e aprendiz. |
| `codigoMunicipio` | código IBGE (Brasília = `5300108`) [V] | obtido via `api.ciee.org.br/core/city/search?filter=BRASILIA` |
| `idAreaProfissional` | id numérico (Informática = **18**) [V] | lista em `api.ciee.org.br/core/professional-area?ativo=true&nivelEnsino=SU&queroUmaVaga=true` — **70 áreas, e só UMA é de TI** [V] |
| `nivelEnsino` | `SU` (superior) | |
| `codigoVaga` | id da vaga | busca direta |
| `page`/`size`/`sort` | Spring Data | |

Endpoints irmãos, todos 200 sem auth: `/core/city/search?filter=<texto>` e `/core/professional-area` [V].

Funciona com `User-Agent: BotVagasLuiz/1.0` (UA inventado), sem `Origin`, sem `Referer` [V].

#### 1.2 Autenticação — **[V] nenhuma para listar.** Candidatar-se exige conta em `ciee.app` (o botão "Tenho interesse" aponta para `ciee.app/login?codigoVagaPortal=<id>&acesso=VITRINE_VAGA`) [V]. Para um bot que só **notifica**, o login é irrelevante.

#### 1.3 ToS / robots

`portal.ciee.org.br/robots.txt` [V]:
```
User-agent: *
Disallow:                     ← libera tudo (bloco Yoast)
Sitemap: https://portal.ciee.org.br/sitemap_index.xml
```
O sitemap index não contém vagas (só posts/páginas WordPress) [V]. Não li os ToS textuais [P].

Rate limit: **15 requisições seguidas sem pausa → 15/15 HTTP 200 em 7,2s**, sem 429, sem captcha [V].

#### 1.4 Cobertura — **[V] o número que mata a fonte**

| Consulta | Total ativas |
|---|---|
| todas | **5.907** |
| `tipoVaga=ESTAGIO` | 4.874 |
| `tipoVaga=APRENDIZ` | 960 |
| `nivelEnsino=SU` | 2.453 |
| `codigoMunicipio=5300108` (Brasília) | **221** |
| `idAreaProfissional=18` (Informática) | **67** |
| **Informática + Brasília** | **ZERO** |

Baixei as **221 vagas de Brasília inteiras** e apliquei regex de TI sobre `areaProfissional` + `atividades`: **6 candidatas, todas falso positivo** (DETRAN-DF "acessar o SEI e digitalizar", Ministério da Pesca, escola bilíngue) [V]. **A CIEE não tem estágio de TI em Brasília hoje.**

Distribuição das 67 de Informática por UF: SP 25, RJ 9, BA 6, CE 4, GO 4, AM 3, e cauda longa [V]. **DF: 0.**

Áreas mais comuns no DF: Administrativa 57, Educação 33, Ensino Médio 18, Construção Civil 11, Contabilidade 11 [V].

**Não existe campo de modalidade remota.** Toda vaga tem `local.cidade`/`local.uf` preenchidos e não há flag de home office no objeto [V]. Para o eixo "remoto Brasil" do Luiz, a CIEE contribui com **zero**.

#### 1.5 Campos disponíveis — **[V] objeto real**

```json
{
  "codigoVaga": 6193464,
  "tipoVaga": "ESTAGIO",
  "nomeEmpresa": "DEFENSORIA PUBLICA DO ESTADO DE SAO PAULO",
  "areaAtuacao": null,
  "areaProfissional": "Administrativa",
  "bolsaAuxilio": 1375, "tipoAuxilioBolsa": "Mensal", "tipoValorBolsa": "FIXO",
  "beneficios": [{"codigo": 53, "beneficio": "Refeitório no local", "valor": 0}],
  "descricao": "Justiça",
  "local": {"bairro": "Centro", "cidade": "São Paulo", "uf": "SP", "cep": null},
  "tipoHorario": "A_COMBINAR", "horarioEntrada": null, "horarioSaida": null,
  "atividades": ["Auxiliar nas rotinas administrativas do setor", "..."],
  "requisitos": {"semestreInicio": 1, "semestreFinal": 10, "escolas": null},
  "nivelEscolar": "SU", "logo": null
}
```

**Duas ausências graves** [V]:
- **Não há título de vaga.** O que mais se aproxima é `areaProfissional` ("Administrativa"). Uma notificação de Telegram teria que ser montada como *área + empresa + cidade*.
- **Não há data de publicação.** Nenhum campo de data no objeto. A única aproximação de recência é `codigoVaga` crescente (`sort=codigoVaga,desc`) — dá para tratar "id maior que o último visto = nova", mas não dá para saber a idade de uma vaga na primeira coleta.
- `descricao` **não é a descrição da vaga**: é o CNAE da empresa ("Fabricação de artefatos de borracha") [V]. Quem carrega o conteúdo real é `atividades[]`.

Identidade: `codigoVaga` inteiro, estável e global [V].

#### 1.6 Estabilidade
API interna não documentada, endpoint descoberto em JS inline de WordPress [V]. O contrato é Spring Data padrão — quebra ruidosa (KeyError/404), não silenciosa [P]. O histórico de a CIEE ter dois hosts de API (`api.ciee.org.br/vagas/v1/*` autenticado e `/vagas/vitrine-vaga/*` público) sugere que o público é um recorte deliberado, o que é um bom sinal de estabilidade [P].

#### 1.7 Veredito
**Tecnicamente a melhor fonte de estágio do inventário inteiro** (JSON limpo, sem login, sem rate limit, 5.907 vagas). **E irrelevante para o Luiz**: 67 vagas de TI no Brasil, **zero em Brasília**, **zero remotas por construção**. Reavaliar só se o recorte mudar.

---

### 2. Nube — **[V] API pública encontrada; login é só cosmético; cobertura de TI péssima**

#### 2.1 Acesso técnico — **[V] JSON, sem login**

A parte 1 disse "site existe, `/vagas` 404, presumo login-gated". O site foi **reescrito em Vue + Vite** [V]. Dois caminhos, ambos abertos:

**(a) Sitemap dedicado de vagas** — o mais barato de todos:
```
GET https://www.nube.com.br/sitemap-vagas.xml   → 200, 649 KB, 3.499 <loc>
```
Dos quais **3.487 são `/detalhes-vaga/<id>/<slug>`** [V]. **O slug codifica área, cidade, UF e bolsa**: `.../detalhes-vaga/376243/vaga-de-estagio-em-engenharia-civil-mane-do-brasil-jundiai-sp-bolsa-de-1700-mais-beneficios`. Dá para filtrar TI e DF **sem abrir uma única página de detalhe** [V].
⚠️ O sitemap vem com `cache-control: max-age=31536000` (1 ano) e `x-gocache-cachestatus: HIT` [V] — **risco real de servir dado velho**. Não tem `<lastmod>` [V].

**(b) API interna do portal** — achada nos chunks Vite (`/assets/FiltroVagas-*.js`):
```
GET https://www.nube.com.br/api/portal/buscar_filtro_vagas
GET https://www.nube.com.br/api/portal/obter_opcoes_filtro_vagas
GET https://www.nube.com.br/api/portal/buscar-detalhes-vaga/json?id_vaga=<id>
```
`buscar_filtro_vagas` → **HTTP 200, 3,8 MB, todas as vagas de uma vez** (ignorou `limite`/`offset` que passei) [V].

**Login:** o componente Vue faz `if(!isLoggedIn){ window.location.href="/login/login-geral?redirect=..." }` — **mas a checagem é 100% client-side**. Chamei o endpoint anonimamente e recebi 200 com o payload completo [V]. **Login não é barreira para coleta**, só para candidatura.

Filtros disponíveis (de `obter_opcoes_filtro_vagas`, 200 sem login) [V]:
- `id_modalidade_atuacao`: **1 = Presencial, 2 = Home Office, 3 = Híbrido**
- `id_tipo_vaga`: 1 = Estágio, 2 = Efetivo, 3 = Aprendiz
- `id_nivel`, `id_curso_busca`, `texto_area`, `id_periodo`, `distancia_km`, `jornada_semanal`, `ano_conclusao`, `semestre_conclusao`, `inclusao`, `valor_minimo`, `id_vaga`

#### 2.2 Autenticação — **[V] nenhuma efetiva.** O gate de login existe no front-end e é contornado por chamar a API direto — não por burlar controle de acesso, mas porque o servidor simplesmente não exige nada [V].

#### 2.3 ToS / robots
`www.nube.com.br/robots.txt` [V]:
```
User-agent: *
Disallow: /estudantes/gestor/
Disallow: /empresas/gestor/
Disallow: /escolas/gestor/
Sitemap: https://www.nube.com.br/sitemap.xml
```
`/detalhes-vaga/` e `/api/portal/` **não estão bloqueados** [V]. Não li os ToS textuais [P].
Há um `report-uri` de CSP para `csp-report.softrh.com.br` [V] — irrelevante para bot server-side.

#### 2.4 Cobertura — **[V]**

A página server-rendered legada (`/estudantes/api/vagas`) exibe o contador oficial: **"6443 vagas abertas, em 2695 empresas"** [V]. A API anônima devolve **3.629** [V] e o sitemap **3.487** [V]. **A diferença de ~2.800 não foi explicada** — pode ser agrupamento, vaga exclusiva de perfil logado, ou cache. Registro como discrepância aberta.

Sobre as 3.629 que consegui medir:

| Corte | N |
|---|---|
| total | 3.629 |
| Estágio / Aprendiz | 3.199 / 430 |
| **Presencial** | **3.528** |
| **Híbrido** | **88** |
| **Home Office** | **13** ← treze, no Brasil inteiro |
| Brasília/DF (qualquer área) | **58** |
| **TI (por área no título)** | **40** (1,1%) |
| **TI + Home Office/Híbrido** | **5** |
| **TI no DF** | **2** |

As 2 de TI no DF [V]: *"Análise de Dados"* home office, R$ 1.800; *"Tecnologia da Informação"* presencial Brasília, **R$ 750,00**.

Áreas de TI existentes: Tecnologia da Informação 17, Análise de Dados 6, Suporte Técnico 5, Informática 4, Suporte/Help Desk 4, Suporte e Serviços 2, Desenvolvimento de Programas 2 [V]. Top áreas do portal: Administrativa 620, Atendimento ao Cliente 461, Comercial 244, Logística 163 [V].

#### 2.5 Campos — **[V]**
Da API: `id_vaga`, `titulo` (= área + " - " + id), `tipo_vaga`, `cidade`, `uf`, `local`, `bolsa_valor`, `id_modalidade_atuacao`, `beneficios[]` (com ícone), `url` (`/detalhes-vaga/<id>/<slug>`), `destaque`, `alta_procura`, `selo[]`, `regex_filtro` (string tipo `"|Administrativa||Estagio|Sao Paulo|SP"`).
**Não há data de publicação** [V]. Identidade: `id_vaga` inteiro sequencial [V] — serve como proxy de recência.

#### 2.6 Estabilidade
Site foi reescrito recentemente (Vue/Vite, hashes de bundle) [V] — sinal de que **acabou de quebrar uma vez** e pode quebrar de novo. Os nomes de chunk (`FiltroVagas-CpDYA1wp.js`) têm hash e mudam a cada deploy, mas o **path da API (`/api/portal/buscar_filtro_vagas`) não tem hash** — é o que se deve gravar no coletor [P].

#### 2.7 Veredito
Acesso tecnicamente fácil e login não é barreira. **Mas 13 vagas home office no país inteiro e 2 de TI no DF** tornam a fonte irrelevante para o recorte. Fora.

---

### 3. Agiel — **[V] listagem pública, detalhe atrás de login; melhor densidade DF/TI dos agentes**

#### 3.1 Acesso técnico — **[V] AJAX do OctoberCMS, sem login para listar**

`www.agiel.com.br` redireciona para `/site/` [V]. `/site/vagas` → 200, 79 KB [V]. É **OctoberCMS**: a busca é um POST para a própria URL da página com header de handler:

```
POST https://www.agiel.com.br/site/vagas
Headers: X-OCTOBER-REQUEST-HANDLER: onClickBuscar
         X-OCTOBER-REQUEST-PARTIALS: ajax_vagas_busca
         X-Requested-With: XMLHttpRequest
Body:    curso=<id>&estado=&cidade=
→ 200 application/json {"ajax_vagas_busca": "<html do resultado>"}
```
[V, testado com sucesso]

O HTML do resultado traz `Sua busca gerou N vagas de estágio.` — **contador explícito, canário de graça** [V].

**A busca exige um `curso`.** Não achei jeito de listar tudo sem curso [V]. O `<select name="curso">` da página tem **326 opções** com id numérico, extraíveis do HTML estático [V]. `onCursoChange` (que popula estado/cidade) devolveu **HTTP 500** quando chamei isoladamente [V] — não persegui.

#### 3.2 Autenticação — **[V] listagem pública, detalhe fechado**

Este é o ponto crítico da fonte. O botão "Saiba Mais" de cada card aponta para `https://www.agiel.com.br/site/entrar/<CODIGO>`, e essa página é **um formulário de login** — título `"Acesso do Estudante Cadastrado"`, texto *"Faça o login para se candidatar às vagas!"* [V].

**O que sobra sem login (suficiente para um alerta de Telegram):** código da vaga, lista de cursos aceitos, nome da empresa (às vezes genérico, tipo "COMÉRCIO VAREJISTA"), endereço/cidade/UF [V].
**O que fica atrás do login:** descrição, atividades, bolsa, horário.

#### 3.3 ToS / robots — **[V] não existe robots.txt**
`https://www.agiel.com.br/robots.txt` devolve **a home do site em HTML** (soft-404), não um robots [V]. Sem regra publicada, não há proibição explícita — nem permissão. A meta tag da página é `<meta name="robots" content="index,follow">` [V]. Não li os ToS textuais [P].

#### 3.4 Cobertura — **[V] medida rodando os 34 cursos de TI**

Extraí do `<select>` os **34 cursos de TI** (Análise e Desenvolvimento de Sistemas, Ciência da Computação ×2, Ciência de Dados ×2, Ciência de Dados e IA, Ciência de Dados e ML ×2, Engenharia de Software, Engenharia de Computação, Sistemas de Informação, Redes de Computadores, Segurança da Informação, Cibersegurança, Defesa Cibernética, Desenvolvimento Full Stack, BI, Informática, Tecnologia da Informação, Gestão da TI, Licenciatura em Computação, técnicos, etc.) e rodei uma busca para cada — **34 requisições, 0 erros, 38s** [V].

Contagens por curso (as maiores) [V]: Sistemas de Informação 18, Ciência da Computação 17, Ciências da Computação 14, Engenharia de Computação 14, Gestão da TI 8, Tecnologia da Informação 8, ADS 7, Ciência de Dados 6, Engenharia de Software 5, Redes 3. Vários zerados (Cibersegurança, BI, Full Stack, Informática, técnicos).

Como uma vaga aceita vários cursos, deduplicando pelo código:

| Métrica | Valor |
|---|---|
| **Vagas de TI únicas no Brasil** | **26** [V] |
| por UF | **MG 14, DF 7, ES 2, MA 1, RS 1, SP 1** [V] |
| ano no código | 2026 em 100% das 26 [V] |

**7 vagas de TI em Brasília** [V]: `DF2026000226`, `...315`, `...320`, `...329`, `...344`, `...353`, `...367`.

Escala geral da agência (amostra de cursos grandes) [V]: Administração 131, Administração de Empresas 129, Ensino Médio 53. Na união dessas amostras, a distribuição por UF foi **MG 23, DF 12, SP 3, BA 2** — confirmando que **Agiel é uma agência de Minas + Distrito Federal**, não nacional.
⚠️ O partial AJAX parece renderizar ~20 cards por resposta mesmo quando o contador diz 131 — **não resolvi a paginação** [V]. Para os cursos de TI isso não importou (todos ≤18).

**Não há campo/filtro de modalidade remota** [V]. Toda vaga tem endereço físico.

#### 3.5 Campos — **[V]**
Código (`DF2026000226`), lista de cursos aceitos, nome/razão da empresa, endereço com bairro e cidade/UF, link para `/site/entrar/<codigo>`.
**Identidade excelente:** o código é `<UF><ano><sequencial>` — traz **UF e ano embutidos**, e é sequencial por UF. Isso dá simultaneamente chave estável, filtro geográfico e sinal de recência sem nenhum campo de data [V].
**Não há data de publicação nem bolsa na listagem** [V].

#### 3.6 Estabilidade
OctoberCMS com tema Bootstrap antigo (o HTML ainda tem o menu de demo do template: "search jobs 1", "find a candidate 2") [V] — site que ninguém redesenha. Ponto a favor. Risco: o handler AJAX (`onClickBuscar`) e o nome do partial (`ajax_vagas_busca`) são internos e mudariam num refactor [P].

#### 3.7 Veredito
**Melhor razão TI/DF de todos os agentes de integração: 7 das 26 vagas de TI estão em Brasília (27%)**. Volume absoluto pequeno, mas é exatamente o buraco que a Gupy tem no DF. O login no detalhe degrada o alerta (sem bolsa, sem descrição) mas não o inviabiliza. Custo: 34 requisições/dia para cobrir TI.

---

### 4. Super Estágios — **[V] a melhor fonte técnica desta rodada entre os agentes**

#### 4.1 Acesso técnico — **[V] um único POST devolve a base inteira**

Achado no JS de `/index/js/vagasEstagio/vagasInteracao.js` [V]:

```
POST https://www.superestagios.com.br/index/comunicacaoAjax/vagas.php
Body: acao=listarAtivas&limite=0&geo=0&id_estado=&id_nivel_ensino=&id_curso=&id_vaga=&id_cidade=
→ 200, 5,9 MB, JSON array com TODAS as vagas ativas
```

⚠️ A resposta começa com o lixo `<!-- a:  -->` antes do `[` — **precisa fatiar a partir do primeiro `[`** antes do `json.loads` [V].

Endpoints irmãos, todos POST sem login [V]:
- `comunicacaoAjax/estados.php` (`acao=listar`) → 200, lista de UFs com `cod_estado`
- `comunicacaoAjax/cursos.php`

Filtros do próprio endpoint: `id_estado`, `id_cidade`, `id_curso`, `id_nivel_ensino`, `id_vaga`, `limite` [V]. Com `limite=0` vem tudo — **uma requisição por dia resolve a fonte inteira**.

#### 4.2 Autenticação — **[V] nenhuma.** A listagem completa, com atividades e bolsa, vem sem cookie e sem sessão [V]. Login (`/index/comunicacaoAjax/autenticaLogin.php`) só para candidatar-se.

#### 4.3 ToS / robots — **[V] robots incompleto, sem bloco `*`**
```
User-agent: Googlebot        → Allow: /
User-agent: AdsBot-Google    → Allow: /
User-agent: Googlebot-Image  → Allow: /
Sitemap: https://www.superestagios.com.br/sitemap.xml
```
**Não existe bloco `User-agent: *`** [V]. Pela convenção do REP, agente não listado não tem regra e não está proibido — mas o arquivo também não autoriza ninguém explicitamente. Zona cinzenta parecida com a da Gupy. Não li os ToS textuais [P].
O sitemap tem 210 URLs, quase todas `processoSeletivo/processo.php?v=<base64>` (processos seletivos de órgãos públicos), **nenhuma vaga individual** [V].

#### 4.4 Cobertura — **[V] a base inteira, contada**

| Corte | N |
|---|---|
| **Vagas ativas (total)** | **3.698** |
| por UF | SP 1.042, RJ 459, ES 442, **MT 406**, MG 228, SC 227, **DF 133**, RS 107 |
| Presencial / Híbrido / Home Office | **3.654 / 26 / 17** |
| **TI (por curso exigido)** | **148** (4,0%) |
| TI por UF | **MT 72**, SP 31, **DF 9**, RJ 7, ES 4, MG 4, RN 4 |
| TI presencial / híbrido / home office | 134 / 10 / 3 |
| com processo seletivo formal | 551 de 3.698 |

**As 9 vagas de TI no DF** [V] — note a concentração no TRE-DF:

| id_vaga | Cidade | Curso | Bolsa | Empresa |
|---|---|---|---|---|
| 313708 | Brasília | INFORMATICA | R$ 1.200 | TRE-DF |
| 313697 | Brasília | ENGENHARIA DE SOFTWARE | R$ 1.200 | TRE-DF |
| 313693 | Brasília | ENGENHARIA DA COMPUTAÇÃO | R$ 1.200 | TRE-DF |
| 313681 | Brasília | CIÊNCIA DA COMPUTAÇÃO | R$ 1.200 | TRE-DF |
| 313670 | Brasília | BANCO DE DADOS | R$ 1.200 | TRE-DF |
| 313651 | Brasília | ANÁLISE E DESENV. DE SISTEMAS | R$ 1.200 | TRE-DF |
| 313664 | Brasília | TÉCNICO EM INFORMÁTICA | R$ 650 | TRE-DF |
| 311158 | Asa Norte | GESTÃO DE TI / SIST. INFORMAÇÃO / SEGURANÇA | R$ 1.050 | Confidencial |
| 311790 | Águas Claras | REDES DE COMPUTADORES / SISTEMAS P/ INTERNET | R$ 900 | Confidencial |

⚠️ **Achado relevante para deduplicação:** 7 das 9 são do mesmo empregador (TRE-DF) e provavelmente do mesmo edital. Um bot ingênuo mandaria 7 notificações para o que é, na prática, um processo seletivo só.

⚠️ **O "HOME_OFFICE" da Super Estágios é falso remoto:** as 3 de TI home office têm cidade fixa (Piracicaba/SP, Maringá/PR ×2) [V]. É home office *da cidade tal*, não remoto Brasil.

#### 4.5 Campos — **[V] os mais ricos de todos os agentes**

43 campos por vaga. Objeto real:
```json
{"id_vaga":"314728","curso1":"DIREITO","curso2":"","curso3":"","cidade":"Jundiaí",
 "sgl_estado":"SP","valor":"3300.00","transporte":"12.30","nome_fantasia":"CONFIDENCIAL",
 "nivel_ensino":"Superior","modalidade":"PRESENCIAL","processo_seletivo":"0",
 "atividades":"Auxiliar nas atividades de: - Revisar contratos...","beneficios":"...",
 "requisito":"Entre o 4º e o 8º período","turno":"Matutino e Vespertino",
 "carga_horaria":"6","hora_flex":"Das 07h às 14h...","endereco":"Av. caminho de Goiás",
 "bairro":"Bairro dos Fernandes","qtd_vagas":"1","vaga_confidencial":"1",
 "exige_CNH":"Não","exige_EXP":"Não","id_empresa":"28827", ...}
```

Tem **modalidade estruturada** (`PRESENCIAL`/`HIBRIDO`/`HOME_OFFICE`), **bolsa**, **atividades completas**, **cursos exigidos**, **carga horária**, **turno** [V].
**Não há data de publicação** [V]. `id_vaga` é inteiro sequencial (faixa observada 260.828–315.787) → proxy de recência [V].
**Não há título de vaga** — o proxy é `curso1` [V].

#### 4.6 Estabilidade
PHP procedural clássico (`comunicacaoAjax/vagas.php`), jQuery 3.6, marcação antiga [V]. Esse tipo de stack raramente muda. Ponto forte. Contra: o payload de 5,9 MB numa requisição é pesado mas cabe folgado em free tier [P].

#### 4.7 Veredito
**Tecnicamente é a melhor das seis agências**: 1 requisição/dia, sem login, JSON completo com modalidade e bolsa estruturadas. **148 vagas de TI e 9 no DF** — o dobro da Agiel em TI nacional e mais que ela no DF. Candidata real a fonte do bot, com o cuidado de deduplicar lotes de mesmo empregador.

---

### 5. Cia de Talentos — **[V] API pública; volume ínfimo e metadado inútil**

#### 5.1 Acesso técnico — **[V] REST, POST, sem login**

O portal (`www.ciadetalentos.com.br`) é WordPress e manda o candidato para `vagas.ciadetalentos.com.br/applicant/` — um AngularJS 1.x antigo (ATS "Globe") [V]. Achei o endpoint em `resources/js/applicant/applicant-services-*.js`:

```
POST https://vagas.ciadetalentos.com.br/applicant/rest/applicant/authentication/filter
Content-Type: application/json
Body: {"locale":"pt"}
→ 200, JSON array
```
[V]. GET no mesmo path → **405 Method Not Allowed** [V], confirmando que a rota existe e só aceita POST.

#### 5.2 Autenticação — **[V] nenhuma.** O endpoint está sob `.../authentication/filter` mas é a busca pública pré-login [V].

#### 5.3 ToS / robots
`www.ciadetalentos.com.br/robots.txt`: bloco Yoast com `User-agent: * / Disallow:` — **libera tudo** [V]. Não verifiquei robots do subdomínio `vagas.` [não medido]. Não li ToS [P].

#### 5.4 Cobertura — **[V] 28 processos, e o metadado não serve**

**28 oportunidades abertas no total** [V]. E não são vagas: são **programas corporativos** (estágio/trainee).

Tipos: Estágio Superior 9, Trainee 9, Estágio Técnico 7, Ensino Médio 1, nulo 2 [V].

Exemplos reais [V]: *Trainee Itaú Unibanco 2027*, *Programa Estagiar Globo 2026*, *Nova Geração PwC 2026*, *Estágio PepsiCo First Gen 2026*, *Tech Analyst Fiserv 2026*, *Programa de Estágio Bayer*, *Programa Vale Trainee em Engenharia*.

**O problema que mata a fonte como dado estruturado:**
- `opportunityAreas` é **`"Área: Diversas"` em 26 das 28** [V]. Só 2 têm área real ("Operações", "Comercial / Vendas"). **Não dá para filtrar TI por campo.**
- `opportunityLocations` está majoritariamente vazio [V]. **Não dá para filtrar Brasília por campo.**
- Filtrar exigiria parsear o `opportunityDescription`, que é **HTML inteiro com estilos inline** [V].

Pelo título, **1 das 28 é claramente de TI** ("Tech Analyst Fiserv 2026") [V].

#### 5.5 Campos — **[V]**
`opportunityId`, `opportunityName`, `opportunityDescription` (HTML), `opportunityLocations`, `opportunityAreas`, `companyName`, `hiringType`/`hiringTypeId`, `opportunityHotsiteUrl`, `opportunityInscriptionUrl`, `inscriptionEnd`, **`daysRemainingForInscription`** ("Encerra hoje"), `countFinishDays`, `selectionProcessClassification`, `applicantRegistered`.
**Tem prazo de inscrição, não tem data de publicação** [V]. Identidade: `opportunityId` inteiro [V].

#### 5.6 Veredito
API limpa, sem login, mas **28 itens e metadados inutilizáveis**. Como o volume é minúsculo, seria viável mandar *todos* os programas novos para o Telegram sem filtro nenhum e deixar o Luiz ler os 28 títulos — mas isso é uma decisão de produto, não de coleta. Fora da largada; possível "fonte de programas de estágio" na fase 2, junto com a Cia de Estágios.

---

### 6. Companhia de Estágios — **[V] domínio do ticket está errado; é catálogo de programas**

#### 6.1 Achado de domínio
`companhiadeestagios.com.br` **não responde** — `curl` retorna `000` em https, http e www; o DNS resolve para `75.101.130.197` mas a conexão TCP não completa [V]. O domínio correto é **`www.ciadeestagios.com.br`** (título: *"Companhia de Estágios - Faz o amanhã"*) [V].

#### 6.2 Acesso técnico — **[V] sitemap de programas; portal de candidato é SPA**
- `www.ciadeestagios.com.br/robots.txt`: `User-agent: * ` sem nenhum `Disallow` + sitemap [V] — libera tudo.
- `sitemap-programas-de-estagio.xml` → **104 URLs** de programas (`/vagas/<empresa>/` e `/programas/<empresa>`), **com `<lastmod>`** (mais recentes: 2026-08-12, 2026-08-11, 2026-08-10) [V]. O `lastmod` é um sinal de recência utilizável.
- As páginas de programa são **redirects**: `/vagas/ericsson/` → 2,4 KB, corpo *"Redirecionando para a página de vagas..."*, **sem JSON-LD JobPosting** [V]. O conteúdo real vive em hotsites externos.
- O portal de candidato é `carreira.ciadeestagios.com.br` — **Next.js/Turbopack SPA**, `/vagas`, `/oportunidades` e `/pt-br/vagas` todos **404** [V]. **Não localizei a API.**

#### 6.3 Autenticação — não determinado. O portal tem `/entrar`, mas não cheguei a testar se a listagem exige login [não medido].

#### 6.4 Cobertura — **[V] 104 programas no sitemap.** Não medi quantos estão abertos, quantos são de TI, nem quantos aceitam Brasília ou remoto — as páginas não expõem esses campos [V].
**Como medir:** achar a API do `carreira.ciadeestagios.com.br` lendo os chunks `/_next/static/chunks/*.js` (mesma técnica da Gupy e do Sólides). Não fiz.

#### 6.5 Veredito parcial
Mesma categoria da Cia de Talentos: **catálogo de programas corporativos, não mural de vagas**. O sitemap com `lastmod` já daria um coletor pobre-mas-honesto ("programa novo publicado"). Volume de TI **não medido**.

---

## Parte B — Plataformas e agregadores

### 7. Sólides Vagas — **[V] O ACHADO DO TICKET. API pública, 73 mil vagas, senioridade estruturada**

Isto fecha a **pergunta aberta nº 3 da parte 1** ("Endpoint do Sólides Vagas — se existir, vira candidata forte a 4ª fonte"). Existe, e é forte demais para ser 4ª.

#### 7.1 Acesso técnico — **[V]**

`vagas.solides.com.br` é Next.js e o SSR **não traz vagas** (`pageProps` vazio; `/_next/data/<buildId>/vagas.json` devolve só `{"position":"..."}`) [V].

Achei a API lendo o bundle. **Detalhe técnico que custou tempo e vale registrar:** os chunks são servidos com `Content-Encoding: br` e o `curl --compressed` do sistema **não** descomprime (grava lixo binário). Precisei baixar o `.js` e rodar `brotli -d`; só aí o bundle de 430 KB virou 1,58 MB de texto pesquisável [V].

```
GET https://apigw.solides.com.br/jobs/v3/portal-vacancies-new?page=1
→ 200 {"success":true,"data":{"count":73355,"totalPages":7336,"currentPage":1,"data":[...]}}
```
[V]. Sem login, sem token, sem `Origin`, com UA inventado [V].

Variantes testadas [V]: `jobs/v3/portal-vacancy/portal-vacancies-new` → 404; `applicants-v2/jobs/v4/portal-vacancies-new` → **403 `Missing Authentication Token`** (essa é a fechada).

**Parâmetros confirmados por teste real** [V] — note que são **camelCase**, a versão snake_case é ignorada silenciosamente (retorna o total sem filtrar, que é a armadilha):

| Param | Valores | Efeito medido |
|---|---|---|
| `seniorities` | `estagio`, `junior`, `pleno`, `senior`, `especialista`, `principal` | `junior` → 15.202. **`estagio` → 0** (senioridade não é onde mora estágio) |
| `contractsType` | `estagio`, `aprendiz`, `clt`, `pj`, `temporario`, `autonomo`, `freelancer`, `cooperado` | **`estagio` → 2.869** |
| `jobsType` | `presencial`, `remoto`, `hibrido` | remoto 1.989 · híbrido 2.705 · presencial 68.665 |
| `occupationAreas` | `tecnologia`, `administrativo`, `agronegocio`, `comercial`, `compras`, `comunicacao`, `design`, `educacao`, `engenharia`, `financeiro`, `juridico`, `logistica`, `marketing`, `primeiro-emprego`, `producao`, `recursos-humanos`, `saude`, `turismo` | **`tecnologia` → 3.690** |
| `locations` | slug `cidade-uf` | **`brasilia-df` → 1.661**. `Brasília` e `Brasília-df` → 0 |
| `title` | texto livre | `desenvolvedor` → 999 |
| `page` | inteiro | **`limit` é ignorado — sempre 10 por página** [V] |

⚠️ **Armadilha séria:** parâmetro com nome errado **não dá erro** — devolve o total sem filtro. Um coletor que erre o nome vai achar que tem 73 mil vagas no recorte. O contador `count` deve ser validado contra um esperado.

#### 7.2 Autenticação — **[V] nenhuma.**

#### 7.3 ToS / robots — **[V] robots deliberadamente permissivo para vagas**
```
User-agent: Googlebot
Disallow: /nogooglebot/
# permite explicitamente rotas de vaga
Allow: /empresa/*/vaga
Disallow: /empresa/*$
User-agent: *
Allow: /
Sitemap: https://www.vagas.solides.com.br/sitemap.xml
```
[V]. O comentário em português *"permite explicitamente rotas de vaga"* é uma declaração de intenção difícil de interpretar contra o crawler. ⚠️ O sitemap anunciado no robots (`www.vagas.solides.com.br/sitemap.xml`) responde **404** [V]. Não li os ToS textuais [P].

#### 7.4 Cobertura — **[V] e é aqui que ela bate a Gupy no ponto fraco dela**

Comparação direta com os números da parte 1:

| Corte | **Sólides [V]** | Gupy (parte 1) [V] |
|---|---|---|
| total do portal | **73.355** | 82.023 |
| estágio (Brasil) | 2.869 | 2.915 |
| estágio remoto | **94** | 49 |
| estágio em Brasília | **91** | 47 |
| júnior remoto | **310** | 46 |
| **júnior em Brasília** | **409** | **11 (zero de TI)** |
| senioridade como campo | **SIM** | não |

Recorte de TI, usando `occupationAreas=tecnologia` (campo estruturado) [V]:

| Consulta | Ativas | Publicadas ≤7d |
|---|---|---|
| TI + estágio + remoto | 33 | 1 |
| TI + estágio + Brasília | 5 | 0 |
| TI + júnior + remoto | 69 | 7 |
| TI + júnior + Brasília | 15 | 0 |
| **união (deduplicada por id)** | **109** | **8** |
| TI + Brasília (qualquer senioridade) | 118 | — |
| TI + remoto (qualquer senioridade) | 505 | — |

**Vazão medida: 8 vagas de TI no recorte publicadas nos últimos 7 dias ≈ 1,1/dia** [V, snapshot único] — contra ~3–4/dia da Gupy. **Sólides não substitui a Gupy em vazão, mas cobre o que a Gupy não cobre** (júnior estruturado, júnior de TI em Brasília).

Exemplos reais colhidos das ≤7d [V]: *"Analista de Suporte JR - Noturno"* (remoto), *"ANALISTA DE SISTEMAS JR"* (remoto), *"Banco de Talentos | Área de Inteligência Artificial"*, *"Banco de Talentos | Área de Dados"*, *"Analista de Redes (CGR) - Júnior"*, *"Analista de Monitoramento (NOC) - Júnior"*, *"Estagiário em Geoprocentamento"*, *"Estágio de Desenvolvimento de Software"* (Brasília, presencial).

⚠️ **Cross-check honesto:** rodei também sem `occupationAreas`, aplicando regex de TI no título. O resultado foi **pior**, não melhor — a regex trouxe *"Estagiário(a) de Fisioterapia"* e *"Operador de loja em Samambaia Sul"* como TI [V]. Isso reforça o aviso da parte 1: **o campo estruturado é mais confiável que o regex de título**, e o número de 8/semana é o que vale.
⚠️ Não medi quanto `occupationAreas=tecnologia` **perde** (vaga de TI classificada em outra área). Isso é o análogo do buraco "júnior sem a palavra júnior" da parte 1, e continua aberto.

#### 7.5 Campos — **[V] os mais completos do inventário inteiro**

```json
{
  "id": 903765,
  "title": "CONSULTOR(A) DE VENDAS - O BOTICÁRIO - (VÁRZEA GRANDE)",
  "description": "<div>…HTML…</div>",
  "currentState": "em_andamento",
  "companyName": "Matos Comercio De Perfumes E Cosmeticos Ltda",
  "companyLogo": "https://…",
  "state": {"id": 25, "name": "Mato Grosso", "code": "MT"},
  "city":  {"id": 5314, "name": "Várzea Grande", "state_id": 25},
  "slug": "grupomatos",
  "redirectLink": "https://grupomatos.solides.jobs/vacancies/903765?origem=portal",
  "type": "externa",
  "homeOffice": false,
  "jobType": "presencial",
  "openPositions": 1,
  "salary": {"type":"simple","showRangeToApplicant":true,"initialRange":0,"finalRange":2310.62,"negotiable":false},
  "seniority": [{"id": 4, "name": "Junior"}],
  "recruitmentContractType": [{"id": 10, "name": "CLT"}],
  "benefits": [], "language": [], "hardSkills": [], "education": [],
  "occupationAreas": [],
  "affirmative": [{"id":351201,"name":"Vaga afirmativa para Pessoas Negras"}, …],
  "peopleWithDisabilities": false, "pcdOnly": false,
  "createdAt": "2026-08-14",
  "address": {"zip_code":"…","street_address":"…","neighborhood":"…","city":{…},"state":{…},"country":{…}}
}
```

O que ela tem e **nenhuma outra fonte do inventário tem junta** [V]:
- **`seniority` estruturado** (`Estagiário` / `Junior` / …) — a parte 1 dizia que só o Programathor tinha, e o Programathor é um board pequeno.
- **`recruitmentContractType` estruturado** (`Estágio` / `CLT` / …).
- **`createdAt` em data ISO** — resolve "é nova?" sem diff.
- **`salary` com faixa numérica** — a Gupy não tem salário nenhum.
- `jobType` + `homeOffice` explícitos.
- `city`/`state` com id IBGE-like **mesmo em vaga remota** (a Gupy zera cidade/estado em remoto).
- `hardSkills`, `language`, `education`, `affirmative`, `benefits` como listas.

Identidade: `id` inteiro global. `redirectLink` leva ao `*.solides.jobs` da empresa [V].

#### 7.6 Estabilidade
API interna não documentada, sob API Gateway (`apigw.`) com versionamento no path (`jobs/v3`) [V]. Versionamento explícito é o melhor sinal de estabilidade que se pode pedir de API interna [P]. A convivência de `v3` (aberta) e `applicants-v2/jobs/v4` (403) sugere migração em curso — **a v3 pode ser depreciada** [P].
Quebra seria ruidosa (404/`success:false`), exceto pelo caso silencioso do parâmetro renomeado [V].

#### 7.7 Veredito
**Deveria entrar na largada, não na fase 2.** É a única fonte do inventário inteiro (parte 1 + parte 2) que resolve simultaneamente: JSON limpo, sem login, senioridade estruturada, data de publicação, salário, e **cobertura de júnior em Brasília** — o buraco que a parte 1 identificou como o mais grave da Gupy.

---

### 8. Eureca — **[V] API pública encontrada; 81 programas; TI residual** *(parcial)*

#### 8.1 Acesso técnico — **[V]**
`eureca.me` é WordPress institucional; o único link de vagas é `oportunidades.eureca.me` → redireciona para `app.eureca.me` [V], um SPA (Vite, `assets/index-C75Ph1H_.js`, 545 KB) [V].

Endpoint achado no bundle e testado [V]:
```
GET https://candidate-api.eureca.me/opportunities
→ 200, 211 KB, {"items":[…], "total":81, "page":1, "pageSize":200}
```
Sem login, sem token [V].
Os endpoints irmãos são fechados: `/jobs`, `/v1/jobs`, `/api/jobs`, `/vacancies` → **401 `Unauthorized: Missing or invalid Authorization header`** [V]. Só `/opportunities` é público.

#### 8.2 Autenticação — **[V] nenhuma para `/opportunities`.** SSO em `sso.eureca.me` para candidatura [V].

#### 8.3 ToS / robots — `eureca.me/robots.txt`: só bloqueia `/wp-admin/` [V]. **Não verifiquei robots de `candidate-api.eureca.me` nem de `app.eureca.me`** [não medido]. Não li ToS [P].

#### 8.4 Cobertura — **[V] 81 oportunidades, majoritariamente programas**
Mesmo perfil da Cia de Talentos: programas corporativos de estágio/trainee/aprendiz (Unilever, L'Oréal, Nestlé, PagBank).
Pelos títulos, os de TI são: *"Tecnologia e Dados"*, *"Trainee em Tecnologia e Digital"*, *"Trainee em Tecnologia da Informação"*, *"Estágio em Dados e Analytics"*, *"Estágio em Tecnologia"* — **5 de 81** [V].
**Não contei quantas são remotas nem quantas aceitam DF** — o campo `locations` do primeiro item veio `{"states":[],"cities":[]}` e `cityName`/`stateAcronym` vieram `null` [V], então a filtragem geográfica precisa de checagem item a item que **não fiz** [não medido].

#### 8.5 Campos — **[V]**
`id` (UUID), `source`, `name`, `description` (HTML), `companyId`/`companyName`/`companyLogoUrl`, `programId`/`programName`, **`workModel`** (`presencial`), `workModels[]`, `acceptsRelocation`, `locations{states,cities}`, `cityId`/`cityName`/`stateAcronym`, `salary{display,minCents,maxCents}`, `diversity[]`, `weeklyHours`, **`contractTypeKey`** (`trainee`), `publishedAt` (veio **null** no item inspecionado), **`createdAt`** (`2026-07-23 …`), **`endApplying`**.
Tem **modalidade e tipo de contrato estruturados** e **createdAt** [V]. Identidade: UUID [V].

#### 8.6 Veredito parcial
API limpa e gratuita, **81 itens, ~5 de TI**. Volume irrelevante sozinho, custo de implementação baixíssimo (uma requisição, JSON, sem paginação). Mesmo bucket da Cia de Talentos: "fonte de programas", fase 2. **Falta medir:** quantos dos 81 são remotos/DF.

---

### 9. Plooral — **[V] não é um portal de vagas; é ATS white-label**

- `plooral.com` → 200; `robots.txt` = `User-agent: * / Allow: /` + sitemap [V].
- O sitemap é institucional (`/pt-BR`, `/pt-BR/solutions`, …), **nenhuma vaga** [V].
- O único link de vagas da home é `https://enliztvagas.enlizt.me/` — que é **a página de carreiras da própria Plooral** (título: *"Plooral - Vagas Abertas | Powered by Plooral"*) [V].
- Padrão `enlizt.me`: cada empresa-cliente tem seu subdomínio (`<cliente>.enlizt.me`), com URLs tipo `/vagas/desenvolvedor_backend-290726` [V]. **Não existe mural central agregando clientes** [V].

**Veredito: mesma categoria do Abler na parte 1** — ATS sem portal público agregado. Só serviria via lista curada de empresas, como Greenhouse/Lever. **Fora.** Não procurei a API do enlizt [não medido].

---

### 10. Empregare — **[V] só robots.txt lido; nada mais medido** *(parcial)*

Único dado verificado: o `robots.txt` [V], que é **o mais interessante do inventário inteiro**:
```
User-agent: *
Content-Signal: search=yes, ai-input=yes, ai-train=no
Allow: /
Allow: /api/mcp          ← servidor MCP anunciado no robots
Allow: /api/docs         ← documentação de API anunciada
Disallow: /api/
Disallow: /whatsapp/
Disallow: /pt-br/Login/GetUsuarioLogado
Disallow: /pt-br/Vagas/VerificarAlertaVagas
Disallow: /pt-br/Vagas/SalvarVisualizacao
… (variantes en-us / es-cl)
Sitemap: https://www.empregare.com/pt-br/sitemap-index.xml
```

Leitura: o site **bloqueia `/api/` em geral, mas libera explicitamente `/api/mcp` e `/api/docs`** — ou seja, parece **oferecer uma API/MCP pública e documentada de propósito**. E o `Content-Signal` diz `ai-input=yes` (pode ser lido por agente) com `ai-train=no` (não pode treinar). Para um bot pessoal de leitura isso é praticamente um convite formal.

**Não medi nada além disso**: não abri `/api/docs`, não testei `/api/mcp`, não contei vagas, não verifiquei login, não olhei o sitemap. Ver "Não investigado".

---

### 11. Remotar — **[V] 404 no robots; nada mais medido** *(parcial)*

- `remotar.com.br` → 200, é **Next.js** (`buildId: brz-vIeaMBoOqWEwnJSPw`, `__NEXT_DATA__` presente) [V].
- `remotar.com.br/robots.txt` → **devolve a página 404 do Next.js**, não um robots [V]. Não há regra publicada.
- A parte 1 registrou `/vagas` → 404 [V, parte 1]. **Não achei o path correto da listagem nesta sessão** [não medido].

Ver "Não investigado".

---

## Parte C — Fontes citadas no ticket e não investigadas

Ver seção "Não investigado" abaixo. Nada foi medido para EstágioTrainee, InfoJobs (lacuna da parte 1), Glassdoor, Senado Federal e BairesDev.

---

## Comparativo consolidado (só o que foi medido)

| Fonte | Acesso | Login p/ listar | robots | Total ativas | **TI Brasil** | **TI em Brasília** | **TI remoto BR** | Data de publicação | Senioridade estruturada |
|---|---|---|---|---|---|---|---|---|---|
| **Sólides** | **JSON `apigw` [V]** | **não** | `Allow: /` + comentário pró-vaga [V] | **73.355** | 3.690 (área) | **118** | **505** | **`createdAt` ISO [V]** | **SIM [V]** |
| **Super Estágios** | JSON via POST PHP [V] | não | sem bloco `*` [V] | 3.698 | **148** | **9** | 3 "home office" com cidade fixa [V] | **não [V]** | só estágio |
| **CIEE** | **JSON Spring [V]** | não | `Disallow:` (libera) [V] | 5.907 | **67** | **0** | **0 (sem campo)** | **não [V]** | só estágio/aprendiz |
| **Nube** | JSON + sitemap [V] | **gate só client-side [V]** | libera `/detalhes-vaga/` [V] | 3.629 (portal diz 6.443) | **40** | **2** | 13 home office no total [V] | **não [V]** | só estágio/aprendiz |
| **Agiel** | AJAX OctoberCMS [V] | listar não / **detalhe SIM [V]** | **não existe robots.txt [V]** | não medido | **26** | **7** | 0 (sem campo) | **não** (ano no código) [V] | só estágio |
| **Cia de Talentos** | REST POST [V] | não | `Disallow:` (libera) [V] | **28 programas** | ~1 pelo título | não filtrável [V] | não filtrável [V] | só `endApplying` [V] | `hiringType` [V] |
| **Eureca** | REST GET [V] | não | libera [V] | **81 programas** | ~5 pelo título | não medido | não medido | **`createdAt` [V]** | `contractTypeKey` [V] |
| **Cia de Estágios** | sitemap c/ `lastmod` [V] | não determinado | libera [V] | **104 programas** | não medido | não medido | não medido | **`lastmod` [V]** | não medido |
| **Plooral** | — | — | `Allow: /` [V] | **não tem portal central [V]** | — | — | — | — | — |
| **Empregare** | não testado | não medido | **`Allow: /api/mcp`, `/api/docs` [V]** | não medido | não medido | não medido | não medido | não medido | não medido |
| **Remotar** | Next.js, path não achado [V] | não medido | **robots = 404 [V]** | não medido | não medido | não medido | não medido | não medido | não medido |

*(Gupy, para referência da parte 1: 82.023 total, 49 estágio remoto, 47 estágio DF, 46 júnior remoto, **11 júnior DF sendo 0 de TI**, sem senioridade estruturada, `publishedDate` com timestamp.)*

---

## Recomendação de ordem de adição

> A decisão é do ticket [Fechar fontes e stack](../issues/04-fechar-fontes-e-stack.md). O que segue é recomendação com justificativa.

A parte 1 recomendou **Gupy → Programathor → Vagas.com**. Minha resposta à pergunta final do ticket ("alguma deveria *substituir* uma das três?"):

### Sim, uma substituição: **Sólides entra no lugar do Programathor como 2ª fonte**

O argumento do Programathor na parte 1 foi **"é a única fonte com senioridade e tipo de contrato como campo estruturado"**. Esse argumento **caiu**: o Sólides tem os dois (`seniorities`, `recruitmentContractType`), e ainda tem `createdAt`, `salary`, `jobType` e cidade/estado estruturados **inclusive em vaga remota** [V].

Comparação direta no ponto que decidiu a parte 1:

| | Programathor | Sólides |
|---|---|---|
| senioridade estruturada | sim (HTML) | **sim (JSON)** |
| data de publicação | só no detalhe, 1 req/vaga [V, parte 1] | **no objeto da listagem [V]** |
| vagas encerradas na listagem | **sim, contamina** [V, parte 1] | `currentState` no objeto [V] |
| combinar dois filtros | **HTTP 302, quebra** [V, parte 1] | funciona [V] |
| cobertura Brasília | fraca [P, parte 1] | **1.661 vagas, 409 júnior [V]** |
| paginação | teto de 40 páginas, opaca [V, parte 1] | `totalPages` explícito [V] |

O Programathor mantém uma vantagem: **é 100% TI**, então o filtro "é TI?" desaparece. Mas o `occupationAreas=tecnologia` do Sólides entrega quase o mesmo benefício, com muito mais volume atrás.

**Contra-argumento pedagógico, que é real e pode inverter a decisão:** o mapa quer que o Luiz digite **um scraper de HTML**, e o Programathor é o modo fácil desse exercício (HTML estático, sem JS, sem Cloudflare challenge). Se o Sólides tomar o lugar dele, as três primeiras fontes viram **três APIs JSON** e a técnica "parsear HTML" nunca é digitada. Duas saídas: (a) manter o Programathor em 4º só pelo valor de aprendizado, ou (b) deixar o Vagas.com (HTML) cumprir esse papel — ele já cumpre, e é o 3º. **Recomendo (b)**: o Vagas.com já é o scraper de HTML da lista.

### Ordem recomendada

1. 🥇 **Gupy** — inalterado. Melhor vazão medida (~3–4 TI/dia), JSON puro, pedagogicamente certo como primeiro coletor.
2. 🥈 **Sólides** — `apigw.solides.com.br/jobs/v3/portal-vacancies-new`. Entra **no lugar do Programathor**. Motivo: é a única fonte que resolve o buraco de **júnior de TI em Brasília** (Gupy: zero; Sólides: 15 ativas, 409 júnior no DF no total) e a única com senioridade + data + salário estruturados. Segundo coletor JSON = repetição da técnica, portanto **mão do agente** pela regra do mapa.
3. 🥉 **Vagas.com** — inalterado, e agora com peso duplo: cobre Brasília **e** é o único scraper de HTML das três, ou seja, é onde a técnica de parsing é digitada pela primeira vez.
4. **Super Estágios** — 4ª, e a melhor candidata das agências. Uma requisição POST por dia devolve as 3.698 vagas com modalidade e bolsa estruturadas. Traz **9 vagas de TI em Brasília** que não estão em nenhuma das três acima. Custo de implementação: ~15 linhas.
5. **Agiel** — 5ª, condicional. Traz **7 vagas de TI em Brasília** com 27% de densidade DF/TI — a melhor do inventário. Custo maior (34 requisições/dia, uma por curso) e **o detalhe exige login**, então o alerta sai pobre (sem bolsa, sem descrição). Vale se, depois de 2–3 semanas de coleta, o eixo Brasília ainda estiver seco.

### O que fica de fora, e por quê

| Fonte | Motivo |
|---|---|
| **CIEE** | Melhor API de estágio que existe no Brasil e **inútil aqui**: 67 vagas de TI no país, **zero em Brasília**, **zero remotas por construção do modelo de dados** [V]. Não é questão de acesso — é questão de não ter a vaga. |
| **Nube** | 13 vagas home office no Brasil inteiro e 2 de TI no DF (uma delas de R$ 750) [V]. Acesso fácil, conteúdo ausente. |
| **Cia de Talentos** | 28 programas; `opportunityAreas` é "Diversas" em 26 deles, `opportunityLocations` vazio [V] — **não dá para filtrar TI nem localidade por campo**. |
| **Eureca** | 81 programas, ~5 de TI pelo título [V]. Mesmo bucket. |
| **Cia de Estágios** | 104 programas via sitemap com `lastmod`; conteúdo mora em hotsites externos [V]. TI não medido. |
| **Plooral** | Não é portal: é ATS white-label em `*.enlizt.me`, sem mural central [V]. Mesma situação do Abler na parte 1. |

**Nota de produto sobre os três "catálogos de programa" (Cia de Talentos, Eureca, Cia de Estágios):** juntos são ~213 itens de baixíssima rotatividade, com programas de nome grande (Itaú, Globo, PwC, Unilever, PepsiCo, Bayer). Nenhum é filtrável por TI. Se o Luiz quiser cobertura de *programa de estágio de empresa grande*, a forma barata não é filtrar — é **mandar todo item novo**, porque são poucos. Isso é decisão de produto, não de coleta, e cabe na fase 2.

---

## Implicações para outros tickets

- **Identidade de vaga / deduplicação.** Achei um caso concreto e feio: **7 das 9 vagas de TI da Super Estágios em Brasília são do TRE-DF**, com ids distintos e um curso diferente cada [V]. Um bot ingênuo manda 7 notificações do que é um edital só. A chave de dedup precisa considerar `(empresa + cidade + janela temporal)`, não só `(fonte + id)`.
- **Semântica de "sumiu".** **Quatro fontes medidas não têm data de publicação nenhuma**: CIEE, Nube, Super Estágios, Agiel [V]. Nelas, "é nova?" só pode ser respondido por diff contra a coleta anterior, e a primeira coleta é toda "nova". Já Sólides (`createdAt`), Eureca (`createdAt`) e Cia de Estágios (`lastmod`) têm data. Isso divide as fontes em **dois regimes de detecção de novidade**, e o schema precisa suportar os dois.
- **Detecção de coleta quebrada.** Três canários gratuitos encontrados: Sólides tem `count` no envelope [V], Super Estágios tem contador implícito no tamanho do array [V], e Agiel imprime `"Sua busca gerou N vagas"` no HTML [V]. Todos alimentam o item "Resiliência a quebra de fonte" do mapa.
- **Armadilha específica do Sólides:** parâmetro com nome errado **não gera erro** — devolve o total sem filtro [V]. É uma quebra silenciosa por construção. O coletor precisa validar `count` contra uma faixa esperada.

---

## Não investigado

Esta apuração foi interrompida por limite de contexto. O que segue **não foi medido**. Nada aqui é chute.

### Fontes do ticket totalmente intocadas

| # | Fonte | O que falta — tudo |
|---|---|---|
| **12** | **EstágioTrainee** (`www.estagiotrainee.com`) | Só sei que a home responde **200 com 770 KB** e que o `robots.txt` é **`Allow: /`**, com bloqueio só de `*?lightbox=`, `PetalBot`, e crawl-delay para dotbot/AhrefsBot; sitemap em `/sitemap.xml`. É um **site Wix** (o robots é auto-gerado pelo editor de SEO da Wix) [V]. **Falta tudo:** path da listagem, se exige login, se há API/JSON (sites Wix costumam ter `_api/wix-ecommerce`/`_functions`), contagem total, contagem de TI, contagem de DF/remoto, campos, identidade de vaga, data de publicação. |
| **13** | **InfoJobs** — *fechar a lacuna da parte 1* | A parte 1 verificou acesso (200, HTML estático, 20 vagas por página, id no slug `__<id>.aspx`) e robots (busca liberada), mas **não conseguiu medir volume**. Reconfirmei nesta sessão apenas que a home responde **200 / 182 KB** e reli o robots (bloqueia só páginas institucionais e `/Candidato-*`) [V]. **A lacuna continua exatamente onde estava:** contar vagas de TI, de estágio, de júnior, em DF e remoto. **Como medir** (herdado da parte 1): rodar `empregos.aspx?palabra=…` com `&provincia=` para DF e contar `__<id>` distintos por 3 dias seguidos; e investigar se há parâmetro de paginação e de "publicadas nas últimas 24h". |
| **14** | **Glassdoor** | Só sei que `www.glassdoor.com.br` responde **HTTP 403** com 240 KB de corpo para um User-Agent de Chrome [V] — ou seja, **anti-bot ativo já na home**, mesmo perfil do Indeed na parte 1. O `robots.txt` começa com `# Brazil (pt_BR)` / `#### Rules for ANY User-Agent` mas **eu não li o arquivo inteiro** [V, leitura parcial]. **Falta:** ler o robots completo, verificar se há endpoint de vagas acessível, avaliar se o 403 é contornável sem headless (provavelmente não, e nesse caso é descarte por R$ 0/mês, igual ao Indeed). |
| **15** | **Programa de estágio do Senado Federal** | **Zero requisições feitas.** Falta: achar a página oficial do programa, verificar se as vagas de TI aparecem em edital PDF ou em página HTML, se há periodicidade previsível (concurso/processo seletivo anual vs. fluxo contínuo), e responder a pergunta do ticket — **vale um coletor dedicado a um empregador?** Minha suspeita [P, não medido] é que o Senado publica por **edital periódico**, o que se detecta melhor monitorando uma página de editais do que raspando vagas. |
| **16** | **BairesDev** | **Zero requisições feitas.** Falta: verificar se o careers page tem JSON-LD `JobPosting` ou API, se as vagas "júnior" existem de fato (a reputação da empresa é de contratar pleno/sênior remoto para clientes dos EUA [P, não medido]), e a mesma pergunta do ticket sobre coletor de empregador único. |

### Fontes com achado parcial (registradas acima, mas incompletas)

| Fonte | O que **está** medido | O que **falta** |
|---|---|---|
| **Empregare** | Só o `robots.txt` [V] — que anuncia **`Allow: /api/mcp` e `/api/docs`** com `Content-Signal: ai-input=yes, ai-train=no`. Forte indício de API pública documentada. | **Tudo o mais.** Abrir `https://www.empregare.com/api/docs`, testar `/api/mcp`, ler o `sitemap-index.xml`, contar vagas totais / TI / estágio / júnior / DF / remoto, verificar login, mapear campos e identidade. **Esta é a lacuna de maior valor esperado da lista** — é a única fonte do inventário inteiro que parece oferecer API pública *de propósito*. |
| **Remotar** | Home 200, é Next.js com `buildId: brz-vIeaMBoOqWEwnJSPw`; `robots.txt` **retorna 404** (não existe) [V]. Parte 1 já registrou `/vagas` → 404. | Achar o path real da listagem (tentar `/`, `/jobs`, `/oportunidades`, ou ler o `_buildManifest.js` para enumerar as rotas do Next). Depois: volume, TI, filtro remoto (é o foco declarado do site), login, campos, data. |
| **Companhia de Estágios** (`ciadeestagios.com.br`) | Domínio correto identificado (o do ticket não resolve); robots libera; **104 programas no sitemap com `<lastmod>`**; páginas de programa são redirects sem JSON-LD [V]. | A API do portal `carreira.ciadeestagios.com.br` (Next.js/Turbopack) — ler os chunks em `/_next/static/chunks/*.js`. Depois: exige login?, quantos programas abertos, quantos de TI, DF/remoto. |
| **Eureca** | API pública `/opportunities` (81 itens, 200 sem token), campos completos incluindo `createdAt`, `workModel`, `contractTypeKey`; ~5 de TI pelo título [V]. | Quantos dos 81 são **remotos** e quantos aceitam **DF** — o `locations` do item que inspecionei veio vazio e `cityName`/`stateAcronym` vieram `null`, então precisa varrer os 81. Também: robots de `candidate-api.eureca.me`. |
| **Cia de Talentos** | API pública POST, 28 programas, campos completos [V]. | robots.txt do subdomínio `vagas.ciadetalentos.com.br` (li só o do site institucional). Se vale filtrar TI parseando o HTML do `opportunityDescription`. |
| **Agiel** | 34 cursos de TI varridos, 26 vagas únicas, 7 no DF, login no detalhe confirmado [V]. | **Paginação do partial AJAX** — para cursos com mais de ~20 resultados (ex.: Administração, 131) o HTML só renderizou parte. Não afetou TI (todos ≤18) mas afeta qualquer medida de total. Também: o handler `onCursoChange` devolveu **HTTP 500** e não investiguei por quê. |
| **Nube** | API pública, 3.629 vagas, filtros mapeados, gate de login é client-side [V]. | **Discrepância não explicada:** o portal anuncia **6.443 vagas abertas** e a API anônima devolve **3.629**. Falta descobrir se as ~2.800 restantes são agrupamentos, vagas exclusivas de perfil logado, ou cache. Se forem visíveis só logado, a cobertura de TI medida está subestimada. |
| **Sólides** | API mapeada e medida a fundo [V]. | Quanto `occupationAreas=tecnologia` **perde** (vaga de TI classificada em outra área) — é o análogo do buraco "júnior sem a palavra júnior" da parte 1. Medir amostrando N vagas de `contractsType=estagio` sem filtro de área e classificando à mão. Também: teste de rate limit (fiz 14 requisições em 37s sem problema, mas não estressei). |
| **CIEE** | Medida a fundo [V]. | Nada material. A fonte foi descartada por conteúdo, não por acesso. |
| **Super Estágios** | Medida a fundo [V]. | Teste de rate limit (fiz poucas requisições; o payload é de 5,9 MB, então vale confirmar que não há throttling). Ler os ToS textuais. |

### Perguntas que este ticket abriu e não fechou

1. **A API do Empregare é real e aberta?** `Allow: /api/docs` num robots.txt é raro o bastante para merecer 20 minutos. Se for, muda a lista.
2. **Sobreposição Sólides × Gupy.** Não medi nenhum overlap. Os dois são ATS grandes com portal agregador; se uma empresa publica nos dois, a dedup cross-source vira problema central. Isso conecta ao item "Sobreposição entre fontes" do mapa, que continua aberto desde a parte 1.
3. **A `v3` do Sólides vai morrer?** Existe uma `applicants-v2/jobs/v4` que responde 403 [V]. Se for a sucessora e for fechada, a fonte some. Não dá para saber sem observar ao longo do tempo.
4. **Vazão real de tudo.** Todos os números aqui são snapshot de 2026-08-14. Só Sólides e Eureca têm `createdAt` para estimar fluxo; as demais exigem dois dias de coleta. Reforça a recomendação da parte 1: instrumentar contagem de ids novos por fonte desde o dia 1.
