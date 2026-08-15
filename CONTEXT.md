# CONTEXT

Vocabulário fixado do bot de vagas de estágio/júnior em TI. Ver [mapa](https://github.com/luizhtmoreira/bot-estagio/issues/1) e [modelo de domínio](https://github.com/luizhtmoreira/bot-estagio/issues/6).

## Termos

- **vaga** — um registro identificado por `(fonte, id_da_fonte)`. Duas linhas com o mesmo `(fonte, id)` são a mesma vaga; a mesma vaga postada em duas fontes diferentes conta como duas vagas (dedup cross-source não existe na v1 — ver Decisões).
- **fonte** — origem de coleta. V1: Gupy. Ordem de adição depois: Sólides → CIEE → Programathor → Vagas.com, cada uma após 2 dias corridos estáveis da anterior.
- **coleta** — uma execução do processo que busca vagas ativas numa fonte.
- **snapshot** — o conjunto de vagas ativas capturado numa coleta.
- **novidade** — vaga cujo `(fonte, id)` nunca apareceu num snapshot anterior. Dispara notificação diária, exceto no dia 1 (ver baseline). Não usa data de publicação da fonte para decidir novidade — só diff contra o histórico. Motivo: metade das fontes do roteiro (CIEE, Nube, Super Estágios, Agiel) não tem campo de data nenhum.
- **baseline** — evento único da primeira execução: notifica tudo que existe no primeiro snapshot. Distinto de novidade, não se repete — evita tanto perder o estado atual quanto inundar o Telegram todo dia.
- **relevante** — vaga que passa no filtro de entrega: é TI **e** (estágio **ou** júnior **ou** trainee) **e não** jovem aprendiz. Usa campo estruturado da fonte quando existe (ex: `type=vacancy_type_internship` na Gupy); cai para regex sobre o título quando não existe. Regex deliberadamente generoso — falso negativo (esconder vaga boa) dói mais que falso positivo (mostrar lixo).
- **sumiço** — vaga presente num snapshot anterior e ausente do snapshot atual. Semântica de quando anunciar isso (quantos dias de ausência até avisar) ainda é questão aberta do mapa — este termo só fixa o nome, não o comportamento.

## Decisões deste ticket que valem registrar

- **Identidade de vaga é só `(fonte, id_da_fonte)`.** Sem hash de empresa+título+local, sem agrupamento de edital (caso concreto conhecido: 7 vagas do TRE-DF na Super Estágios com ids distintos, mesmo edital — tratadas como 7 vagas, não 1).
- **Sem dedup cross-source na v1.** Risco aceito conscientemente; só dá para medir de verdade com a segunda fonte rodando.
- **Um filtro só, compartilhado entre os dois destinatários.** Revoga a decisão anterior do mapa (ticket #12) de que "filtro e destino por pessoa entram no schema desde a v1". Motivo: com uma fonte e ~3-4 vagas/dia, curadoria por pessoa é fardo do bot sem benefício real — cada um filtra no próprio olho ao ler. Reabrir se o volume crescer o suficiente para incomodar.
