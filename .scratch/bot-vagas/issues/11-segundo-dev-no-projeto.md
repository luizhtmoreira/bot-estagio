# Trazer um segundo dev para o projeto

Type: grilling
Status: resolved
Blocked by: —
Parent: [Mapa: Bot de vagas de estágio/júnior em TI](../map.md)

## Question

Luiz tem um amigo na mesma situação (busca de estágio, mesma faculdade, mesma cidade) e quer saber se traz ele para o projeto sem perder aprendizado.

**Perfil levantado:**
1. **Habilidade prática:** mesma situação do Luiz — teoria boa, nunca digitou na mão.
2. **Histórico:** trabalho de faculdade em grupo de 6; os dois fizeram >60% sozinhos. Ele era o **líder**, Luiz o **braço direito**.
3. **Alvo de carreira:** nenhum definido. "Qualquer coisa."
4. **Sincronia:** mesma cidade, mesma faculdade. Blocos síncronos a confirmar com ele.
5. **O bot serve os dois?** Não respondido — mas a recomendação abaixo depende disso.

## Recomendação (pendente de confirmação)

**Sim, trazer.** A simetria de habilidade prática (item 1) é o fator decisivo: elimina o risco de o Luiz virar passageiro, porque não há quem carregue. Travar no mesmo degrau é onde parear rende mais. O item 2 comprova confiabilidade — o amigo aparece.

### Riscos identificados

**R1 — A hierarquia líder/braço-direito se reinstala por hábito.** Numa entrega de faculdade ela funcionou. Num projeto de aprendizado ela é destrutiva: o Luiz quer ser quem decide **e** quem digita. O risco não exige má-fé de ninguém; é inércia. **Mitigação: dizer isso em voz alta para o amigo, não combinar internamente.**

**R2 — Motivação assimétrica (item 3).** Luiz tem alvo e pressão; o amigo não tem nenhum dos dois. Por volta da hora ~12, quando a novidade acaba e o bot ainda não serve, o Luiz continua por necessidade e o amigo para por tédio. **Mitigação: o bot serve os dois desde a v1** — filtro dele, Telegram dele. Interesse próprio imediato retém melhor que curiosidade. Isso responde o item 5: sim.

**R3 — Dividir em vez de parear.** O modo natural e mais rápido, e o que destrói o aprendizado: cada um aprende a própria metade, e escolhe a metade em que já é confortável.

### Condições — se qualquer uma cair, a recomendação inverte

1. **Parear, não dividir.** Um teclado, um problema, revezando a cada 25 min no cronômetro.
2. **Luiz digita primeiro em cada técnica nova**, explicitamente para contrariar R1.
3. **O bot serve os dois desde a v1.**

### Custo

Velocidade cai ~30–40% em linhas por hora. Estimativa de 30–50h **continua valendo quase inteira — não vira 15–25h cada**: não é divisão de trabalho, é o mesmo trabalho com duas cabeças. O ganho é retenção e menor chance de desistência, não velocidade. Bônus: parear elimina conflito de merge, categoria de dor que costuma afundar dupla iniciante no git.

## O que "parear" significa na prática

Esclarecimento necessário — o Luiz entendeu inicialmente como "um teclado físico" e assumiu o modelo "eu aqui, ele lá, e usamos o GitHub", que é **trabalho paralelo**, ou seja, o modo "dividir" que o R3 desaconselha.

**Parear = uma pessoa digitando por vez, no mesmo problema, ao mesmo tempo.** Podem estar em casas diferentes; não podem estar em arquivos diferentes.

- **Driver**: mão no teclado, **narra em voz alta** o que faz e por quê. Não decide sozinho.
- **Navigator**: não digita. Pensa um passo à frente, lê doc, questiona, pega erro antes de rodar. É a cadeira mais cansativa.
- **Troca a cada 25 min no cronômetro**, independente do estado do código. É o timer que impede a hierarquia líder/braço-direito de se reinstalar — não a boa intenção.

