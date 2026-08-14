# Mapa: Bot de vagas de estágio/júnior em TI

Label: `wayfinder:map`

## Destination

Um bot rodando todo dia que entrega, no Telegram, as vagas **novas** de estágio e júnior em TI (remoto Brasil + Brasília/DF, qualquer área de TI) e sinaliza as que **sumiram** — construído sob a regra "primeira vez é sua".

O mapa termina quando o bot está de pé, notificando diariamente sem intervenção, e existe um inventário explícito de quais técnicas Luiz digitou pela primeira vez.

## Notes

**Este mapa carrega execução** — override explícito do padrão "plan, don't do" do wayfinder. Motivo: o perfil do dev é teoria intermediária/avançada com zero prática de mão própria. Um mapa que só decide entregaria a única coisa que ele já tem. O aprendizado *é* a digitação.

**O projeto é de duas pessoas.** Luiz e um segundo dev (mesma faculdade, mesma cidade, mesmo perfil: teoria boa, mão zero), que aceitou as condições em 2026-08-14 — ver [Trazer um segundo dev para o projeto](./issues/11-segundo-dev-no-projeto.md).

**Regra de divisão do trabalho — "primeira vez é sua", versão para dois:**
- **Primeira ocorrência absoluta de uma técnica** (nenhum dos dois digitou): **pareado**, driver e navigator revezando o teclado **a cada 25 min no cronômetro**. Os dois digitam. **Luiz é o primeiro driver** — regra explícita para contrariar a hierarquia líder/braço-direito herdada da faculdade.
- **Técnica que só um dos dois já digitou:** pareado de novo, mas **quem ainda não digitou é o primeiro driver**. É a primeira vez *dele*.
- **Técnica que os dois já digitaram:** repetição, não aprendizado → do agente, ou em paralelo via GitHub se preferirem.
- **Setup, config, boilerplate, YAML de CI:** do agente desde sempre. Convenção não-dedutível não ensina.
- "Nunca digitou" ≠ "nunca entendeu". Código que existe nos projetos deles mas foi escrito por agente **conta como não-digitado**.

**Parear = uma pessoa digitando por vez, no mesmo problema, ao mesmo tempo.** Podem estar em casas diferentes (call + tela compartilhada); não podem estar em arquivos diferentes. Git continua em uso normalmente — o que some é o conflito de merge. Detalhe operacional completo no ticket do segundo dev.

**Só as primeiras vezes precisam ser síncronas** — estimativa de ~2 blocos de 2h por semana, com o resto em paralelo.

**Por que não é o inverso ("agente faz a primeira, Luiz faz a segunda"):** quase toda técnica deste projeto ocorre **exatamente uma vez** (schema, CI, cron, dedup, notificador). Só o coletor se repete. A regra invertida colapsaria em "o agente faz tudo e o Luiz escreve o segundo scraper".

**Escada de saída — "eu digito" nunca significa "eu sozinho, do zero":**

1. A dupla tenta. **Timebox de 30 minutos** por peça — 30 min com os *dois* travados no mesmo problema, não 30 min cada.
2. Travou → pede dica. O agente sobe **um degrau por vez**, e só o necessário:
   1. direção conceitual ("você precisa de duas coisas aqui: pegar o HTML e achar os nós");
   2. o link exato da doc, com a seção;
   3. a assinatura do que precisa ser chamado, sem o corpo;
   4. esqueleto com buracos e `TODO`s — Luiz preenche;
   5. o agente escreve — **e então Luiz apaga e reescreve sem olhar**.
3. **Convenção pura** (YAML de CI, scaffolding, arquivos de config, `.gitignore`): do agente desde o início. Não há raciocínio dedutível ali, só formato memorizado. Luiz lê e modifica.
4. Segunda ocorrência da mesma técnica: do agente.

O degrau 5 é rede de segurança: nada trava o projeto para sempre. Ele custa caro (reescrever) de propósito, para não ser usado por preguiça.

