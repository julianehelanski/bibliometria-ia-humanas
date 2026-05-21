# -*- coding: utf-8 -*-
"""Gera as três figuras novas que situam a IA nas humanidades dentro do
mapa mais amplo da produção pós-graduada brasileira sobre IA (2021-2024).

Pré-requisito: rodar antes `python analise_capes_2021_2024.py` para gerar
`dados_capes/capes_2021_2024_ia.csv`.

Figuras geradas:
  figuras/capes_11_grande_area_share.png    distribuição IA por grande área
  figuras/capes_12_temporal_grande_area.png evolução 2021-2024 por grande área
  figuras/capes_13_heatmap_area_keyword.png heatmap área × keyword

Uso:
    python figuras_capes_2021_2024.py
"""

from __future__ import annotations

import os
import re
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from utils import (
    CORES_INTERMEDIARIAS,
    DADOS_CAPES_DIR,
    FIGURAS_DIR,
    aplicar_estilo_padrao,
    garantir_diretorio,
)

aplicar_estilo_padrao()
garantir_diretorio(FIGURAS_DIR)

CSV_IA = os.path.join(DADOS_CAPES_DIR, "capes_2021_2024_ia.csv")

# Termos individuais para o heatmap (presença/ausência por registro)
KEYWORDS_HEATMAP = [
    ("inteligência artificial", r"\b(intelig[êe]ncia\s+artificial|artificial\s+intelligence)\b"),
    ("machine/deep learning", r"\b(machine\s+learning|deep\s+learning|aprendizado\s+de\s+m[áa]quina|aprendizado\s+profundo)\b"),
    ("redes neurais", r"\b(redes?\s+neurais|neural\s+networks?)\b"),
    ("LLM / modelo de linguagem", r"\b(llms?|large\s+language\s+models?|modelos?\s+de\s+linguagem|transformer[s]?)\b"),
    ("ChatGPT / GPT-N", r"\b(chatgpt|gpt-\d)\b"),
    ("IA generativa", r"\b(ia\s+generativa|generative\s+ai)\b"),
    ("robótica / automação", r"\b(rob[óo]tica|rob[ôo]s|automa[çc][ãa]o|automation)\b"),
    ("NLP", r"\b(processamento\s+de\s+linguagem\s+natural|natural\s+language\s+processing|nlp)\b"),
    ("big data / mineração", r"\b(big\s+data|minera[çc][ãa]o\s+de\s+dados|data\s+mining)\b"),
    ("visão computacional", r"\b(vis[ãa]o\s+computacional|computer\s+vision)\b"),
]


def carregar_ia() -> pd.DataFrame:
    if not os.path.isfile(CSV_IA):
        sys.exit(f"ERRO: rode antes analise_capes_2021_2024.py — falta {CSV_IA}")
    df = pd.read_csv(CSV_IA, low_memory=False)
    return df


def texto_classificacao(df: pd.DataFrame) -> pd.Series:
    s = df["NM_PRODUCAO"].fillna("").astype(str)
    for c in ["DS_RESUMO", "DS_PALAVRA_CHAVE", "DS_ABSTRACT", "DS_KEYWORD"]:
        if c in df.columns:
            s = s + " | " + df[c].fillna("").astype(str)
    return s


# ---------------------------------------------------------------------------
# Figura 11: distribuição IA por grande área (barras horizontais)
# ---------------------------------------------------------------------------
def fig11_distribuicao_grande_area(df: pd.DataFrame) -> None:
    counts = (
        df["NM_GRANDE_AREA_CONHECIMENTO"]
        .fillna("(não informado)")
        .value_counts()
        .sort_values()
    )
    total = counts.sum()

    cores = []
    for area in counts.index:
        if "Humanas" in str(area):
            cores.append(CORES_INTERMEDIARIAS[0])   # destaque vermelho
        else:
            cores.append(CORES_INTERMEDIARIAS[9])   # cinza para o resto

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(counts.index, counts.values, color=cores, edgecolor="white", linewidth=0.5)
    for bar, val in zip(bars, counts.values):
        pct = val / total * 100
        ax.text(
            bar.get_width() + total * 0.005,
            bar.get_y() + bar.get_height() / 2,
            f"{val:,} ({pct:.1f}%)",
            va="center", fontsize=8,
        )
    ax.set_xlabel(f"Trabalhos sobre IA (N = {total:,})")
    ax.set_ylabel("")
    ax.set_xlim(0, counts.max() * 1.18)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "capes_11_grande_area_share.png")
    plt.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  → {out}")