Remoto: call com tela compartilhada (Discord/Meet) resolve, zero setup. VS Code Live Share se quiserem dois cursores.

**Git continua em cena.** Repositório, branch, commit, push e PR seguem — inclusive porque git é uma das técnicas da tabela de lacunas e precisa ser digitada. O que some é só o *conflito de merge*, porque não há duas versões divergentes do mesmo arquivo. Commita-se da máquina de quem estiver de driver.

**Por que trabalho paralelo otimiza a coisa errada aqui:** ele maximiza código por hora, e código por hora não é escasso (o agente produz de graça). O escasso é *hora com a mão do Luiz no teclado num problema que ele não sabe resolver* — e o paralelo corta isso pela metade. Efeito colateral decisivo: em paralelo, cada um pega a parte em que já se sente confortável. Sempre.

### Modo híbrido (o realista)

| Situação | Modo |
|---|---|
| Primeira ocorrência de uma técnica nova | **Pareado**, com revezamento de 25 min |
| Repetição de técnica que os dois já digitaram | Paralelo, GitHub normal |
| Decisão de design | Junto, pode ser conversa sem código |
| Setup, config, boilerplate | Agente |

Consequência: não são necessárias *muitas* horas síncronas, e sim as horas **certas** síncronas — as primeiras vezes. Dois blocos de ~2h por semana provavelmente bastam, com o resto andando em paralelo.

## Answer

**2026-08-14 — O amigo foi convidado e aceitou as três condições.** O projeto passa a ser de duas pessoas.

Condições aceitas:
1. Parear com revezamento de teclado a cada 25 min em técnica nova, em vez de dividir módulos.
2. Luiz digita primeiro em técnica nova — com o recíproco: em técnica que o Luiz já digitou, o segundo dev digita primeiro.
3. O bot serve os dois desde a v1 — filtro e destino próprios para cada um.

### Consequências para o mapa

**A regra "primeira vez é sua" foi reescrita para dois** — ver `## Notes` no [mapa](../map.md). Resumo: "primeira vez" passa a significar *primeira ocorrência da técnica para aquela pessoa*, e a primeira ocorrência absoluta de qualquer técnica é pareada, para que ambos digitem.

**Dois destinatários viraram requisito de v1, não névoa.** Filtro e destino por pessoa entram no schema desde o início. Repassado para o [modelo de domínio](./05-modelo-de-dominio-da-vaga.md), onde é muito mais barato decidir antes da tabela existir.

**A escada de saída passa a ser da dupla, não individual.** O timebox de 30 min conta para os dois travados no mesmo problema — dois travados juntos por 30 min é o gatilho da dica, não 30 min cada.

### Riscos que continuam vivos

**R2 (motivação assimétrica) não foi eliminado, só mitigado.** O segundo dev segue sem alvo de carreira definido; a retenção dele depende inteiramente do bot entregar vaga útil para ele. Isso torna a condição 3 crítica em vez de simpática: **se a v1 só servir o Luiz, o R2 volta com força total por volta da hora 12.**

**R1 (hierarquia líder/braço-direito) depende do cronômetro, não do acordo.** Aceitar a condição é fácil; sustentá-la na hora 20 é que é o teste. Sinal de alerta a monitorar: se o revezamento começar a ser pulado "porque ele estava no meio de uma coisa", a regra já caiu.

### Logística em aberto

Frequência dos blocos síncronos não foi fixada. Estimativa de trabalho: ~2 blocos de 2h por semana bastam, porque só as *primeiras vezes* precisam ser síncronas.

## Para resolver este ticket

Falta a conversa com o amigo. Resolver quando houver resposta para:
- Ele topa parear com revezamento de teclado, em vez de dividir módulos?
- Ele consegue blocos síncronos de ~2h com que frequência?
- Ele topa a regra "Luiz digita primeiro em técnica nova"? (E o recíproco vale: em técnica que o Luiz já digitou, quem digita primeiro é ele.)
- Confirmado que o bot manda vaga para ele também?

Se a resposta a qualquer uma das duas primeiras for não, **é melhor fazer sozinho.**
