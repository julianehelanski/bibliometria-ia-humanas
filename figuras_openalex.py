# -*- coding: utf-8 -*-
"""Gera as figuras da análise OpenAlex (IA nas Humanidades, internacional).

Paralelo a figuras_capes_2021_2024.py e figuras_scielo_articlemeta.py —
mesmo padrão visual (utils.aplicar_estilo_padrao) e mesma nomenclatura de
subcampos.

Pré-requisito: rodar antes
    python analise_openalex.py --modo agregado --mailto SEU_EMAIL      (global + BR)
    python analise_openalex.py --modo agregado --pais BR --mailto ...  (por ano BR)
    python analise_openalex.py --modo corpus  --pais BR --mailto ...   (subcampos)

Figuras geradas em figuras/:
    openalex_01_ranking_paises.png     — top países por volume (Brasil em destaque)
    openalex_02_taxa_interna_paises.png — taxa interna por país (marginalidade BR)
    openalex_03_brasil_temporal.png    — evolução anual do Brasil + taxa interna
    openalex_04_subcampos_3bases.png   — subcampos comparados: CAPES × SciELO × OpenAlex

Uso:
    python figuras_openalex.py
"""

from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from utils import (
    CORES_INTERMEDIARIAS,
    FIGURAS_DIR,
    aplicar_estilo_padrao,
    garantir_diretorio,
)

aplicar_estilo_padrao()

# Caminhos. Módulo-level para permitir override em teste.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_OPENALEX_DIR = os.path.join(BASE_DIR, "dados_openalex")

COR_BRASIL = CORES_INTERMEDIARIAS[0]   # vermelho-muted (Brasil em destaque)
COR_DEST = CORES_INTERMEDIARIAS[3]     # azul (1º lugar)
COR_NEUTRA = CORES_INTERMEDIARIAS[9]   # cinza-azulado (demais)

# Subcampos canônicos das outras bases (decisoes_metodologicas.md I.5 e II.5),
# em % do respectivo corpus IA. OpenAlex é lido do resumo_BR.csv em tempo real.
SUB_ORDER = ["IA stricto", "ML", "DL", "LLM", "Correlatos"]
CAPES_SUB = {"IA stricto": 29.40, "ML": 40.66, "DL": 33.29, "LLM": 3.89, "Correlatos": 38.26}
SCIELO_SUB = {"IA stricto": 29.64, "ML": 21.87, "DL": 25.04, "LLM": 7.13, "Correlatos": 22.19}
SUB_MAP = {
    "SUBCAMPO_IA_STRICTO": "IA stricto",
    "SUBCAMPO_ML": "ML",
    "SUBCAMPO_DL": "DL",
    "SUBCAMPO_LLM": "LLM",
    "SUBCAMPO_CORRELATOS": "Correlatos",
}


def _salvar(fig, nome: str) -> None:
    out = os.path.join(garantir_diretorio(FIGURAS_DIR), nome)
    fig.tight_layout()
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  -> {out}")


def _ler_csv(nome: str) -> pd.DataFrame | None:
    caminho = os.path.join(DADOS_OPENALEX_DIR, nome)
    if not os.path.isfile(caminho):
        sys.stderr.write(f"[pulando] não encontrei {caminho} — rode analise_openalex.py antes.\n")
        return None
    return pd.read_csv(caminho)


def _cores(rotulos, destaque="Brazil", topo_idx=0):
    """Cinza para todos; vermelho no Brasil; azul no 1º colocado."""
    cores = []
    for i, r in enumerate(rotulos):
        if isinstance(r, str) and ("brazil" in r.lower() or "brasil" in r.lower()):
            cores.append(COR_BRASIL)
        elif i == topo_idx:
            cores.append(COR_DEST)
        else:
            cores.append(COR_NEUTRA)
    return cores


def fig_ranking_paises(top: int = 15) -> None:
    """openalex_01 — top países por volume de IA-Humanas (conceito), Brasil destacado."""
    df = _ler_csv("openalex_ia_humanas_por_pais_global.csv")
    if df is None:
        return
    df = df[df["pais_codigo"].astype(str).str.strip() != ""].copy()
    df = df.sort_values("count_ia_hum", ascending=False).head(top).iloc[::-1]

    fig, ax = plt.subplots(figsize=(10, 6))
    cores = _cores(df["pais"].tolist(), topo_idx=len(df) - 1)  # topo está no fim (iloc invertido)
    ax.barh(df["pais"].astype(str), df["count_ia_hum"], color=cores)
    for y, v in enumerate(df["count_ia_hum"]):
        ax.text(v, y, f" {int(v):,}".replace(",", "."), va="center", fontsize=8)
    ax.set_xlabel("Publicações de IA nas Humanidades (2016–2024)")
    ax.set_title(f"Top {top} países — IA nas Humanidades (OpenAlex; definição conceito)")
    ax.margins(x=0.12)
    _salvar(fig, "openalex_01_ranking_paises.png")


