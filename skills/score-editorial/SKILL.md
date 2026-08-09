---
name: score-editorial
description: Pontua um insumo real do Vitor nos 4 eixos do Content OS (só-eu, evidência, tensão, utilidade) e devolve a linha pronta para ideias.csv. Use sempre que chegar insumo novo; nunca rode sem insumo.
---

# Score editorial

## Entrada

Um insumo BRUTO real do Vitor (áudio transcrito, mensagem, nota) + origem (`telegram`, `whatsapp`, `conversa`, `nota`). Sem insumo real, esta skill não roda — é proibido gerar ideia do zero em nome dele.

## Antes de pontuar

Releia `PILARES.md` (nunca use versão em cache). Classifique o insumo em um dos pilares; se não couber em nenhum, marque `fora-de-pilar` (entra no ledger, mas não vira brief na POC).

## Os 4 eixos (0–5 cada)

- **score_so_eu** — só o Vitor poderia publicar isso? 0 = qualquer perfil publicaria · 3 = ângulo dele sobre tema comum · 5 = experiência/dado/posição que só ele tem.
- **score_evidencia** — tem fato verificável por trás? 0 = opinião solta · 3 = caso real dele · 5 = número/fonte verificável + caso real.
- **score_tensao** — contraria senso comum ou expõe trade-off real? 0 = consenso morno · 3 = nuance incômoda · 5 = tese que metade da audiência vai querer contestar.
- **score_utilidade** — o leitor sai com algo aplicável? 0 = desabafo · 3 = princípio aplicável · 5 = passo concreto que dá para usar hoje.

`score_total` = soma dos quatro (0–20).

## Saída (exata, nada além)

1. Linha CSV pronta para `ideias.csv`, no cabeçalho
   `id,data_captura,insumo_bruto,origem,pilar,score_so_eu,score_evidencia,score_tensao,score_utilidade,score_total,status`
   com `status=capturada` e `id` sequencial (`i001`, `i002`, …).
2. Uma linha de justificativa por eixo (máximo 1 frase cada).

Sem ranking, sem sugestão de brief, sem dashboard. A seleção (Gate 1) é do Vitor.

<!-- TODO-VITOR: calibração — cole aqui 3 insumos seus já pontuados por você
     (um alto, um médio, um baixo) para ancorar a régua. Sem isso a régua fica genérica. -->
