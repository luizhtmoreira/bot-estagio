# Execução agendada via GitHub Actions e persistência via Postgres gerenciado (Neon)

O bot precisa rodar todo dia sem depender do notebook do Luiz ligado, e persistir snapshots de vagas entre execuções, sob restrição de R$0/mês. Decisão: **GitHub Actions `schedule`** dispara o job diário (repo privado hoje, com plano de tornar público depois — minutos grátis cobrem qualquer um dos dois cenários no volume atual), e o estado persiste em **Postgres gerenciado via Neon**, não SQLite commitado no repo nem JSON em Gist.

Actions foi escolhido por não exigir infra nova a manter (sem VPS, sem plataforma extra) — a imprecisão do `schedule` (atraso ou skip ocasional em pico) é aceitável porque o diff diário de novidade/sumiço não depende de intervalo exato de 24h. Neon foi escolhido sobre SQLite-no-repo (que exigiria a CI commitar de volta em `main` todo dia — "gambiarra que só funciona em baixo volume", nas palavras do ticket) e sobre Supabase (superfície de produto maior que o problema pede, apesar da familiaridade de conta já existente) porque o alvo de carreira é ML/MLOps ([#10](https://github.com/luizhtmoreira/bot-estagio/issues/10)) e esta é a primeira vez que Luiz e o parceiro escrevem SQL na mão contra um Postgres de verdade — sessão pareada, primeira ocorrência da técnica.

## Considered Options

- **SQLite commitado pelo workflow** — rejeitado: força a CI a escrever em `main` todo dia, e não escala.
- **Supabase** — rejeitado: bundla auth/storage/API REST que o bot não usa; Neon é só Postgres.
- **Vercel Cron / VPS free tier** — rejeitado: infra extra sem ganho sobre Actions, que já está disponível de graça no repo.

## Consequences

- Dois segredos reais em v1: `TELEGRAM_BOT_TOKEN` e `DATABASE_URL` (Neon), via GitHub encrypted Secrets injetados como env vars — nunca impressos em log, nunca interpolados em string de shell. Nenhuma fonte da v1 exige credencial própria (Gupy, Sólides, CIEE, Programathor são todas sem login, por [#5](https://github.com/luizhtmoreira/bot-estagio/issues/5)).
- `*.db` / `*.sqlite*` seguem no `.gitignore` (já estavam lá como boilerplate, não decisão) — nenhuma mudança necessária ali.
