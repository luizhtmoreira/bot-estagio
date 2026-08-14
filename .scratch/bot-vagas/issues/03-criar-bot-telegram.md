# Criar o bot no Telegram e obter o token

Type: task
Status: open
Blocked by: —
Parent: [Mapa: Bot de vagas de estágio/júnior em TI](../map.md)

## Question

Trabalho manual que só o Luiz pode fazer, e que bloqueia qualquer discussão sobre formato de mensagem e sobre onde guardar segredos.

Checklist (HITL — o agente não tem acesso à conta do Telegram):

1. Abrir o Telegram e conversar com **@BotFather**.
2. `/newbot` → escolher um nome de exibição e um username terminado em `bot`.
3. Guardar o **token** que o BotFather devolve. **Não commitar em lugar nenhum.** Colocar num `.env` local (e criar o `.gitignore` antes disso).
4. Mandar qualquer mensagem para o bot recém-criado (ele só pode te escrever se você iniciar a conversa).
5. Descobrir o seu **chat id**: acessar `https://api.telegram.org/bot<TOKEN>/getUpdates` no navegador e ler o campo `message.chat.id`.
6. Testar o envio na mão, sem escrever código ainda: montar a URL `https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<CHAT_ID>&text=oi` e abrir no navegador.

O passo 6 é deliberado: é a sua primeira chamada de API feita à mão. Não pule para a biblioteca.

**Resolvido quando:** a mensagem "oi" chegou no seu Telegram, disparada por você.

**A resposta deve registrar:** onde o token está guardado, o chat id (ou onde ele está guardado), e o nome/username do bot.
