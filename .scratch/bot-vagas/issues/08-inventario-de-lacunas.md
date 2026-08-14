# Inventário de lacunas e divisão do trabalho

Type: grilling
Status: open
Blocked by: 04, 06, 11
Parent: [Mapa: Bot de vagas de estágio/júnior em TI](../map.md)

## Question

Este é o ticket que entrega metade do que o Luiz pediu: **quais são as lacunas dele, e quem digita o quê.**

Com stack e infra fechadas, listar toda técnica que o projeto exige e classificar cada uma em três colunas:

- **Nunca digitei** → primeira ocorrência é dele.
- **Já digitei na mão** → do agente.
- **Existe nos meus projetos mas quem escreveu foi um agente** → conta como *nunca digitei*.

Lista inicial de técnicas a classificar (expandir conforme a stack escolhida):

| Técnica | Onde aparece no projeto |
|---|---|
| Chamar HTTP e tratar resposta/erro | coletor, notificador |
| Parsear HTML | coletor |
| Parsear JSON e mapear pra tipo do domínio | coletor |
| Navegador headless | coletor, se a fonte exigir |
| Modelar tabela e escrever schema | persistência |
| Escrever SQL na mão (não ORM) | persistência |
| Deduplicação / diff entre dois conjuntos | núcleo do bot |
| Escrever teste antes do código | tudo |
| `.env`, segredos, `.gitignore` | tudo |
| Workflow de CI em YAML | agendamento |
| Cron / expressão de agendamento | agendamento |
| Ler log de execução remota pra debugar | operação |
| Tratar falha silenciosa e alertar | resiliência |
| Git: branch, commit atômico, PR | tudo |

Para cada item classificado como lacuna, definir também: **qual é o exercício mínimo** que prova o aprendizado, e **qual o critério de "aprendi"** (sabe refazer sem consultar? explica por que funciona?).

**Saída deste ticket:** a tabela preenchida, mais os tickets de execução da v1 já recortados e marcados "mão sua" / "mão minha". É aqui que a névoa de implementação vira mapa.

**Depende de 04 e 06** porque a lista de técnicas só é real depois de linguagem e infra escolhidas.
