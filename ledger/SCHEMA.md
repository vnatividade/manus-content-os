# SCHEMA.md — ledger editorial (fonte de verdade fora do Manus)

O Manus não tem write-back na knowledge base: sem este ledger externo não há loop de
aprendizado — há repetição. O Instagram Insights retém ±90 dias; o ledger é o snapshot
que sobrevive. Formato: 6 CSVs (uma aba cada no Google Sheets). Cabeçalho é contrato:
`scripts/ledger_lint.py` valida `metricas.csv`; não renomeie nem acrescente coluna sem
mudar o lint junto.

## ideias.csv

`id,data_captura,insumo_bruto,origem,pilar,score_so_eu,score_evidencia,score_tensao,score_utilidade,score_total,status`

- `id`: `i001`, `i002`, … · `origem` ∈ {telegram, whatsapp, conversa, nota}
- scores: 0–5 (skill score-editorial); `score_total` = soma (0–20)
- `status` ∈ {capturada, selecionada, descartada, brief, publicada}

## briefs.csv

`id_brief,id_ideia,pilar,formato,angulo,hook,n_slides,cta,estrutura,data`

- `id_brief`: `b001`, … · `id_ideia` obrigatório (rastreabilidade: sem insumo não há peça)
- `formato` ∈ {carrossel, reel} na POC · `n_slides`: 2–10 (carrossel) ou vazio (reel)

## publicados.csv

`id_peca,id_brief,data,hora,formato,n_slides,hook_tipo,cta,primeira_pessoa,historia_pessoal,framework,permalink,creditos,reescrita,n_intervencoes,tempo_humano_min`

- `id_peca`: `p001`, … · `primeira_pessoa`/`historia_pessoal`/`reescrita` ∈ {0,1}
- `hook_tipo` ∈ {pergunta, dado, contraste, historia, afirmacao} (taxonomia inicial, ajustável)
- `creditos`: custo da geração em créditos Manus · `tempo_humano_min`: minutos do Vitor na peça

## metricas.csv

`id_peca,janela,data_coleta,origem_dado,views,reach,saves,shares,comments,sends_por_reach`

- `janela` ∈ {72h, 7d} — coletar SEMPRE nas duas janelas (Insights morre em ±90 dias)
- `origem_dado` ∈ {conector, app, indisponivel} — TODA métrica declara de onde veio
- valores: número ≥0 ou o literal `INDISPONIVEL` (nunca estimativa, nunca faixa)
- `sends_por_reach` = shares/reach (4 decimais); `INDISPONIVEL` se shares ou reach faltarem
- Nota: o cabeçalho segue o handoff (§5.5) à letra — `likes` (o sinal mais fraco, §3.7)
  fica fora deste CSV, embora seja uma das seis métricas do conector.
- PROIBIDO criar coluna de métrica fora das seis do conector — impressions, video_views,
  plays, profile_views, follower_conversion, follows, watch_time, avg_watch_time,
  skip_rate, retenção por segundo, demografia, "melhor horário": esses dados não existem
  nesta integração (deprecados ou inexistentes por peça). `ledger_lint.py` reprova.

## hipoteses.csv

`id_hip,data,variavel_editorial,hipotese,previsao,pecas_teste,status,evidencia`

- `id_hip`: `h001`, … · `status` ∈ {aberta, validada, refutada}
- `pecas_teste`: ids de peça separados por `;`

## aprendizados.csv

`data,aprendizado,evidencia_ids,acao_no_sistema`

- Só entra aprendizado com evidência (ids de peças/hipóteses)
- `acao_no_sistema` = o que mudou por causa dele (VOZ/FORMATOS/skill/…)
