# -*- coding: utf-8 -*-
"""Figuras temáticas do universo de Humanidades (OpenAlex) — de que ele é feito.

Complementa figuras_openalex.py. Ilustra a COMPOSIÇÃO da produção de Ciências
Humanas (do que o país publica) e onde a IA penetra, em dois níveis:
  - subfield (treemap): áreas como "Sociology and Political Science", "Education"
  - topic (barras): temas específicos mais frequentes

Pré-requisito de dados:
    python analise_openalex.py --modo temas --pais BR --mailto SEU_EMAIL
    (gera openalex_temas_humanas_BR.csv e openalex_topics_humanas_BR.csv)

Pré-requisito de pacotes:
    pip install squarify

Saídas em figuras/:
    openalex_10_treemap_temas.png   composição por subfield (treemap)
    openalex_11_topics_temas.png    temas específicos mais frequentes

Uso:
    python figuras_openalex_temas.py [--pais BR]
"""

from __future__ import annotations

import argparse
import os
import sys

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from utils import FIGURAS_DIR, aplicar_estilo_padrao, garantir_diretorio

try:
    import squarify
except ImportError:  # pragma: no cover
    squarify = None

aplicar_estilo_padrao()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_OPENALEX_DIR = os.path.join(BASE_DIR, "dados_openalex")

# Teto da escala de cor (taxa de IA). Os bolsões quantitativos (Psicologias)
# chegam a ~7%; o teto realça o contraste com o grosso interpretativo (~1%).
TETO_COR = 5.0
CMAP = matplotlib.colormaps["YlOrRd"]
NORM = matplotlib.colors.Normalize(vmin=0, vmax=TETO_COR)


def _cor(taxa: float):
    return CMAP(NORM(min(float(taxa), TETO_COR)))


def _ler(nome: str) -> pd.DataFrame | None:
    caminho = os.path.join(DADOS_OPENALEX_DIR, nome)
    if not os.path.isfile(caminho):
        sys.stderr.write(f"[pulando] não encontrei {caminho} — rode "
                         "analise_openalex.py --modo temas antes.\n")
        return None
    return pd.read_csv(caminho)


def _colorbar(fig, ax) -> None:
    sm = matplotlib.cm.ScalarMappable(norm=NORM, cmap=CMAP)
    sm.set_array([])
    cb = fig.colorbar(sm, ax=ax, shrink=0.6, pad=0.01)
    cb.set_label(f"Penetração da IA no tema (%) — escala até {TETO_COR:.0f}%+")


def fig_treemap(sufixo: str, top: int = 18) -> None:
    """openalex_10 — treemap: tamanho = volume, cor = penetração da IA."""
    df = _ler(f"openalex_temas_humanas{sufixo}.csv")
    if df is None:
        return
    df = df.sort_values("count_universo", ascending=False).head(top)
    cores = [_cor(t) for t in df["taxa_ia_%"]]
    # Rótulo só nos retângulos com peso suficiente, para não poluir.
    labels = [
        f"{r['subfield']}\n{r['pct_do_universo']:.1f}%" if r["pct_do_universo"] >= 1.3 else ""
        for _, r in df.iterrows()
    ]

    fig, ax = plt.subplots(figsize=(14, 8))
    if squarify is None:
        sys.stderr.write("[aviso] squarify ausente; gerando barra no lugar do treemap.\n")
        d = df.iloc[::-1]
        ax.barh(d["subfield"], d["count_universo"], color=[_cor(t) for t in d["taxa_ia_%"]])
    else:
        squarify.plot(sizes=df["count_universo"], label=labels, color=cores,
                      ax=ax, pad=True, ec="white",
                      text_kwargs={"fontsize": 9, "color": "black"})
        ax.axis("off")
    _colorbar(fig, ax)
    ax.set_title("De que é feita a produção brasileira em Ciências Humanas\n"
                 "tamanho = volume de publicações · cor = penetração da IA no tema",
                 fontsize=13)
    fig.tight_layout()
    out = os.path.join(garantir_diretorio(FIGURAS_DIR), "openalex_10_treemap_temas.png")
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  -> {out}")


