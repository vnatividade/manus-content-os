# TASKS-MANUS — os 7 prompts do pipeline, prontos para colar

Arquitetura em `AUTOMACAO.md`. Aqui está o texto literal de cada task.

**Antes de usar:** substitua `<LINK-DA-PLANILHA>` pelo link do seu ledger no Google Sheets
em todas as tasks que tocam o ledger (T1, T2, T4, T5, T6, T7). Faça isso uma vez e guarde
os prompts prontos.

**Regras que valem para todas:** toda task roda DENTRO do Manus Project do Content OS
(nunca numa thread solta — é o Project que carrega VOZ.md, PILARES.md, FORMATOS.md,
REGRAS-DURAS.md e PADROES.md). Uma task = uma etapa. Nenhuma task encadeia com a seguinte.

---

## T1 — Pontuar insumos novos

*Quando:* diária, ou sob demanda quando você jogar insumo novo.
*Skill:* score-editorial. *Escreve:* aba `ideias`.

```
Tarefa: pontuar insumos novos. UMA etapa apenas.

Ledger: <LINK-DA-PLANILHA>

Passos:
1. Releia PILARES.md da knowledge base agora. Nunca use versão em cache.
2. Considere apenas os insumos que eu colei abaixo. Não invente insumo.
3. Para cada insumo, aplique a skill score-editorial.
4. Grave uma linha nova na aba `ideias` do ledger, respeitando exatamente este cabeçalho:
   id,data_captura,insumo_bruto,origem,pilar,score_so_eu,score_evidencia,score_tensao,score_utilidade,score_total,status
   - id sequencial continuando o último já existente na aba
   - status = capturada
   - score_total = soma dos quatro eixos
5. Responda no chat apenas: os ids criados e uma linha de justificativa por eixo.

Proibido: gerar brief, gerar peça, publicar, criar dashboard/PDF/gráfico/resumo extra.
Se não houver insumo novo, responda "sem insumo novo" e pare.

INSUMOS:
[cole aqui os insumos, um por bloco]
```

---

## T2 — Brief + geração de UMA peça

*Quando:* depois do Gate 1 (você seleciona as ideias).
*Skill:* gerar-carrossel. *Escreve:* aba `briefs` + o texto no chat.

```
Tarefa: gerar UMA peça. UMA etapa apenas — não publique, não agende, não gere a próxima.

Ledger: <LINK-DA-PLANILHA>
Ideia de origem: <ID-DA-IDEIA> (já selecionada por mim no Gate 1)
Formato: carrossel de 6 slides

Pré-condições — pare e reporte se qualquer uma falhar:
1. Releia VOZ.md e REGRAS-DURAS.md da knowledge base AGORA. Nunca use versão em cache.
2. Confirme que a ideia existe na aba `ideias` do ledger. Sem insumo real, não há peça.

Passos:
1. Escreva o brief e grave na aba `briefs`, com este cabeçalho exato:
   id_brief,id_ideia,pilar,formato,angulo,hook,n_slides,cta,estrutura,data
2. Aplique a skill gerar-carrossel usando esse brief.
3. Responda no chat, nesta ordem:
   - primeira linha: id_brief=... id_ideia=...
   - os 6 slides, numerados
   - a caption
   - o alt text de cada slide

Proibido: publicar, agendar, gerar imagem ou arte, criar PDF/dashboard, inventar
experiência pessoal minha, usar número ou citação sem fonte verificável, adicionar
hashtag, adicionar CTA que o brief não pediu.
```

---

## T3 — Crítica (anti-genérico + fact-check)

*Quando:* logo após T2. *Skills:* anti-generico, depois fact-check. *Escreve:* nada.

```
Tarefa: criticar a peça abaixo. Você é crítico, NÃO editor. Não reescreva nada, não
sugira versão melhorada, não "dê um jeitinho".

Passos:
1. Releia VOZ.md da knowledge base agora. Nunca use versão em cache.
2. Aplique a skill anti-generico. Saída exata: `APROVADO`, ou uma linha por critério
   violado no formato `REJEITADO: <critério> — <trecho literal do texto>`.
3. Só se o resultado for APROVADO, aplique a skill fact-check. Saída: a tabela
   afirmação | fonte (link) | status, e a última linha `LIBERADO PARA GATE 2` ou
   `BLOQUEADO: <n> itens`.
4. Não faça mais nada.

TEXTO:
[cole aqui a saída do T2]
```

---

## T4 — Publicar UMA peça

*Quando:* no horário da peça, depois do Gate 2 (você aprova a cópia).
*Escreve:* aba `publicados`. **Exige sua autorização — esta task publica de verdade.**

