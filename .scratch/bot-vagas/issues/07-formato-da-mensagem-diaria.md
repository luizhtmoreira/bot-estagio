# Formato da mensagem diária

Type: prototype
Status: open
Blocked by: 03, 05
Parent: [Mapa: Bot de vagas de estágio/júnior em TI](../map.md)

## Question

Como é, exatamente, a mensagem que chega no Telegram todo dia?

Fazer 3 mockups concretos de mensagem (texto puro, com dados inventados mas plausíveis) e reagir a eles, em vez de discutir no abstrato. Variar deliberadamente:

- **Densidade**: uma linha por vaga vs. um cartão por vaga com empresa, local e modalidade.
- **Agrupamento**: por fonte? por área (dev/dados/infra)? por modalidade (remoto/presencial)? sem agrupar?
- **Sumiços**: aparecem na mesma mensagem, numa seção separada, ou não aparecem? Uma vaga que sumiu é informação acionável ou só ruído?
- **Dia vazio**: o bot manda "nenhuma vaga nova hoje" ou fica calado? Silêncio é ambíguo — não dá pra distinguir de bot quebrado.
- **Volume alto**: e se caírem 40 vagas num dia? A mensagem trunca, pagina, ou vira link?

Perguntas de fundo: quantas mensagens por dia é o limite antes de você começar a ignorar o bot? A mensagem deve caber numa notificação de celular ou é pra abrir e ler com calma?

**Entregável:** o formato escolhido, escrito como exemplo literal, linkado a partir deste ticket. Vira a especificação do notificador.

**Depende de 03** (o canal precisa existir pra testar de verdade) e **de 05** (não dá pra formatar um campo que ainda não foi definido).
