---
name: analise-semanal
description: Análise editorial semanal sobre o ledger (últimos 30 dias) usando SOMENTE as seis métricas do conector. Termina, sempre, em 5 ângulos para dobrar a aposta e 3 coisas para parar de postar.
---

# Análise semanal

## Trava anti-fabricação (inviolável)

"Só reporte métricas que o conector retornar. Se um dado não estiver disponível, escreva INDISPONIVEL. NUNCA estime, infira ou complete. É proibido reportar: impressions, profile visits, follower conversion, follows por peça, watch time, demografia, melhores horários — esses dados não existem nesta integração."

Métricas permitidas (as únicas): `views · reach · likes · comments · shares · saves`.
Métrica-norte: **sends/reach** (= shares/reach). Likes é o sinal mais fraco — nunca conclua por likes sozinho.

## Entrada

`metricas.csv` + `publicados.csv` + `briefs.csv` das peças dos últimos 30 dias. Linhas com `origem_dado=indisponivel` ficam FORA das comparações (aparecem apenas como lacuna reportada).

## Processo

1. Monte a base peça×janela com as seis métricas permitidas + `sends_por_reach`.
2. Quebre por: tipo de hook, formato, tema/pilar e nº de slides.
3. **Compare apenas dentro do mesmo formato E da mesma faixa de reach** (faixas = quartis do período). Comparar carrossel com reel, ou peça de reach 300 com peça de reach 5.000, gera conclusão causal falsa — proibido.
4. Padrão só existe com ≥2 ocorrências. Uma peça boa é anedota, não padrão.
5. Se um padrão se sustentar por 2 semanas seguidas, proponha (não escreva) uma entrada para `PADROES.md` — quem aprova é o Vitor.

## Saída (estrutura obrigatória)

1. Resumo do período (nº de peças; lacunas de dado com `INDISPONIVEL` explícito onde faltar).
2. Quebras (hook, formato, tema, slides) — números reais do ledger, sem estimativa.
3. Hipóteses tocadas (`hipoteses.csv`): o que os dados desta semana dizem sobre cada uma.
4. **5 ângulos para dobrar a aposta** — cada um com evidência (ids + métricas).
5. **3 coisas para parar de postar** — cada uma com evidência (ids + métricas).

A saída termina SEMPRE nas seções 4 e 5: 5 ângulos para dobrar a aposta e 3 coisas para parar de postar. Sem recomendação vaga: cada item aponta ids de peças.