**Racional:** o perfil é "conceito forte, prática zero". Para quem já tem o conceito, tentar-e-falhar antes de ver a solução retém mais do que ver a solução primeiro. E "não sei fazer" aqui quase sempre significa "não sei a sintaxe exata" — problema de consulta à documentação, que é justamente a habilidade a treinar.

**Restrições fixadas:**
- Orçamento: **R$ 0/mês** — só free tier.
- Canal de entrega: **Telegram**.
- Escopo de vaga: estágio **e** júnior, qualquer área de TI (dev, dados, infra, QA, suporte), remoto no Brasil + presencial/híbrido em Brasília/DF.

**Coleta larga, entrega filtrada.** Princípio fixado em 2026-08-14. Coletar é quase de graça (a requisição custa o mesmo trazendo 4 ou 400 vagas; guardar custa kilobytes) e **coletar estreito é a única decisão irreversível do projeto** — dado não coletado não pode ser analisado depois. Notificar largo, ao contrário, mata o bot: 200 itens/dia no Telegram e eles param de ler em quatro dias, com o bot tecnicamente funcionando e praticamente morto.

Portanto: **a coleta puxa todas as vagas de TI sem recorte de área ou senioridade; o filtro mora na entrega e é por pessoa.** Consequências: o alvo de ML vira mudança de config e não recoleta; cada dev tem o filtro dele; o problema do "júnior invisível" (senioridade só no título) vira ajustável com reprocessamento do que já está no banco. Não por acaso, é o padrão camada-crua/camada-refinada de pipeline de dados — a competência que serve o alvo de MLOps.

**Inventário ≠ escopo da v1.** O inventário de fontes deve ser o mais completo possível — ele é o roteiro de crescimento. O escopo da v1 é **uma fonte só**: 19 fontes na primeira versão são 19 formatos de HTML, 19 modos de quebrar e 19 depurações antes do primeiro ciclo fechar. A lista completa alimenta a ordem de adição, não o mês um.

**Skills a consultar por sessão:** `/grilling`, `/domain-modeling`, `/research`, `/prototype`, `/tdd`.

## Decisions so far

- [Trazer um segundo dev para o projeto](./issues/11-segundo-dev-no-projeto.md) — **Sim, entrou.** Amigo de mesmo perfil (teoria boa, mão zero) aceitou as três condições: parear com revezamento de 25 min, Luiz digita primeiro em técnica nova, e o bot serve os dois desde a v1. Regra de divisão reescrita para dois nas Notes. **Dois destinatários viram requisito de v1**, não névoa — filtro e destino por pessoa entram no schema. Risco vivo: a retenção do segundo dev depende inteiramente do bot entregar vaga útil *para ele*.
- [Objetivo de carreira e o que o bot é, afinal](./issues/09-objetivo-de-carreira.md) — Alvo: **ML → MLOps / ML engineering / AI engineering**; bot misto ("rápido, mas aprendendo"); pressão sem prazo duro. **A tensão instrumento-vs-portfólio se dissolveu:** Python é simultaneamente o caminho mais rápido e a linguagem do alvo. Duas consequências: (a) o filtro deve capturar vaga de **dados e backend Python**, não só "ML" no título, porque MLOps quase não contrata estágio direto; (b) este bot **é um pipeline de dados** — schema, agendamento, idempotência e detecção de coleta quebrada deixam de ser andaime e viram o miolo do portfólio.
- [Inventário de fontes de vagas](./issues/01-inventario-de-fontes.md) — **Gupy tem API JSON pública sem login** (`employability-portal.gupy.io/api/v1/jobs`, verificada, sem rate limit; ~3–4 vagas/dia no recorte). Ordem: Gupy → Programathor (HTML estático, única com senioridade estruturada) → Vagas.com (cobre Brasília, onde a Gupy tem **zero** júnior de TI). LinkedIn e Indeed descartados (robots/403); RemoteOK e WWR descartados com medição. **Achado que muda o design:** estágio é campo de banco, júnior é palavra no título — dois pipelines com filtros distintos, não um `OR`.