def fig_topics(sufixo: str, top: int = 20) -> None:
    """openalex_11 — barras dos temas específicos (topics) mais frequentes."""
    df = _ler(f"openalex_topics_humanas{sufixo}.csv")
    if df is None:
        return
    df = df.sort_values("count_universo", ascending=False).head(top).iloc[::-1]
    cores = [_cor(t) for t in df["taxa_ia_%"]]

    fig, ax = plt.subplots(figsize=(11, 9))
    ax.barh(df["topic"].astype(str), df["count_universo"], color=cores)
    for y, v in enumerate(df["count_universo"]):
        ax.text(v, y, f" {int(v):,}".replace(",", "."), va="center", fontsize=8)
    ax.set_xlabel("Publicações no universo de Humanidades (2016–2024)")
    ax.set_title(f"Temas específicos mais frequentes nas Ciências Humanas do Brasil\n"
                 f"(top {top} topics · cor = penetração da IA no tema)", fontsize=12)
    ax.margins(x=0.13)
    _colorbar(fig, ax)
    fig.tight_layout()
    out = os.path.join(garantir_diretorio(FIGURAS_DIR), "openalex_11_topics_temas.png")
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  -> {out}")


# Áreas das ciências sociais para o painel (slug do arquivo, título exibido).
AREAS_SOCIAIS = [
    ("anthropology", "Antropologia"),
    ("sociology_and_political_science", "Sociologia e Ciência Política"),
    ("political_science_and_international_relations", "Ciência Política e Rel. Internacionais"),
]


def fig_painel_areas(sufixo: str, top: int = 10, areas=AREAS_SOCIAIS) -> None:
    """openalex_12 — painel: top temas de cada ciência social, cor = penetração da IA."""
    dfs = []
    for slug, titulo in areas:
        df = _ler(f"openalex_topics_{slug}{sufixo}.csv")
        if df is not None and not df.empty:
            dfs.append((titulo, df))
    if not dfs:
        sys.stderr.write("[pulando painel] rode antes: analise_openalex.py --modo temas "
                         "--subfield \"Anthropology,Sociology and Political Science,"
                         "Political Science and International Relations\"\n")
        return

    n = len(dfs)
    fig, axes = plt.subplots(n, 1, figsize=(12, 4.7 * n), constrained_layout=True)
    if n == 1:
        axes = [axes]
    for ax, (titulo, df) in zip(axes, dfs):
        d = df.sort_values("count_universo", ascending=False).head(top).iloc[::-1]
        ax.barh(d["topic"].astype(str), d["count_universo"],
                color=[_cor(t) for t in d["taxa_ia_%"]])
        for y, (v, t) in enumerate(zip(d["count_universo"], d["taxa_ia_%"])):
            ax.text(v, y, f"  {int(v):,}".replace(",", ".") + f"  ·  IA {t:.1f}%",
                    va="center", fontsize=7.5)
        ax.set_title(titulo, fontsize=12, loc="left", fontweight="bold")
        ax.set_xlabel("publicações no universo de Humanidades (2016–2024)")
        ax.margins(x=0.22)

    _colorbar(fig, list(axes))
    fig.suptitle("O que as ciências sociais brasileiras estudam — e onde a IA entra\n"
                 "(barras = temas mais frequentes por área · cor = penetração da IA)",
                 fontsize=14)
    out = os.path.join(garantir_diretorio(FIGURAS_DIR), "openalex_12_painel_ciencias_sociais.png")
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  -> {out}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pais", default="BR", help="Sufixo do país (default BR; use vazio p/ global)")
    args = parser.parse_args()
    sufixo = f"_{args.pais.upper()}" if args.pais else "_global"
    print("Gerando figuras temáticas OpenAlex em figuras/ ...")
    fig_treemap(sufixo)
    fig_topics(sufixo)
    fig_painel_areas(sufixo)
    print("Concluído.")


if __name__ == "__main__":
    main()
