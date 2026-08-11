# AUTOMACAO — o que já pode rodar sozinho, em que ordem, e como provar em horas

Pergunta do Vitor em 10/08/2026: *"se você já consegue me dar toda essa recomendação e já
configuramos tudo que permite automatizar esse fluxo, por que eu vou ter que gerar as
publicações manuais?"* — pergunta certa. Este documento é a resposta.

## 1. Três "manuais" estavam sendo confundidos

| O que | Estava manual | Precisa ser? | Por quê |
|---|---|---|---|
| **Gerar o texto** | sim — o Claude escreveu as 3 peças no chat | **NÃO** | erro de processo, corrigido abaixo |
| **Aprovar** (Gates 1 e 2) | sim | **SIM, para sempre** | é a tese do projeto, não uma limitação |
| **Publicar** (Gate 3) | sim, nas 4 primeiras peças | **NÃO** — 1 teste por formato basta | o "4 peças" era proxy de evidência; há proxy mais rápido |

### O erro que eu cometi

Eu entreguei o texto das 3 peças prontas no chat. Isso é **fora do sistema** — e corrompe
a medição da POC. O alvo `aprovação sem reescrita ≥60%` mede a saída do **Manus**, não a
minha. Se as peças publicadas forem o meu texto, esse número não significa nada e a
semana 1 não gera aprendizado nenhum.

**Correção:** o texto que está no artifact é **referência/fallback**, não o que se publica.
Quem gera é o Manus, a partir do brief `b004`. A primeira medição real do projeto é
comparar a saída dele com a referência — e isso está disponível em uma hora, não em quatro
semanas.

### Por que o Gate 3 pode acelerar

O handoff pede publicação manual nas 4 primeiras peças. O motivo real não é cautela
genérica: é que a API tem limites duros (JPEG ≤8MB, aspect 4:5 a 1.91:1, alt text só em
imagem, sem sticker, carrossel 2–10) e um publicador que erra, erra **em público**.

"4 peças" era um proxy para "evidência suficiente". Pelo combinado de validação rápida,
existe proxy melhor: **um teste deliberado por formato** (1 carrossel, 1 reel, 1 post),
verificando corte, ordem dos slides, caption e alt text logo após publicar. Três testes no
mesmo dia cobrem o mesmo risco que quatro peças em duas semanas. Se saírem limpos, o Gate 3
pode virar automático já na semana 1 — sem esperar a semana 3.

O que NÃO muda: Gates 1 e 2 continuam humanos para sempre.

## 2. A arquitetura automatizada — 7 Scheduled Tasks

Regra inviolável do handoff (§3.5): **1 Scheduled Task = 1 etapa**. Nunca encadear
ideação→publicação numa execução só. Não existe fila de rascunhos: o agendamento é da
*task*, não do post.

| # | Task | Quando | Lê | Escreve | Skill |
|---|---|---|---|---|---|
| T1 | Pontuar insumos novos | diária | thread de captura | `ideias.csv` | score-editorial |
| — | **Gate 1 — você escolhe 3 de ~8** | seg, ~5 min | `ideias.csv` | `status=selecionada` | humano |
| T2 | Brief + geração | após o Gate 1 | ideias selecionadas | `briefs.csv` + texto | gerar-carrossel |
| T3 | Crítica | após T2 | o texto | veredito | anti-generico + fact-check |
| — | **Gate 2 — você aprova a cópia** | ~90s/peça | texto aprovado pelo crítico | — | humano |
| T4 | Publicar | horário da peça | peça aprovada | `publicados.csv` | conector |
| T5 | Coletar 72h | +72h de T4 | conector | `metricas.csv` | conector |
| T6 | Coletar 7d | +7d de T4 | conector | `metricas.csv` | conector |
| T7 | Análise semanal | domingo | ledger | relatório | analise-semanal |

Os gates humanos **não são bloqueios técnicos** — são estados de espera entre tasks. O
sistema fica pronto inteiro; o que passa por você são dois checkpoints curtos por semana.

**Custo estimado por peça:** agendar custa ~12 créditos por task (medido); tasks de
geração/análise ficaram em 89–148 créditos nas medições do handoff — que são de tasks de
*pesquisa*, não deste pipeline. Trate como ordem de grandeza até medir: registre `creditos`
em `publicados.csv` a cada peça. Teto da POC: 600/peça.

