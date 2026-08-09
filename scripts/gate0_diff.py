#!/usr/bin/env python3
"""gate0_diff.py — executor do Gate 0 (HANDOFF §6).

Compara as métricas que o Manus reportou com as lidas no app do Instagram,
por id_peca × métrica.

Uso:
    python3 gate0_diff.py --manus manus.csv --app app.csv [--tolerancia 0.05]

Formatos aceitos (detectados pelo cabeçalho):
  longo: id_peca,metrica,valor
  largo: id_peca,<met1>,<met2>,...  (colunas além de id_peca/janela/data_coleta/origem_dado)

Exit 1 se:
  - o arquivo do Manus contiver métrica fora das seis permitidas (fabricação — pior cenário);
  - houver divergência relativa acima da tolerância em qualquer id_peca × métrica.
Exit 0 caso contrário. Avisos (dado só de um lado, INDISPONIVEL) não reprovam.
"""

import argparse
import csv
import math
import sys

PERMITIDAS = {"views", "reach", "likes", "comments", "shares", "saves"}
META_COLS = {"id_peca", "janela", "data_coleta", "origem_dado"}
LITERAL_FALTA = "INDISPONIVEL"


def carregar(caminho):
    """Devolve (dados, fabricadas): dados[(id_peca, metrica)] = valor_str;
    fabricadas = [(onde, metrica)] fora das seis permitidas."""
    dados, fabricadas = {}, []
    # utf-8-sig: Excel/Sheets exportam "CSV UTF-8" com BOM; sem isso a 1ª coluna vira '﻿id_peca'
    # e todas as linhas seriam puladas em silêncio — inclusive as com métrica fabricada
    with open(caminho, newline="", encoding="utf-8-sig") as f:
        leitor = csv.DictReader(f)
        cols = [c.strip() for c in (leitor.fieldnames or [])]
        formato_longo = "metrica" in cols and "valor" in cols
        if formato_longo:
            for n, linha in enumerate(leitor, start=2):
                idp = (linha.get("id_peca") or "").strip()
                met = (linha.get("metrica") or "").strip().lower()
                val = (linha.get("valor") or "").strip()
                if not idp or not met:
                    continue
                if met not in PERMITIDAS:
                    fabricadas.append((f"linha {n}", met))
                    continue
                dados[(idp, met)] = val
        else:
            cols_metrica = [c for c in cols if c not in META_COLS]
            for c in cols_metrica:
                if c.lower() not in PERMITIDAS:
                    fabricadas.append(("cabeçalho", c))
            for linha in leitor:
                idp = (linha.get("id_peca") or "").strip()
                if not idp:
                    continue
                for c in cols_metrica:
                    if c.lower() in PERMITIDAS:
                        dados[(idp, c.lower())] = (linha.get(c) or "").strip()
    return dados, fabricadas


def main() -> int:
    ap = argparse.ArgumentParser(description="Gate 0: Manus × app do Instagram")
    ap.add_argument("--manus", required=True, help="CSV exportado da resposta do Manus")
    ap.add_argument("--app", required=True, help="CSV com a leitura manual no app do Instagram")
    ap.add_argument("--tolerancia", type=float, default=0.05,
                    help="divergência relativa tolerada (padrão 0.05 = 5%%)")
    args = ap.parse_args()

    manus, fabricadas = carregar(args.manus)
    app, _ = carregar(args.app)  # métrica desconhecida no app = leitura irrelevante, não fabricação

    divergencias, avisos = [], []
    for chave in sorted(set(manus) | set(app)):
        idp, met = chave
        vm, va = manus.get(chave), app.get(chave)
        if vm is None:
            avisos.append(f"{idp}×{met}: só no app (o conector não retornou?)")
            continue
        if va is None:
            avisos.append(f"{idp}×{met}: só no Manus (sem leitura do app para conferir)")
            continue
        if LITERAL_FALTA in (vm, va):
            avisos.append(f"{idp}×{met}: {LITERAL_FALTA} declarado — sem comparação")
            continue
        try:
            fm, fa = float(vm), float(va)
        except ValueError:
            divergencias.append((idp, met, vm, va, "valor não numérico"))
            continue
        if not (math.isfinite(fm) and math.isfinite(fa)):
            divergencias.append((idp, met, vm, va, "valor não finito (nan/inf)"))
            continue
        delta = abs(fm - fa) / max(abs(fa), 1.0)
        if delta > args.tolerancia:
            divergencias.append((idp, met, vm, va, f"delta {delta:.1%}"))

    if fabricadas:
        print("MÉTRICA FABRICADA no arquivo do Manus — fora das seis permitidas (§3.6, pior cenário):")
        for onde, met in fabricadas:
            print(f"  - {onde}: '{met}' não existe nesta integração")
    if divergencias:
        print(f"Divergências acima da tolerância ({args.tolerancia:.0%}):")
        print(f"  {'id_peca':<10}{'métrica':<12}{'manus':>10}{'app':>10}  obs")
        for idp, met, vm, va, obs in divergencias:
            print(f"  {idp:<10}{met:<12}{vm:>10}{va:>10}  {obs}")
    for a in avisos:
        print(f"  aviso: {a}")

    comparadas = len(set(manus) & set(app))
    if fabricadas:
        print("GATE 0: REPROVADO — o Manus reportou métrica que a integração não expõe. "
              "Reforce a trava anti-fabricação na instrução mestra e reteste.")
        return 1
    if divergencias:
        print("GATE 0: REPROVADO — números do Manus divergem do app. Coleta manual durante "
              "toda a POC; o conector vira só publicador.")
        return 1
    if comparadas == 0:
        print("GATE 0: REPROVADO — nenhum par id_peca×métrica comparável (arquivo vazio, "
              "cabeçalho errado ou lados sem interseção). Sem evidência não há aprovação.")
        return 1
    print(f"GATE 0: APROVADO — {comparadas} pares id_peca×métrica dentro da tolerância. "
          "O ledger pode confiar no conector.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
