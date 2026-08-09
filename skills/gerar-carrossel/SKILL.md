---
name: gerar-carrossel
description: Gera UM carrossel a partir de UMA linha de briefs.csv aprovada no Gate 1. Produz texto slide a slide + caption + alt text, dentro dos limites da API. Nunca publica.
---

# Gerar carrossel

## Pré-condições (pare se qualquer uma falhar)

1. Releia `VOZ.md` e `REGRAS-DURAS.md` AGORA — nunca use versão em cache. Se as seções essenciais de `VOZ.md` ainda tiverem TODO-VITOR, pare e reporte: sem voz não há copy.
2. A entrada é UMA linha de `briefs.csv` com `id_brief` e `id_ideia` válidos. Sem `id_ideia` rastreável a insumo real do Vitor, não há peça.
3. Uma task = um carrossel. Nunca gere lote.

## Limites técnicos (de FORMATOS.md)

2–10 slides · JPEG ≤8MB · aspect 4:5 a 1.91:1 · alt text por imagem · sem sticker de link/enquete · sem filtro.

## Estrutura da saída

1. **Rastreio** — primeira linha da resposta: `id_brief=… id_ideia=…`.
2. **Slides** — a quantidade `n_slides` do brief; slide 1 = o hook do brief (não reescreva o hook sem avisar); um argumento por slide; último slide = fechamento. CTA só se o brief pedir — CTA forçado é critério de rejeição do anti-generico.
3. **Caption** — abre com a tese, sem muleta de engajamento ("salva esse post", "comenta aqui"). Sem hashtag inventada. <!-- TODO-VITOR: política de hashtags (usa? quais? quantas?) -->
4. **Alt text por slide** — descritivo, uma linha por imagem.

## Depois de gerar

Submeta o texto à skill `anti-generico` (task separada — atomicidade). Só depois de `APROVADO` a peça vai ao Gate 2 (aprovação do Vitor). Esta skill NUNCA publica nem agenda.
