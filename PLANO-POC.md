# PLANO-POC — 4 semanas, 12 peças, GO/ADJUST/STOP

**Escopo:** 4 semanas · 12 peças (9 carrosséis + 3 reels) · 1 conta (`@vidavesso`) · 2 pilares: **IA que vira sistema** e **Vida como projeto aberto** (definidos em `project/PILARES.md`).
<!-- TODO-VITOR: data de início da semana 1 -->

Pré-condição: `CHECK-DIA-0.md` completo (conector presente + Gate 0 rodado).

## Cadência semanal (3 peças/semana)

| Etapa | Gate humano | Quem/o quê |
|---|---|---|
| Capturar insumos (áudio/mensagem) | — | Telegram/WhatsApp → thread do Manus |
| Pontuar (score-editorial) | — | skill |
| **Selecionar 3 de ~8 ideias** | **Gate 1 (~5 min/semana)** | Vitor |
| Brief + geração (gerar-carrossel / roteiro de reel) | — | skills; 1 task = 1 etapa, sempre |
| Crítica (anti-generico) + fact-check | — | skills |
| **Aprovar a cópia** | **Gate 2 (alvo: 90s/peça)** | Vitor |
| **Publicar** | **Gate 3: manual nas 4 primeiras peças; se erro = 0, pode virar automático na semana 3** — caminho acelerado em `AUTOMACAO.md` §1 (1 teste de publicação por formato substitui as 4 peças), pendente de decisão do Vitor | Vitor / conector |
| Coletar métricas 72h e 7d → ledger | — | conector (ou app, se o Gate 0 reprovou) |
| Análise (analise-semanal) | — | skill |

Gates 1 e 2 permanecem **para sempre** — é onde o leverage humano é desproporcional.

**Como funciona a automação (semana 3+, se erro = 0):** não existe fila de rascunhos nativa
no Manus — o agendamento é da **task**, não do post. Automatizar = criar uma Scheduled Task
por publicação (custo medido: ~12 créditos), e a coleta 72h/7d é outra Scheduled Task
própria. Sempre 1 Scheduled Task = 1 etapa; nunca ideação→publicação numa execução só.

## Alvos operacionais

| Alvo | Meta |
|---|---|
| Aprovação sem reescrita | ≥60% |
| Intervenções por peça | ≤2 |
| Tempo humano por peça | ≤5 min |
| Publicação bem-sucedida | ≥90% |
| Créditos por peça | ≤600 |
| Erro factual publicado | 0 |
| Consistência visual | ≥90% |
| Insight acionável | ≥1/semana a partir da semana 2 |

## Métricas editoriais (SÓ as seis permitidas)

- Atenção: `views`, `reach` · Valor percebido: `saves`, `shares` · Conversa: `comments`
- **Métrica-norte: `sends/reach`** (= shares/reach). Likes é o sinal mais fraco. Volume não é estratégia.
- Dado que o conector não devolver: literal `INDISPONIVEL` no ledger — nunca estimativa.

## Validação × monitoramento (combinado de 10/08/2026)

Duas coisas diferentes, nunca misturadas:

- **Funcionamento de fluxo** (skill nova, etapa nova, automação do Gate 3): prova-se em
  **horas, teto de 3 dias**, com execução real ponta a ponta em dado pequeno
  (`CHECK-DIA-0.md` §3, Teste A é o modelo). Nada entra na rotina sem esse smoke.
- **Performance e objetivo**: monitoramento com cadência fixa —
  - por peça: coleta 72h e 7d no ledger (com `origem_dado`);
  - por semana: fechamento com a skill analise-semanal + atualização da tabela de alvos
    operacionais acima + toque nas hipóteses (`hipoteses.csv`);
  - semana 4: decisão GO/ADJUST/STOP abaixo, com a tabela completa como evidência.

## Decisão ao fim das 4 semanas

- **GO** — todos os alvos operacionais + ≥1 hipótese validada ou refutada com dados + custo ≤US$40/mês.
- **ADJUST** — aprovação sem reescrita 35–59% OU tempo humano 5–15 min/peça → iterar `VOZ.md` e a skill anti-generico, repetir por 2 semanas.
- **STOP → arquitetura própria** — qualquer um destes: aprovação <35% após 2 iterações do brand file · falha de publicação >20% · conector indisponível/instável · custo >US$100/mês.

## Custo (vigiar task a task)

Referência medida: 89–148 créditos por task de pesquisa; 12 para agendar. O Manus não tem preview de custo — registre `creditos` em `publicados.csv` a cada task.
