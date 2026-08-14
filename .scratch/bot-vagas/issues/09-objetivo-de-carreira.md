# Objetivo de carreira e o que o bot é, afinal

Type: grilling
Status: resolved
Blocked by: —
Parent: [Mapa: Bot de vagas de estágio/júnior em TI](../map.md)

## Question

"Mais empregável" não significa nada até saber **empregável para quê**. A pesquisa de linguagem entregou o dado de mercado, mas não pôde recomendar com firmeza porque o alvo nunca foi declarado.

Duas perguntas acopladas:

1. **Qual é o alvo de carreira?** Dev backend, front, full-stack, dados/BI, infra/DevOps, QA, segurança — ou "qualquer porta de entrada"? E o horizonte: a primeira vaga é degrau descartável ou já é a direção?

2. **Qual dos dois empregos do bot domina?** O bot é (a) **instrumento** — precisa rodar rápido pra te alimentar vaga todo dia — ou (b) **portfólio/trilha** — precisa casar com a vaga-alvo e ensinar o vocabulário certo? A escolha de stack muda conforme a resposta, e as duas não se maximizam juntas.

**Tensão a grelhar:** "quero entrar logo" e "quero a linguagem mais empregável" são objetivos diferentes e podem apontar para stacks opostas. Em Brasília, Java/.NET é o maior volume de vaga de *dev* mas é caminho de fábrica govtech; Python é o maior volume bruto mas concentrado em dados/BI/automação. Escolher errado não é fatal — escolher sem saber que houve uma escolha, é.

**Sub-questão:** a urgência é real? Prazo de formatura, exigência de estágio obrigatório, necessidade financeira? Um prazo duro reordena o mapa inteiro — pode valer o bot tosco em duas semanas em vez do bot bem-feito em dois meses.

## Answer

**Alvo declarado:** ML → MLOps, ML engineering, AI engineering.
**Função do bot:** mista — "o mais rápido possível aprendendo".
**Urgência:** pressão sem data dura.

### 1. A tensão instrumento-vs-portfólio se dissolveu

Ela existia porque "entrar rápido" e "linguagem empregável" podiam apontar para stacks opostas (Python vs. Java govtech). Com o alvo em ML/MLOps, **Python é as duas respostas ao mesmo tempo**: é a linguagem que faz o bot rodar mais rápido *e* a linguagem do alvo de carreira. Não há trade-off a arbitrar.

**Consequência:** a mitigação "segundo projeto obrigatório em Java/Spring", herdada da pesquisa de linguagem, **cai**. Ela pressupunha alvo de dev backend em fábrica govtech, que não é o caso. Removida de *Out of scope*.

### 2. Correção necessária sobre o alvo

MLOps e ML engineering **quase não contratam estágio direto** — são papéis que exigem infra + ML simultaneamente e enviesam sênior. Isso não invalida o alvo; muda a rota até ele. As portas de entrada reais, em ordem de acessibilidade:

1. **Dados / analytics / engenharia de dados** — a porta mais larga, e a mais próxima de MLOps na prática diária.
2. **AI engineering / LLM apps** — hoje contrata júnior de verdade, e demanda menos matemática que ML clássico.
3. **Backend Python** — vira ML platform por dentro da empresa.

O filtro do bot deve, portanto, capturar vaga de **dados e backend Python**, não só o que tem "ML" no título. Isso é input direto para o ticket de modelo de domínio.

### 3. O reenquadramento que aumenta o valor do projeto

Este bot **é um pipeline de dados**: ingestão de múltiplas fontes → normalização → deduplicação → persistência → entrega agendada. Isso não é analogia, é literalmente a arquitetura de um ETL.

As partes que pareciam "chatas" — schema, agendamento, idempotência, detectar coleta quebrada, qualidade de dado — são **exatamente as competências de MLOps/engenharia de dados**. Sob o alvo declarado, elas deixam de ser imposto e viram o miolo do portfólio.

**Consequência para o mapa:** os tickets de persistência, agendamento e resiliência sobem de prioridade em vez de serem cortados por escopo. O ticket de inventário de lacunas deve pesá-los como aprendizado de alto valor, não como andaime.

### 4. Sem prazo duro

Sem data, mas com pressão. Justifica a estratégia de **uma fonte só na v1** — mensagem chegando no celular o quanto antes — sem justificar cortar a camada de dados, que é onde mora o valor de carreira.
