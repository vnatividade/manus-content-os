#!/usr/bin/env python3
"""ledger_check.py — integridade do ledger inteiro (as 6 abas).

Uso:
    python3 ledger_check.py [diretorio_com_os_csvs]

Sem argumento: valida ledger/csv/ (relativo à raiz do projeto).
Exit 0 = íntegro · Exit 1 = quebrado (relatório no stdout).
Avisos (lacunas de coleta) NÃO afetam o exit code.

Complementa `ledger_lint.py`, que valida só o conteúdo de metricas.csv.
Este script é o smoke test do pipeline AUTOMATIZADO: quando as tasks do Manus
escrevem linhas sozinhas, o defeito típico não é valor errado — é referência
quebrada, id duplicado, coluna a mais ou etapa pulada em silêncio (§3.5 do
handoff: falhas silenciosas, pula fonte sem avisar). Roda em segundos, então
cabe no combinado de validar funcionamento em horas, não em dias.
"""

import csv
import math
import sys
from pathlib import Path

from ledger_lint import PROIBIDAS, ORIGENS, JANELAS, LITERAL_FALTA

COLUNAS = {
    "ideias": ["id", "data_captura", "insumo_bruto", "origem", "pilar",
               "score_so_eu", "score_evidencia", "score_tensao", "score_utilidade",
               "score_total", "status"],
    "briefs": ["id_brief", "id_ideia", "pilar", "formato", "angulo", "hook",
               "n_slides", "cta", "estrutura", "data"],
    "publicados": ["id_peca", "id_brief", "data", "hora", "formato", "n_slides",
                   "hook_tipo", "cta", "primeira_pessoa", "historia_pessoal",
                   "framework", "permalink", "creditos", "reescrita",
                   "n_intervencoes", "tempo_humano_min"],
    "metricas": ["id_peca", "janela", "data_coleta", "origem_dado", "views",
                 "reach", "saves", "shares", "comments", "sends_por_reach"],
    "hipoteses": ["id_hip", "data", "variavel_editorial", "hipotese", "previsao",
                  "pecas_teste", "status", "evidencia"],
    "aprendizados": ["data", "aprendizado", "evidencia_ids", "acao_no_sistema"],
}

ORIGEM_IDEIA = {"telegram", "whatsapp", "conversa", "nota"}
STATUS_IDEIA = {"capturada", "selecionada", "descartada", "brief", "publicada"}
STATUS_HIP = {"aberta", "validada", "refutada"}
FORMATOS = {"carrossel", "reel", "post"}
BINARIOS = ["primeira_pessoa", "historia_pessoal", "reescrita"]


def ler(caminho):
    """Devolve lista de dicts (linhas não-vazias) + o cabeçalho lido."""
    if not caminho.exists():
        return None, None
    # utf-8-sig: Sheets/Excel exportam "CSV UTF-8" com BOM
    with open(caminho, newline="", encoding="utf-8-sig") as f:
        leitor = csv.reader(f)
        try:
            cabecalho = [c.strip() for c in next(leitor)]
        except StopIteration:
            return [], []
        linhas = []
        for n, bruta in enumerate(leitor, start=2):
            if not any(v.strip() for v in bruta):
                continue
            linha = {c: (bruta[i].strip() if i < len(bruta) else "")
                     for i, c in enumerate(cabecalho)}
            linha["__n"] = n
            linhas.append(linha)
        return linhas, cabecalho


def ids_de(campo):
    """Quebra um campo multi-id (`p001;p002`) na lista de ids."""
    return [x.strip() for x in campo.replace(",", ";").split(";") if x.strip()]


