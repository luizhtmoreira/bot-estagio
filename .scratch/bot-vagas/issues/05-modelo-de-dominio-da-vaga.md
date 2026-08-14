# Modelo de domínio: o que é uma vaga, o que é "nova", o que é "relevante"

Type: grilling
Status: open
Blocked by: 01
Parent: [Mapa: Bot de vagas de estágio/júnior em TI](../map.md)

## Question

O bot inteiro depende de três definições que ninguém escreveu ainda. Esta sessão usa `/domain-modeling` para fixá-las na linguagem do projeto.

1. **Identidade da vaga.** O que faz duas linhas coletadas em dias diferentes serem *a mesma vaga*? A URL? Um id da fonte? Um hash de `(empresa, título, local)`? O que acontece quando a mesma vaga aparece em duas fontes — é uma vaga ou duas? E quando a empresa reposta a mesma vaga uma semana depois?
2. **"Nova".** Nova para o mundo (data de publicação) ou nova para mim (nunca te mostrei)? Não são a mesma coisa: na primeira execução, *tudo* é novo para você e nada é novo para o mundo. Como se comporta o dia 1?
3. **"Relevante".** ⚠️ **Input já fixado:** vale o princípio *coleta larga, entrega filtrada* (ver Notes do mapa). A coleta puxa **todas as vagas de TI**, sem recorte de área nem de senioridade. A pergunta abaixo é, portanto, sobre o **filtro de entrega**, não sobre o que coletar — e o filtro é por pessoa. Como o filtro decide que uma vaga é estágio/júnior de TI em remoto-BR ou Brasília/DF. Os títulos são bagunçados na prática ("Estágio em Tecnologia", "Jovem Aprendiz TI", "Dev Jr.", "Trainee"). Onde fica o corte? Vale mais errar mostrando lixo ou errar escondendo vaga boa? (Para quem está procurando estágio, falso negativo dói muito mais que falso positivo — mas isso precisa ser dito, não presumido.)
4. **Dois destinatários.** O projeto passou a ter duas pessoas ([Trazer um segundo dev](./11-segundo-dev-no-projeto.md)), e o bot serve as duas desde a v1. Isso é decisão de schema, não de apresentação: filtro e destino passam a ser **por pessoa**. Perguntas: uma coleta compartilhada com filtros distintos por destinatário, ou dois pipelines independentes? "Já mostrei essa vaga" é por pessoa ou global? Decidir agora custa uma coluna; decidir depois custa uma migração.

5. **Vocabulário.** Fixar os termos que o código vai usar: *vaga*, *coleta*, *fonte*, *snapshot*, *novidade*, *sumiço*. Escrever num `CONTEXT.md`.

**Depende de 01** porque a identidade da vaga só pode ser decidida sabendo quais campos as fontes realmente expõem — se nenhuma dá id estável, a resposta muda.