def fig_taxa_interna_paises(top: int = 15) -> None:
    """openalex_02 — taxa interna por país; evidencia a marginalidade do Brasil."""
    df = _ler_csv("openalex_ia_humanas_por_pais_global.csv")
    if df is None:
        return
    df = df[df["pais_codigo"].astype(str).str.strip() != ""].copy()
    # Top por volume (mesmos países da fig 1), ordenados por taxa para leitura.
    df = df.sort_values("count_ia_hum", ascending=False).head(top)
    df = df.sort_values("taxa_interna_%", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    cores = _cores(df["pais"].tolist(), topo_idx=-1)
    ax.barh(df["pais"].astype(str), df["taxa_interna_%"], color=cores)
    for y, v in enumerate(df["taxa_interna_%"]):
        ax.text(v, y, f" {v:.1f}%", va="center", fontsize=8)
    ax.set_xlabel("Taxa interna: % das Humanidades do país que tocam IA")
    ax.set_title(f"Penetração da IA nas Humanidades — top {top} produtores")
    ax.margins(x=0.12)
    _salvar(fig, "openalex_02_taxa_interna_paises.png")


def fig_brasil_temporal() -> None:
    """openalex_03 — evolução anual do Brasil: volume (barras) + taxa interna (linha)."""
    df = _ler_csv("openalex_ia_humanas_por_ano_BR.csv")
    if df is None:
        return
    df = df.sort_values("ano")

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.bar(df["ano"].astype(int).astype(str), df["count_ia_hum"], color=COR_DEST, label="Volume")
    ax1.set_ylabel("Publicações de IA nas Humanidades", color=COR_DEST)
    ax1.tick_params(axis="y", labelcolor=COR_DEST)
    for x, v in enumerate(df["count_ia_hum"]):
        ax1.text(x, v, f"{int(v):,}".replace(",", "."), ha="center", va="bottom", fontsize=8)

    ax2 = ax1.twinx()
    ax2.plot(df["ano"].astype(int).astype(str), df["taxa_interna_%"],
             color=COR_BRASIL, marker="o", linewidth=2, label="Taxa interna")
    ax2.set_ylabel("Taxa interna (%)", color=COR_BRASIL)
    ax2.tick_params(axis="y", labelcolor=COR_BRASIL)
    ax2.grid(False)

    ax1.set_title("Brasil — IA nas Humanidades por ano (OpenAlex)\n"
                  "Atenção: 2024 provavelmente subestimado por indexação incompleta")
    _salvar(fig, "openalex_03_brasil_temporal.png")


def fig_subcampos_3bases() -> None:
    """openalex_04 — subcampos comparados entre CAPES, SciELO e OpenAlex (% do corpus IA)."""
    df = _ler_csv("openalex_ia_humanas_resumo_BR.csv")
    if df is None:
        return
    foco = df[df["tipo"] == "FOCO_IA"]
    n_ia = int(foco[foco["categoria"] != "Outros Temas"]["obras_unicas"].sum())
    if n_ia == 0:
        sys.stderr.write("[pulando subcampos] nenhum trabalho que toca IA no resumo.\n")
        return
    sub = df[df["tipo"] == "SUBCAMPO"].set_index("categoria")["obras_unicas"]
    openalex_sub = {SUB_MAP[k]: 100 * v / n_ia for k, v in sub.items() if k in SUB_MAP}

    bases = {
        "CAPES (corpus IA total)": CAPES_SUB,
        "SciELO (corpus IA total)": SCIELO_SUB,
        "OpenAlex (Brasil, Humanas)": openalex_sub,
    }
    x = np.arange(len(SUB_ORDER))
    largura = 0.26

    fig, ax = plt.subplots(figsize=(11, 6))
    for i, (nome, dados) in enumerate(bases.items()):
        valores = [dados.get(s, 0) for s in SUB_ORDER]
        ax.bar(x + (i - 1) * largura, valores, largura, label=nome,
               color=CORES_INTERMEDIARIAS[[2, 3, 0][i]])
    ax.set_xticks(x)
    ax.set_xticklabels(SUB_ORDER)
    ax.set_ylabel("% do corpus de IA da base (multi-label)")
    ax.set_title("Subcampos de IA — comparação entre as três bases")
    ax.legend(fontsize=8)
    _salvar(fig, "openalex_04_subcampos_3bases.png")


def main() -> None:
    print("Gerando figuras OpenAlex em figuras/ ...")
    fig_ranking_paises()
    fig_taxa_interna_paises()
    fig_brasil_temporal()
    fig_subcampos_3bases()
    print("Concluído.")


if __name__ == "__main__":
    main()