## 3. Teste de funcionamento de cada task (combinado: horas, não dias)

Cada task entra em produção só depois de passar no seu smoke. Nenhum deles precisa de
audiência nem de janela de dado:

| Task | Smoke | Prova o quê |
|---|---|---|
| T1 | 1 insumo real → linha em `ideias.csv` → `ledger_check.py` | escrita no Sheets, colunas certas, score coerente |
| T2 | 1 brief → texto no formato exato da skill | releitura de VOZ, formato, rastreio ao `id_ideia` |
| T3 | **controle negativo obrigatório** (abaixo) | que o crítico realmente rejeita |
| T4 | 1 publicação de teste por formato | corte, ordem dos slides, caption, alt text |
| T5/T6 | rodar logo após publicar | conector devolve SÓ as seis métricas |
| T7 | rodar com 3 peças no ledger | sai com 5 ângulos + 3 "parar de postar" |

### O controle negativo do T3 — o teste mais importante de todos

Um crítico que aprova tudo é pior que crítico nenhum: dá sensação de qualidade sem
entregar qualidade. Então o smoke do anti-generico tem **duas** entradas:

1. um texto deliberadamente genérico ("No mundo de hoje, a IA veio para revolucionar…")
   → **tem que voltar `REJEITADO`**, citando o critério e o trecho;
2. o texto de referência aprovado → tem que voltar `APROVADO`.

Se o item 1 passar, o crítico está decorativo — pare tudo e conserte a skill antes de
publicar qualquer coisa. Vale a mesma lógica para métricas: `gate0_diff.py` já tem o
controle negativo embutido nas fixtures (`gate0_manus_ruim.csv` reprova).

### O verificador do ledger automatizado

Quando as tasks escrevem sozinhas, o defeito típico não é valor errado — é **referência
quebrada, id duplicado, coluna a mais ou etapa pulada em silêncio** (§3.5: o Manus pula
fonte sem avisar). Rode a cada ciclo, leva segundos:

    python3 scripts/ledger_check.py ledger/csv

Ele reprova brief que aponta para ideia inexistente, peça publicada duas vezes, métrica de
peça que não existe, `sends_por_reach` calculado errado, coluna de métrica proibida em
qualquer aba, e avisa quando uma peça publicada ficou sem coleta de 72h ou 7d.

## 4. As ondas — o que dá para começar hoje

| Onda | O que | Quando dá para começar | Gate |
|---|---|---|---|
| 1 | Manus gerando (T2+T3) com gates humanos | **hoje** | nenhum |
| 2 | Publicação e coleta automáticas (T4–T6) | **esta semana**, após 1 teste por formato | OAuth + publicação: seus |
| 3 | Captura automática (T1) — áudio/nota → `ideias.csv` | esta semana | — |
| 4 | Loop de aprendizado fechado (T7 → propõe `PADROES.md`) | semana 2+ | precisa de dados reais |

A Onda 3 é onde entra a ponte com o AuraSite (`PONTE-AURASITE.md`, cenário C): a ingestão
dele já faz transcrição de áudio e curadoria de corpus, que é exatamente o insumo do T1.

**O que genuinamente não acelera:** a leitura editorial. reach, saves e shares dependem de
audiência real ao longo de dias — 12 peças em 4 semanas é a amostra mínima para afirmar
qualquer coisa sobre o que funciona. Mas isso é **monitoramento**, e roda em paralelo: o
sistema pode estar 100% automatizado na semana 1 e ainda assim levar 4 semanas para
ensinar o que a audiência responde. Uma coisa não segura a outra.

## 5. O que continua sendo gate meu (não posso fazer por você)

Autorizar OAuth de qualquer conector · publicar, agendar ou enviar conteúdo · criar as
Scheduled Tasks dentro da sua conta Manus · comprar ou fazer upgrade de plano.

Posso: escrever e testar scripts, redigir as instruções exatas de cada task, revisar saída,
rodar os verificadores e diagnosticar falha. A automação é sua para ligar — o desenho e a
prova de funcionamento são meus para entregar.
