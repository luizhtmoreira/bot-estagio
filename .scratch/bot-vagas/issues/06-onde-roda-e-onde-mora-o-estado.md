# Onde o bot roda e onde o estado mora

Type: grilling
Status: open
Blocked by: 04
Parent: [Mapa: Bot de vagas de estágio/júnior em TI](../map.md)

## Question

O bot precisa acordar todo dia sem o notebook do Luiz estar ligado, e precisa lembrar o que já mostrou ontem. Duas decisões acopladas, ambas sob a restrição de **R$ 0/mês**.

1. **Execução agendada.** GitHub Actions com `schedule` (grátis em repo público, ensina YAML/CI/secrets) vs. cron em VPS free tier vs. Vercel Cron vs. outra. Considerar: o `schedule` do GitHub Actions atrasa e às vezes pula execuções em horário de pico — isso é aceitável para um bot diário?
2. **Persistência.** Onde mora o histórico de vagas já vistas:
   - SQLite commitado no próprio repositório pelo workflow (grátis, versionado, e o diff do commit *é* o log de mudanças — mas é uma gambiarra que só funciona em baixo volume);
   - Postgres em free tier gerenciado (Neon, Supabase);
   - um JSON num Gist ou artifact.
   Cada opção ensina uma coisa diferente. Sob a regra "primeira vez é sua", qual dessas técnicas o Luiz nunca digitou?
3. **Segredos.** Onde ficam o token do Telegram e credenciais de fonte, e como o job os lê sem vazar em log.
4. ~~**Repo público ou privado?**~~ **Corrigido em 2026-08-14 — o trade-off que eu descrevi aqui era falso.** Actions é ilimitado em repo público, mas o plano gratuito dá **2.000 minutos/mês para repo privado**, e um job diário de ~2 min gasta ~60 min/mês. Não há concessão a fazer: **privado, de graça**. A pergunta que sobra é só de portfólio (repo público mostra o trabalho a recrutador) e pode ser adiada — dá pra tornar público depois, desde que o histórico de commits não contenha segredo. Isso reforça o item 3.

**Depende de 04** porque a linguagem escolhida muda o custo de cada runtime.
