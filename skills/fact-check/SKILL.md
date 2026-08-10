---
name: fact-check
description: "Verifica toda afirmação factual, número e citação de uma peça antes do Gate 2. Sem link verificável, o item bloqueia a peça. Meta da POC — erro factual publicado = 0."
---

# Fact-check

## Regra única

Nenhum número, citação ou afirmação factual sem link verificável. A sua memória não é fonte. Estimativa não é fonte. "É sabido que" não é fonte.

## Processo

1. Extraia da peça TODAS as afirmações verificáveis (números, datas, citações, "estudo mostra", comparações).
2. Para cada uma, busque a fonte primária (ou a melhor disponível) e verifique se ela sustenta a afirmação COMO ESCRITA — inclusive a magnitude.
3. Experiência pessoal do Vitor não se verifica na web: confira apenas se rastreia ao insumo (`id_ideia`); se não rastrear, é invenção → bloqueia.

## Saída (tabela, nada além)

| afirmação | fonte (link) | status |

com status ∈ `VERIFICADO` · `IMPRECISO (corrigir para: …)` · `NAO-VERIFICADO`.

Última linha, obrigatória:

- `LIBERADO PARA GATE 2` — só se TODOS os itens forem VERIFICADO.
- `BLOQUEADO: <n> itens` — se houver qualquer IMPRECISO ou NAO-VERIFICADO. Item sem fonte sai da peça ou derruba a peça; nunca segue "por conta".
