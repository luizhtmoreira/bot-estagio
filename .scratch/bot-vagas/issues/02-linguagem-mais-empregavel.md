# Linguagem mais empregável para estágio/júnior de TI

Type: research
Status: resolved
Blocked by: —
Parent: [Mapa: Bot de vagas de estágio/júnior em TI](../map.md)

## Question

Qual linguagem/stack o mercado de **estágio e júnior de TI** pede mais em **Brasília/DF** e em **remoto Brasil**?

O dev escolheu "a que me tornar mais empregável" em vez de escolher por conforto. Este ticket produz a evidência; a escolha acontece no ticket "Fechar fontes e stack".

Levantar:

1. **Demanda real por linguagem** em vagas de estágio/júnior de TI no Brasil — Python, JavaScript/TypeScript, Java, C#/.NET, Go, PHP. Usar dados de pesquisas recentes (Stack Overflow Survey BR, State of Software Engineering, pesquisas da comunidade BR) e, se possível, contagem direta de vagas em portais.
2. **Recorte Brasília/DF** especificamente — o DF tem perfil atípico (peso grande de setor público, órgãos federais, consultorias). Isso muda a resposta? Java/.NET costumam pesar mais em contexto de governo.
3. **Encaixe com o projeto**: qual delas tem ecossistema decente para (a) HTTP + parsing de HTML/JSON, (b) navegador headless se necessário, (c) rodar de graça em CI, (d) SQLite/Postgres. Nenhuma deve ser descartada por isso, mas o atrito importa.
4. **Sinal de portfólio**: para um recrutador de estágio, um bot em Python e o mesmo bot em TypeScript sinalizam a mesma coisa? Existe diferença de percepção?

**Entregável:** comparativo em Markdown com uma recomendação fundamentada e o custo de escolher a alternativa. Fontes primárias, com data — dado de mercado envelhece.

## Answer

Comparativo completo em [`research/02-linguagem.md`](../research/02-linguagem.md).

**1. A pesquisa brasileira contradiz a global.** Código Fonte 2026 (17.046 respondentes, coleta fev–jun/2026): Java 16,5%, C# 14,6%, TypeScript 14,1%, Python 13,8%, JavaScript 11,7%. Frameworks: Spring Boot 14,1%, .NET 13,7%. **Java + C# = ~31% do mercado dev empregado no Brasil.** O Stack Overflow Survey 2025 (JS 66%, Python 58%) mede uso global, não contratação brasileira — é a razão pela qual o conteúdo em português repete "JS e Python lideram", e para esta decisão isso é enganoso.

**2. A hipótese Brasília/DF se confirma, mas por outro mecanismo.** O DF fica em ~2–3% do total nacional para *todas* as linguagens — não existe concentração estatística de Java. O que existe é concentração de **empregador**: as vagas de dev em Brasília saem quase todas de consultorias/fábricas govtech (Basis, Engesoftware, Mirante, Implanta, Place, DATAEASY, Global HITSS), e essas pedem Java+Spring+Angular ou .NET+Angular. Reforçado pela demanda pública (edital Dataprev de fábrica de software com lote principal em Java; legado Serpro/Demoiselle).

**3. Reviravolta que muda a conclusão.** Python lidera o **volume bruto** de vagas no DF (111 vs 61 de Java, Glassdoor) — mas em dados/BI/automação/analista, não em fábrica de software. Órgão federal gera muita demanda de dado. Como o escopo deste mapa é "qualquer área de TI", esse pool conta.

**4. Recomendação: Python + SQL.** Custo explícito: não casa por keyword com a vaga de *dev* mais numerosa de Brasília, e não exercita tipagem estática, build system nem injeção de dependência — o vocabulário da entrevista corporativa BR. **Mitigação marcada como obrigatória, não opcional:** se o alvo incluir vaga de dev no DF, o *segundo* projeto precisa ser Java/Spring.

**Confiabilidade — ler antes de usar:**
- Código Fonte 2026: fonte primária, datada, alta confiança.
- As contagens diretas em portais **falharam em boa parte**: Catho e Adzuna devolveram 403, Indeed não expõe total, e o LinkedIn público retornou os mesmos números com e sem filtro de senioridade (cache provável). Marcadas como baixa confiança.
- Duas fontes frágeis, sinalizadas no arquivo: o edital Dataprev (URL original deu 404 — reconfirmar antes de citar) e os snapshots do Glassdoor (data imprecisa, extraídos de títulos indexados).

**Ironia registrada:** a dificuldade de contar vagas por portal é exatamente o problema que este bot resolve. Vale reabrir esta pergunta com dados próprios após ~4 semanas de coleta.

**A decisão em si não é deste ticket** — acontece em [Fechar fontes e stack](./04-fechar-fontes-e-stack.md), junto com o inventário de fontes.
