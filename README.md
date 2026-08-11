# Content OS de Instagram (sobre Manus)

Transforma ideias reais do Vitor em conteúdo com qualidade editorial e usa performance
real (ledger externo) para melhorar o sistema. O Manus executa; a memória vive fora dele.
Fonte de verdade do desenho: `HANDOFF-manus-content-os.md` (cópia neste diretório).

## Ordem de operação

1. **Dia 0** — siga `CHECK-DIA-0.md` (o conector existe? conta profissional? Gate 0).
2. **Preencha o que é seu** — `project/VOZ.md`, `project/PILARES.md` e os demais
   `TODO-VITOR` (`grep -rn "TODO-VITOR" .` lista todos). Sem voz e pilares, o pipeline
   se recusa a gerar copy — por desenho.
3. **Monte o Manus Project** — instrução mestra = `project/PROJECT-INSTRUCTION.md`;
   knowledge base = os outros 5 arquivos de `project/`; importe as 5 skills de `skills/`.
4. **Ledger** — planilha no Google Sheets com 6 abas, cabeçalhos exatos de `ledger/csv/`
   (contrato documentado em `ledger/SCHEMA.md`).
5. **POC** — 4 semanas, 12 peças, gates e critérios GO/ADJUST/STOP em `PLANO-POC.md`.

## O loop semanal (resumo)

capturar → pontuar (score-editorial) → **Gate 1: você escolhe 3** → brief → gerar
(gerar-carrossel) → anti-generico + fact-check → **Gate 2: você aprova a cópia** →
**Gate 3: publicar** → coletar métricas 72h/7d no ledger → analise-semanal.

## Scripts de integridade

- `python3 scripts/ledger_lint.py ledger/csv/metricas.csv` — valida o conteúdo de
  metricas.csv (domínios, `INDISPONIVEL`, nenhuma métrica proibida). Exit 0 = ok.
- `python3 scripts/ledger_check.py ledger/csv` — integridade das 6 abas: referências,
  ids duplicados, `sends_por_reach` coerente, lacuna de coleta. É o smoke do pipeline
  automatizado — rode a cada ciclo.
- `python3 scripts/gate0_diff.py --manus manus.csv --app app.csv` — Gate 0: o Manus fala
  a verdade? Exit 1 = divergência ou métrica fabricada.

## Automação

`AUTOMACAO.md` — as 7 Scheduled Tasks do pipeline, o smoke de cada uma (validação em
horas), o controle negativo do crítico e as 4 ondas. Leia antes de ligar qualquer
automação.

## Regras que não se negociam

- Só existem SEIS métricas: views, reach, likes, comments, shares, saves. Faltou dado →
  `INDISPONIVEL`, nunca estimativa. Métrica-norte: sends/reach.
- Uma task Manus = uma etapa (agendar = 1 Scheduled Task por etapa; não há fila de rascunhos).
- Gates 1 e 2 (seleção e cópia) são humanos para sempre; o Gate 3 começa manual e só
  automatiza com erro zero (`PLANO-POC.md`).
- Detalhe completo: `project/REGRAS-DURAS.md`.

## Se o conector falhar

`FALLBACK-PUBLICACAO.md` — caminho B via Publora (documentado, NÃO instalado).

## Pós-POC

`PONTE-AURASITE.md` — mapa verificado de convergência com o motor v3 do AuraSite
(levar o Content OS para lá, ou usar a ingestão/captura do Aura aqui). Decisão do Vitor.
