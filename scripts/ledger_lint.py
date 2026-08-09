#!/usr/bin/env python3
"""ledger_lint.py — valida o metricas.csv do Content OS.

Uso:
    python3 ledger_lint.py [caminho/do/metricas.csv]

Sem argumento: valida ledger/csv/metricas.csv (relativo à raiz do projeto).
Exit 0 = válido · Exit 1 = inválido (relatório no stdout).

Checa (HANDOFF §5.6):
  - cabeçalho exato do schema — nenhuma coluna de métrica proibida;
  - origem_dado ∈ {conector, app, indisponivel};
  - janela ∈ {72h, 7d};
  - valores de métrica: número ≥ 0 ou o literal INDISPONIVEL (nunca estimativa).
"""

import csv
import math
import sys
from pathlib import Path

COLUNAS = ["id_peca", "janela", "data_coleta", "origem_dado",
           "views", "reach", "saves", "shares", "comments", "sends_por_reach"]
COLS_METRICA = ["views", "reach", "saves", "shares", "comments", "sends_por_reach"]
ORIGENS = {"conector", "app", "indisponivel"}
JANELAS = {"72h", "7d"}
LITERAL_FALTA = "INDISPONIVEL"

# Métricas que NÃO existem na integração (HANDOFF §3.2) — coluna com esses nomes é fabricação.
PROIBIDAS = {"impressions", "impression", "video_views", "plays", "profile_views",
             "profile_visits", "follower_conversion", "follows", "follower",
             "watch_time", "avg_watch_time", "skip_rate", "retention", "retencao",
             "demografia", "demographics", "best_time", "melhores_horarios"}


def main() -> int:
    caminho = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        Path(__file__).resolve().parent.parent / "ledger" / "csv" / "metricas.csv")
    if not caminho.exists():
        print(f"ERRO: arquivo não encontrado: {caminho}")
        return 1

    erros = []
    # utf-8-sig: Excel/Sheets exportam "CSV UTF-8" com BOM; sem isso a 1ª coluna vira '﻿id_peca'
    with open(caminho, newline="", encoding="utf-8-sig") as f:
        leitor = csv.reader(f)
        try:
            cabecalho = [c.strip() for c in next(leitor)]
        except StopIteration:
            print(f"LEDGER LINT: REPROVADO — {caminho} está vazio (nem cabeçalho).")
            return 1

        for c in cabecalho:
            if c.lower() in PROIBIDAS:
                erros.append(f"cabeçalho: coluna PROIBIDA '{c}' — métrica que não existe "
                             f"nesta integração (fabricação). Remova a coluna.")
        if cabecalho != COLUNAS:
            erros.append("cabeçalho: esperado exatamente\n"
                         f"      {','.join(COLUNAS)}\n    encontrado\n"
                         f"      {','.join(cabecalho)}")

        indice = {c: i for i, c in enumerate(cabecalho)}

        def campo(linha, col):
            i = indice.get(col)
            return linha[i].strip() if i is not None and i < len(linha) else ""

        for n, linha in enumerate(leitor, start=2):
            if not any(v.strip() for v in linha):
                continue  # linha em branco
            if not campo(linha, "id_peca"):
                erros.append(f"linha {n}: id_peca vazio")
            if campo(linha, "janela") not in JANELAS:
                erros.append(f"linha {n}: janela '{campo(linha, 'janela')}' fora do domínio "
                             f"{sorted(JANELAS)}")
            if campo(linha, "origem_dado") not in ORIGENS:
                erros.append(f"linha {n}: origem_dado '{campo(linha, 'origem_dado')}' fora do "
                             f"domínio {sorted(ORIGENS)} — estimativa não tem origem válida")
            for col in COLS_METRICA:
                if col not in indice:
                    continue
                v = campo(linha, col)
                if v == LITERAL_FALTA:
                    continue
                try:
                    x = float(v)
                    if not math.isfinite(x):
                        erros.append(f"linha {n}: {col}='{v}' não é valor finito — "
                                     f"nan/inf não é métrica real")
                    elif x < 0:
                        erros.append(f"linha {n}: {col}='{v}' negativo")
                except ValueError:
                    erros.append(f"linha {n}: {col}='{v}' não é número nem o literal "
                                 f"{LITERAL_FALTA} — faixa/texto/estimativa é proibido")

    if erros:
        print(f"LEDGER LINT: REPROVADO — {caminho}")
        for e in erros:
            print(f"  - {e}")
        return 1
    print(f"LEDGER LINT: OK — {caminho}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
