# Mockups — formato da mensagem diária (issue #8)

Três variações concretas, dados inventados mas plausíveis. Objetivo: reagir a exemplos literais, não discutir no abstrato. Nenhuma ainda escolhida — ver decisão ao final quando fechada.

## Mockup A — densidade alta, uma linha por vaga, sem agrupamento

```
📋 Vagas de hoje (18/08) — 5 novas

• Estagiário de Dados — Neoway (remoto) — gupy.io/neoway/123
• Dev Jr Backend Python — Softplan (Brasília/DF) — gupy.io/softplan/456
• Estágio TI/Suporte — TRE-DF (Brasília/DF, presencial) — gupy.io/tredf/789
• Estagiário QA — Stone (remoto) — gupy.io/stone/321
• Analista Jr Infra — Dataprev (Brasília/DF, híbrido) — gupy.io/dataprev/654

⚠️ Sumiram desde ontem (2):
• Estágio Backend — iFood (remoto)
• Dev Jr Full Stack — Loft (remoto)
```

- Dia vazio: manda `📋 Vagas de hoje (18/08) — nenhuma vaga nova. Bot rodou ok.` (silêncio nunca, pra diferenciar de bot quebrado)
- Volume alto (40 vagas): lista tudo mesmo, sem truncar — testar se realmente vira ruído antes de otimizar

## Mockup B — cartão por vaga, agrupado por área (dev/dados/infra), sumiços numa seção própria

```
📋 Vagas de hoje (18/08)

🖥️ Dev (2)
┌ Dev Jr Backend Python
│ Softplan · Brasília/DF · presencial
└ gupy.io/softplan/456

┌ Estágio Backend Full Stack
│ Loft · remoto
└ gupy.io/loft/999

📊 Dados (1)
┌ Estagiário de Dados
│ Neoway · remoto
└ gupy.io/neoway/123

🔧 Infra/Suporte (2)
┌ Estágio TI/Suporte
│ TRE-DF · Brasília/DF · presencial
└ gupy.io/tredf/789

┌ Analista Jr Infra
│ Dataprev · Brasília/DF · híbrido
└ gupy.io/dataprev/654

—

⚠️ Sumiram (1)
┌ Estágio Backend — iFood (remoto)
└ presente desde 15/08, sumiu hoje
```

- Dia vazio: mesma lógica do Mockup A, mas sem seções vazias — só a linha de status
- Volume alto: trunca por seção em 5, com `+12 mais em Dev → link pro histórico`

## Mockup C — uma linha por vaga, agrupado por modalidade (remoto/presencial/híbrido), sem seção de sumiço

```
📍 Remoto (3)
Estagiário de Dados — Neoway — gupy.io/neoway/123
Dev Jr Backend Python — Stone — gupy.io/stone/321
Estágio Backend Full Stack — Loft — gupy.io/loft/999

📍 Brasília/DF (2)
Estágio TI/Suporte — TRE-DF (presencial) — gupy.io/tredf/789
Analista Jr Infra — Dataprev (híbrido) — gupy.io/dataprev/654
```

- Sumiço não aparece na mensagem — fica só no banco/histórico, consultável sob demanda
- Dia vazio: bot fica em silêncio (risco: ambíguo com bot quebrado — ponto contra este mockup)
- Volume alto: pagina por modalidade, sem link externo

## Decisão

**Escolhido: Mockup A.** Uma linha por vaga, sem agrupamento, sumiços numa seção separada no fim da mensagem. Dia vazio manda mensagem de status ("nenhuma vaga nova") em vez de ficar em silêncio — silêncio é ambíguo com bot quebrado. Volume alto lista tudo sem truncar por enquanto; revisitar se isso virar ruído na prática.

Este formato vira a especificação literal do notificador (issue #17).