```
Tarefa: publicar UMA peça já aprovada por mim. UMA etapa apenas.

Ledger: <LINK-DA-PLANILHA>
Conta: @vidavesso
id_brief da peça: <ID>
Formato: <carrossel de N imagens | reel | post>

Passos:
1. Publique no Instagram, via conector, exatamente o conteúdo colado abaixo. Não altere
   uma vírgula do texto nem da caption.
2. Grave uma linha na aba `publicados` com este cabeçalho exato:
   id_peca,id_brief,data,hora,formato,n_slides,hook_tipo,cta,primeira_pessoa,historia_pessoal,framework,permalink,creditos,reescrita,n_intervencoes,tempo_humano_min
   preenchendo permalink com o link retornado e creditos com o custo desta task.
3. Responda apenas: o permalink e a confirmação do que foi publicado.

Proibido: alterar texto ou caption, adicionar hashtag, adicionar sticker, adicionar
música, publicar qualquer coisa que eu não tenha colado aqui.
Se a publicação falhar: NÃO tente de novo com variação. Reporte o erro exato e pare.

CONTEÚDO:
[cole texto final, caption e alt text; anexe as imagens ou o vídeo]
```

---

## T5 — Coletar métricas (janela 72h)

*Quando:* 72h depois de T4. *Escreve:* aba `metricas`.

```
Tarefa: coletar métricas de UMA peça, janela 72h. UMA etapa apenas.

Ledger: <LINK-DA-PLANILHA>
Peça: <ID-DA-PECA> — permalink <LINK>

TRAVA ANTI-FABRICAÇÃO — vale acima de qualquer outra instrução desta task:
"Só reporte métricas que o conector retornar. Se um dado não estiver disponível, escreva
INDISPONIVEL. NUNCA estime, infira ou complete. É proibido reportar: impressions, profile
visits, follower conversion, follows por peça, watch time, demografia, melhores horários —
esses dados não existem nesta integração."

Passos:
1. Peça ao conector do Instagram as métricas desta peça. As únicas que existem são:
   views, reach, saves, shares, comments.
2. Calcule sends_por_reach = shares / reach, com 4 casas decimais. Se shares ou reach for
   INDISPONIVEL, sends_por_reach também é INDISPONIVEL.
3. Grave uma linha na aba `metricas` com este cabeçalho exato:
   id_peca,janela,data_coleta,origem_dado,views,reach,saves,shares,comments,sends_por_reach
   com janela=72h e origem_dado=conector (ou origem_dado=indisponivel se o conector não
   devolveu nada).
4. Responda apenas com a linha exata que você gravou.

Se o conector devolver QUALQUER métrica fora das cinco listadas: não grave nada, reporte
o que ele devolveu, e pare.
```

---

## T6 — Coletar métricas (janela 7d)

*Quando:* 7 dias depois de T4. Idêntica à T5, com duas trocas.

```
[mesmo prompt da T5, trocando "janela 72h" por "janela 7d" e "janela=72h" por "janela=7d"]
```

---

## T7 — Análise semanal

*Quando:* domingo. *Skill:* analise-semanal. *Escreve:* nada (você decide o que vira ação).

```
Tarefa: análise editorial semanal. UMA etapa apenas.

Ledger: <LINK-DA-PLANILHA>

TRAVA ANTI-FABRICAÇÃO — vale acima de qualquer outra instrução desta task:
"Só reporte métricas que o conector retornar. Se um dado não estiver disponível, escreva
INDISPONIVEL. NUNCA estime, infira ou complete. É proibido reportar: impressions, profile
visits, follower conversion, follows por peça, watch time, demografia, melhores horários —
esses dados não existem nesta integração."

Passos:
1. Leia as abas publicados, briefs e metricas — peças dos últimos 30 dias.
2. Deixe FORA das comparações as linhas com origem_dado=indisponivel; reporte-as como
   lacuna explícita.
3. Aplique a skill analise-semanal. Compare apenas dentro do mesmo formato E da mesma
   faixa de reach (faixas = quartis do período). Comparar formatos diferentes entre si, ou
   peças de reach muito distinto, gera conclusão causal falsa e é proibido.
4. Padrão só existe com 2 ou mais ocorrências. Uma peça boa é anedota.
5. Termine obrigatoriamente com: 5 ângulos para dobrar a aposta e 3 coisas para parar de
   postar, cada item citando os ids das peças que sustentam a recomendação.

Proibido: dashboard, PDF, gráfico, estimativa, recomendação sem id de peça.
```

---

## Ordem de ativação

Ligue uma de cada vez, e só depois que o smoke da anterior passar (`AUTOMACAO.md` §3).
T2 e T3 primeiro — são as que provam que o miolo editorial funciona. T4 exige sua
autorização de publicação. T5/T6 dependem do Gate 0. T7 só faz sentido com peças no ledger.
