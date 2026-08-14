# Inventário parte 2: agentes de integração e demais fontes

Type: research
Status: open
Blocked by: —
Parent: [Mapa: Bot de vagas de estágio/júnior em TI](../map.md)

## Question

O [Inventário de fontes de vagas](./01-inventario-de-fontes.md) foi bem executado sobre uma lista de candidatas **enviesada para job board de tecnologia**. Ele perdeu a categoria que provavelmente domina o estágio no Brasil: os **agentes de integração**, que têm convênio direto com empresa e universidade e cuja vaga muitas vezes nunca aparece em ATS público.

Aplicar os **mesmos 6 eixos** do ticket 01 (acesso técnico, autenticação, ToS/robots, cobertura, campos disponíveis, estabilidade) às fontes não cobertas, levantadas pelo próprio usuário:

**Agentes de integração** (prioridade — categoria inteira ausente do inventário):
1. CIEE
2. Nube
3. Agiel
4. Super Estágios
5. Cia de Talentos
6. Companhia de Estágios

**Plataformas e agregadores não cobertos:**
7. Eureca
8. Plooral
9. Solides (ATS, análogo à Gupy — verificar se tem portal/API pública)
10. Empregare
11. Remotar (foco remoto BR)
12. EstágioTrainee
13. InfoJobs (o ticket 01 declarou que não conseguiu medir — fechar essa lacuna)
14. Glassdoor (o ticket 02 usou dados dele; verificar viabilidade de coleta e anti-bot)

**Categoria à parte — não são fontes agregadoras, são empregadores/processos únicos:**
15. Programa de estágio do Senado Federal
16. BairesDev

Para 15 e 16, a pergunta é diferente: vale um coletor dedicado a *um* empregador? Provavelmente não para a v1 — avaliar se cabem como "página de carreira monitorada" numa fase posterior, ou se saem de escopo.

## Restrições

- Mesmo critério de honestidade do ticket 01: marcar `[V]` verificado com requisição real vs. `[P]` presumido. **Não inventar volume.**
- Verificar `robots.txt` e ToS de cada uma. Reprovar por ToS é resultado válido.
- Atenção especial ao **login obrigatório**: agentes de integração costumam esconder a vaga atrás de cadastro. Se a vaga só é visível logado, isso muda tudo — registrar explicitamente.
- Medir, onde possível, a **cobertura de TI** especificamente. Um agente de integração com 5.000 vagas e 12 de TI é pior que um board pequeno e focado.
- Comparar com a linha de base já medida: Gupy = ~3–4 vagas de TI novas/dia no recorte (remoto BR + DF).

## Entregável

Comparativo em `research/10-fontes-parte-2.md`, e uma **recomendação de ordem de adição** que se integre à ordem já recomendada no ticket 01 (Gupy → Programathor → Vagas.com). A pergunta final: alguma dessas deveria *substituir* uma das três, ou todas entram depois?

A decisão não é deste ticket — é de [Fechar fontes e stack](./04-fechar-fontes-e-stack.md).
