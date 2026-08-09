# AGENTS.md — manus-content-os

Venture no padrão do `pipe-venture-builder` (manual compartilhado — nunca editar aquele
repo a partir daqui). Fonte de verdade do desenho: `HANDOFF-manus-content-os.md`.
Modo do repo: `.pipe/mode.json` (exploration desde 2026-08-09).

## Gates absolutos (valem em qualquer modo — HANDOFF §4)

- NÃO autorizar OAuth de nada (Instagram, Google, Publora, Manus).
- NÃO publicar, agendar ou enviar conteúdo para o Instagram ou serviço externo.
- NÃO digitar/colar credenciais nem imprimir valores de secret (use o Vaultwarden via `vw`).
- NÃO instalar as skills Publora (`FALLBACK-PUBLICACAO.md` é só documentação).
- NÃO inventar voz, opiniões, histórias, pilares ou identidade visual do Vitor — insumo
  faltando vira `<!-- TODO-VITOR: ... -->`.
- Trava anti-fabricação: só as seis métricas do conector; dado faltando = `INDISPONIVEL`.

## O que exploration cobre aqui

Iterar em docs, skills, scripts e fixtures; commit e push neste repo. Antes de mudar
contrato de CSV, rode `python3 scripts/ledger_lint.py` e mantenha `ledger/SCHEMA.md` e o
lint em sincronia. Gate 0 (`scripts/gate0_diff.py`) é o teste de verdade do conector.

## Pós-POC

`PONTE-AURASITE.md` mapeia a convergência com o motor do AuraSite — decisão do Vitor,
condicionada ao GO/ADJUST/STOP do `PLANO-POC.md`.