- [Linguagem mais empregável para estágio/júnior de TI](./issues/02-linguagem-mais-empregavel.md) — Java+C# dominam o emprego dev no BR (~31%, Código Fonte 2026), contrariando o Stack Overflow global; em Brasília a concentração é de **empregador** (fábricas govtech pedindo Java/Spring ou .NET), não estatística. Mas Python lidera o volume bruto de vagas no DF via dados/BI/automação. **Recomendação: Python + SQL**, com Java/Spring obrigatório como segundo projeto se o alvo incluir vaga de dev no DF. Decisão final fica em *Fechar fontes e stack*.

## Not yet specified

- **Implementação propriamente dita.** Os tickets de execução (coletor, deduplicador, notificador, agendamento) só podem ser recortados depois que fonte, stack e infra estiverem fechadas. Cada um vai nascer marcado "mão sua" ou "mão minha" pela regra da primeira vez.
- **Resiliência a quebra de fonte.** Sites mudam HTML e derrubam scraper em silêncio. Como detectar "coletei 0 vagas hoje porque quebrou" vs. "coletei 0 porque não teve vaga nova" — questão real, mas só ganha forma depois que as fontes existirem.
- ~~**Anti-bot.**~~ Névoa dissipada pelo [Inventário de fontes](./issues/01-inventario-de-fontes.md): as três fontes escolhidas são amigáveis (Gupy sem rate limit observado, Programathor com `robots.txt` convidativo). Resta só a higiene básica — user-agent honesto e intervalo entre requisições — que é detalhe de implementação, não decisão.
- **Sobreposição entre fontes.** A pesquisa não conseguiu medir quantas vagas aparecem em duas fontes ao mesmo tempo. Se a sobreposição for alta, a deduplicação cross-source vira o problema central em vez de detalhe. Só dá pra medir com dados próprios, depois da segunda fonte existir.
- **Semântica de "sumiu".** Vaga fora do resultado pode ser preenchida, despublicada, ou só um erro transitório da coleta. Quantos dias de ausência até anunciar sumiço — depende de conhecer a instabilidade real das fontes.
- **Histórico e métricas.** Quantas vagas por semana, quais empresas mais publicam, tempo médio de vida de uma vaga. Interessa, mas depende do banco existir e ter dados.

## Out of scope

- **Candidatura automática.** O bot avisa, não se candidata. Auto-apply queima reputação, viola ToS de praticamente toda plataforma e remove o julgamento humano de onde ele mais importa.
- **Otimização de currículo / ATS.** Problema adjacente e legítimo, mas é outro produto — não está no caminho até o destino.
- **Ranking ou match por IA.** "Quais dessas vagas combinam mais comigo" é atraente e é a forma mais rápida de nunca terminar o coletor. Fica para depois do bot estar rodando; se voltar, volta como esforço novo.
- **Interface web / dashboard.** O canal é o Telegram. Uma UI é escopo novo, não um passo da rota.
- ~~**O segundo projeto em Java/Spring.**~~ **Cancelado** por [Objetivo de carreira](./issues/09-objetivo-de-carreira.md). A mitigação pressupunha alvo de dev backend em fábrica govtech; o alvo real é ML/MLOps, onde Python é a resposta certa sem ressalva.
- **LinkedIn como fonte.** Tecnicamente acessível sem login, mas `robots.txt` proíbe explicitamente. Ruled out no [Inventário de fontes](./issues/01-inventario-de-fontes.md) — não é névoa, é decisão tomada.
- **Re-medir o mercado com dados próprios.** A pesquisa de linguagem falhou em contar vagas por portal (403, cache, sem total exposto) — e este bot é justamente o instrumento que corrige isso. Vale reabrir a pergunta após ~4 semanas de coleta, mas isso é depois do destino, não antes.