# ---------------------------------------------------------------------------
# Figura 12: evolução temporal por grande área (linhas)
# ---------------------------------------------------------------------------
def fig12_temporal_grande_area(df: pd.DataFrame) -> None:
    df = df.copy()
    df["AN_BASE"] = pd.to_numeric(df["AN_BASE"], errors="coerce")
    df = df.dropna(subset=["AN_BASE"])
    df["AN_BASE"] = df["AN_BASE"].astype(int)
    df["NM_GRANDE_AREA_CONHECIMENTO"] = df["NM_GRANDE_AREA_CONHECIMENTO"].fillna("(não informado)")

    pivot = (
        df.groupby(["AN_BASE", "NM_GRANDE_AREA_CONHECIMENTO"])
        .size()
        .unstack(fill_value=0)
        .sort_index()
    )

    # Ordena por volume total, descendente (linha mais grossa = top)
    pivot = pivot[pivot.sum().sort_values(ascending=False).index]

    fig, ax = plt.subplots(figsize=(11, 6.5))
    for i, area in enumerate(pivot.columns):
        is_humanas = "Humanas" in str(area)
        cor = CORES_INTERMEDIARIAS[0] if is_humanas else CORES_INTERMEDIARIAS[i % 12]
        lw = 2.5 if is_humanas else 1.5
        alpha = 1.0 if is_humanas else 0.75
        ax.plot(
            pivot.index, pivot[area],
            marker="o", linewidth=lw, alpha=alpha,
            color=cor, label=str(area),
        )

    ax.set_xlabel("Ano base de defesa")
    ax.set_ylabel("Trabalhos sobre IA")
    ax.set_xticks(sorted(pivot.index))
    ax.legend(
        loc="center left", bbox_to_anchor=(1.01, 0.5),
        frameon=False, fontsize=8,
    )
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "capes_12_temporal_grande_area.png")
    plt.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  → {out}")


# ---------------------------------------------------------------------------
# Figura 13: heatmap grande área × keyword (presença normalizada por linha)
# ---------------------------------------------------------------------------
def fig13_heatmap_area_keyword(df: pd.DataFrame) -> None:
    texto = texto_classificacao(df)
    presenca = pd.DataFrame(
        {label: texto.str.contains(pat, flags=re.IGNORECASE, regex=True, na=False)
         for label, pat in KEYWORDS_HEATMAP}
    )
    presenca["GRANDE_AREA"] = df["NM_GRANDE_AREA_CONHECIMENTO"].fillna("(não informado)").values

    bruto = presenca.groupby("GRANDE_AREA").sum(numeric_only=True)
    # Mantém só grandes áreas com pelo menos 20 registros IA para reduzir ruído
    totais = df["NM_GRANDE_AREA_CONHECIMENTO"].fillna("(não informado)").value_counts()
    keep = totais[totais >= 20].index
    bruto = bruto.loc[bruto.index.intersection(keep)]
    # Ordena linhas por volume total decrescente
    ordem_linhas = totais.loc[bruto.index].sort_values(ascending=False).index
    bruto = bruto.loc[ordem_linhas]

    # Normaliza por linha: o que cada termo representa dentro daquela área
    norm = bruto.div(bruto.sum(axis=1).replace(0, np.nan), axis=0).fillna(0) * 100

    fig, ax = plt.subplots(figsize=(11, 6.5))
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "muted_red", ["#FFFFFF", CORES_INTERMEDIARIAS[0]]
    )
    im = ax.imshow(norm.values, aspect="auto", cmap=cmap, vmin=0, vmax=norm.values.max())
    ax.set_xticks(range(len(norm.columns)))
    ax.set_xticklabels(norm.columns, rotation=40, ha="right", fontsize=8)
    ax.set_yticks(range(len(norm.index)))
    ax.set_yticklabels(norm.index, fontsize=9)
    for i in range(norm.shape[0]):
        for j in range(norm.shape[1]):
            v = norm.values[i, j]
            if v > 0:
                ax.text(
                    j, i, f"{v:.0f}",
                    ha="center", va="center",
                    color="white" if v > norm.values.max() * 0.55 else "#333",
                    fontsize=7,
                )
    cbar = plt.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_label("% de menções da grande área (por linha)", fontsize=8)
    cbar.ax.tick_params(labelsize=7)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "capes_13_heatmap_area_keyword.png")
    plt.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  → {out}")


if __name__ == "__main__":
    print("Carregando subset IA ...")
    df = carregar_ia()
    print(f"  {len(df):,} trabalhos sobre IA carregados")

    print("\nGerando figuras:")
    fig11_distribuicao_grande_area(df)
    fig12_temporal_grande_area(df)
    fig13_heatmap_area_keyword(df)

    print("\nPronto.")