def main() -> int:
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        Path(__file__).resolve().parent.parent / "ledger" / "csv")
    erros, avisos = [], []
    dados = {}

    for nome, colunas in COLUNAS.items():
        caminho = base / f"{nome}.csv"
        linhas, cabecalho = ler(caminho)
        if linhas is None:
            erros.append(f"{nome}.csv: arquivo não encontrado em {base}")
            dados[nome] = []
            continue
        dados[nome] = linhas
        for c in cabecalho:
            if c.lower() in PROIBIDAS:
                erros.append(f"{nome}.csv cabeçalho: coluna PROIBIDA '{c}' — métrica "
                             f"que não existe nesta integração (fabricação)")
        if cabecalho != colunas:
            erros.append(f"{nome}.csv cabeçalho fora do contrato:\n"
                         f"      esperado {','.join(colunas)}\n"
                         f"      lido     {','.join(cabecalho)}")

    # ---- unicidade de identificadores
    for nome, chave in [("ideias", "id"), ("briefs", "id_brief"),
                        ("publicados", "id_peca"), ("hipoteses", "id_hip")]:
        vistos = {}
        for linha in dados[nome]:
            v = linha.get(chave, "")
            if not v:
                erros.append(f"{nome}.csv linha {linha['__n']}: {chave} vazio")
            elif v in vistos:
                erros.append(f"{nome}.csv linha {linha['__n']}: {chave} '{v}' duplicado "
                             f"(já na linha {vistos[v]})")
            else:
                vistos[v] = linha["__n"]

    ids_ideia = {l.get("id") for l in dados["ideias"]}
    ids_brief = {l.get("id_brief") for l in dados["briefs"]}
    ids_peca = {l.get("id_peca") for l in dados["publicados"]}
    ids_hip = {l.get("id_hip") for l in dados["hipoteses"]}

    # ---- ideias: domínios e soma dos scores
    for l in dados["ideias"]:
        n = l["__n"]
        if l.get("origem") not in ORIGEM_IDEIA:
            erros.append(f"ideias.csv linha {n}: origem '{l.get('origem')}' fora de "
                         f"{sorted(ORIGEM_IDEIA)}")
        if l.get("status") not in STATUS_IDEIA:
            erros.append(f"ideias.csv linha {n}: status '{l.get('status')}' fora de "
                         f"{sorted(STATUS_IDEIA)}")
        eixos = ["score_so_eu", "score_evidencia", "score_tensao", "score_utilidade"]
        valores = []
        for col in eixos:
            try:
                x = int(l.get(col, ""))
                if not 0 <= x <= 5:
                    erros.append(f"ideias.csv linha {n}: {col}={x} fora de 0–5")
                valores.append(x)
            except ValueError:
                erros.append(f"ideias.csv linha {n}: {col}='{l.get(col)}' não é inteiro")
        if len(valores) == 4:
            try:
                total = int(l.get("score_total", ""))
                if total != sum(valores):
                    erros.append(f"ideias.csv linha {n}: score_total={total} ≠ soma dos "
                                 f"eixos ({sum(valores)})")
            except ValueError:
                erros.append(f"ideias.csv linha {n}: score_total='{l.get('score_total')}' "
                             f"não é inteiro")

    # ---- briefs: referência à ideia + formato + n_slides
    for l in dados["briefs"]:
        n = l["__n"]
        alvo = l.get("id_ideia", "")
        if alvo not in ids_ideia:
            erros.append(f"briefs.csv linha {n}: id_ideia '{alvo}' não existe em "
                         f"ideias.csv — sem insumo real não há peça")
        formato = l.get("formato", "")
        if formato not in FORMATOS:
            erros.append(f"briefs.csv linha {n}: formato '{formato}' fora de "
                         f"{sorted(FORMATOS)}")
        slides = l.get("n_slides", "")
        if formato == "carrossel":
            try:
                x = int(slides)
                if not 2 <= x <= 10:
                    erros.append(f"briefs.csv linha {n}: n_slides={x} fora de 2–10 "
                                 f"(limite da API para carrossel)")
            except ValueError:
                erros.append(f"briefs.csv linha {n}: carrossel sem n_slides numérico "
                             f"('{slides}')")
        elif slides:
            erros.append(f"briefs.csv linha {n}: formato '{formato}' não tem slides, "
                         f"mas n_slides='{slides}'")

    # ---- publicados: referência ao brief + binários + formato
    for l in dados["publicados"]:
        n = l["__n"]
        alvo = l.get("id_brief", "")
        if alvo not in ids_brief:
            erros.append(f"publicados.csv linha {n}: id_brief '{alvo}' não existe em "
                         f"briefs.csv")
        if l.get("formato") not in FORMATOS:
            erros.append(f"publicados.csv linha {n}: formato '{l.get('formato')}' fora de "
                         f"{sorted(FORMATOS)}")
        for col in BINARIOS:
            if l.get(col) not in {"0", "1"}:
                erros.append(f"publicados.csv linha {n}: {col}='{l.get(col)}' — use 0 ou 1")

    # ---- metricas: referência à peça, janela única, coerência de sends/reach
    par_visto = {}
    for l in dados["metricas"]:
        n = l["__n"]
        peca = l.get("id_peca", "")
        if peca not in ids_peca:
            erros.append(f"metricas.csv linha {n}: id_peca '{peca}' não existe em "
                         f"publicados.csv")
        janela = l.get("janela", "")
        if janela not in JANELAS:
            erros.append(f"metricas.csv linha {n}: janela '{janela}' fora de "
                         f"{sorted(JANELAS)}")
        if l.get("origem_dado") not in ORIGENS:
            erros.append(f"metricas.csv linha {n}: origem_dado "
                         f"'{l.get('origem_dado')}' fora de {sorted(ORIGENS)}")
        chave = (peca, janela)
        if chave in par_visto:
            erros.append(f"metricas.csv linha {n}: {peca}×{janela} duplicado "
                         f"(já na linha {par_visto[chave]})")
        else:
            par_visto[chave] = n
        shares, reach, declarado = (l.get("shares", ""), l.get("reach", ""),
                                    l.get("sends_por_reach", ""))
        if LITERAL_FALTA not in (shares, reach, declarado):
            try:
                fs, fr, fd = float(shares), float(reach), float(declarado)
                if math.isfinite(fs) and math.isfinite(fr) and math.isfinite(fd) and fr > 0:
                    if abs(fd - fs / fr) > 0.0001:
                        erros.append(f"metricas.csv linha {n}: sends_por_reach={fd} ≠ "
                                     f"shares/reach ({fs / fr:.4f}) — métrica-norte "
                                     f"calculada errado")
            except ValueError:
                pass  # valor não numérico é problema do ledger_lint.py

    # ---- hipoteses e aprendizados: evidência tem que apontar para algo real
    for l in dados["hipoteses"]:
        n = l["__n"]
        if l.get("status") not in STATUS_HIP:
            erros.append(f"hipoteses.csv linha {n}: status '{l.get('status')}' fora de "
                         f"{sorted(STATUS_HIP)}")
        for pid in ids_de(l.get("pecas_teste", "")):
            if pid not in ids_peca:
                erros.append(f"hipoteses.csv linha {n}: pecas_teste aponta '{pid}', "
                             f"que não existe em publicados.csv")
    for l in dados["aprendizados"]:
        n = l["__n"]
        refs = ids_de(l.get("evidencia_ids", ""))
        if not refs:
            erros.append(f"aprendizados.csv linha {n}: sem evidencia_ids — aprendizado "
                         f"sem evidência não entra no ledger")
        for rid in refs:
            if rid not in ids_peca | ids_hip | ids_ideia:
                erros.append(f"aprendizados.csv linha {n}: evidencia_ids aponta '{rid}', "
                             f"que não existe em nenhuma aba")

    # ---- avisos: etapa pulada em silêncio (não reprova, mas é o que o Manus faz)
    for l in dados["publicados"]:
        faltando = [j for j in sorted(JANELAS)
                    if (l.get("id_peca"), j) not in par_visto]
        if faltando:
            avisos.append(f"{l.get('id_peca')}: sem métrica coletada para "
                          f"{', '.join(faltando)}")
    usados_em_brief = {l.get("id_ideia") for l in dados["briefs"]}
    for l in dados["ideias"]:
        if l.get("status") == "brief" and l.get("id") not in usados_em_brief:
            avisos.append(f"{l.get('id')}: status 'brief' mas nenhum brief a referencia")

    print(f"LEDGER CHECK — {base}")
    print(f"  linhas: " + " · ".join(f"{k}={len(v)}" for k, v in dados.items()))
    for a in dict.fromkeys(avisos):  # dedup preservando a ordem
        print(f"  aviso: {a}")
    if erros:
        print(f"REPROVADO — {len(erros)} problema(s) de integridade:")
        for e in erros:
            print(f"  - {e}")
        return 1
    print("APROVADO — ledger íntegro (referências, domínios e unicidade).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
