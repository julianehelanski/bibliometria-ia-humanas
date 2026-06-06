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

# Paleta de alto contraste (plasma): roxo-escuro = pouca IA → amarelo = muita IA.
# Mesmo em valores baixos as cores se distinguem bem (o YlOrRd ficava pálido).
CMAP = matplotlib.colormaps["plasma"]
TETO_TREEMAP = 5.0   # subfields chegam a ~7%
TETO_PAINEL = 3.0    # topics top-por-volume ficam quase todos abaixo de 3%


def _cor(taxa: float, teto: float = TETO_TREEMAP):
    norm = matplotlib.colors.Normalize(vmin=0, vmax=teto)
    return CMAP(norm(min(float(taxa), teto)))


def _ler(nome: str) -> pd.DataFrame | None:
    caminho = os.path.join(DADOS_OPENALEX_DIR, nome)
    if not os.path.isfile(caminho):
        sys.stderr.write(f"[pulando] não encontrei {caminho} — rode "
                         "analise_openalex.py --modo temas antes.\n")
        return None
    return pd.read_csv(caminho)


def _colorbar(fig, ax, teto: float = TETO_TREEMAP) -> None:
    sm = matplotlib.cm.ScalarMappable(
        norm=matplotlib.colors.Normalize(vmin=0, vmax=teto), cmap=CMAP)
    sm.set_array([])
    cb = fig.colorbar(sm, ax=ax, shrink=0.6, pad=0.01)
    cb.set_label(f"% das publicações do tema que usam IA (escala até {teto:.0f}%+)")


# Paleta categórica clara (estilo Web of Science): cada área uma cor própria,
# todas pastéis para o rótulo preto ficar legível.
PALETA_CATEGORICA = (
    list(plt.cm.Set3.colors) + list(plt.cm.Pastel1.colors) + list(plt.cm.Pastel2.colors)
)


def fig_treemap(sufixo: str, top: int = 16) -> None:
    """openalex_10 — treemap de COMPOSIÇÃO (estilo Web of Science).

    Cada área é uma cor categórica própria; tamanho = volume. A penetração da
    IA NÃO é codificada aqui (fica no painel openalex_12 e nas barras), para o
    treemap ficar limpo e legível.
    """
    df = _ler(f"openalex_temas_humanas{sufixo}.csv")
    if df is None:
        return
    df = df.sort_values("count_universo", ascending=False).reset_index(drop=True)
    total = df["count_universo"].sum()

    # Top N áreas + um bloco "Outros" agregando a cauda.
    topo = df.head(top).copy()
    resto = df.iloc[top:]
    if len(resto):
        topo = pd.concat([topo, pd.DataFrame([{
            "subfield": f"Outros ({len(resto)} áreas)",
            "count_universo": int(resto["count_universo"].sum()),
            "pct_do_universo": round(100 * resto["count_universo"].sum() / total, 2),
        }])], ignore_index=True)

    if squarify is None:
        sys.stderr.write("[aviso] squarify ausente; gerando barra no lugar do treemap.\n")
        fig, ax = plt.subplots(figsize=(12, 9))
        d = topo.iloc[::-1]
        ax.barh(d["subfield"], d["count_universo"], color=PALETA_CATEGORICA[:len(d)])
        out = os.path.join(garantir_diretorio(FIGURAS_DIR), "openalex_10_treemap_temas.png")
        fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
        plt.close(fig)
        print(f"  -> {out}")
        return

    import textwrap
    cores = [PALETA_CATEGORICA[i % len(PALETA_CATEGORICA)] for i in range(len(topo))]
    labels = []
    for _, r in topo.iterrows():
        share = r["count_universo"] / total
        nome = "\n".join(textwrap.wrap(str(r["subfield"]), 18))
        if share >= 0.03:                      # áreas grandes: nome + %
            labels.append(f"{nome}\n{r['pct_do_universo']:.1f}%")
        elif share >= 0.013:                   # médias: só o nome
            labels.append(nome)
        else:                                  # pequenas: sem rótulo (evita sobreposição)
            labels.append("")

    fig, ax = plt.subplots(figsize=(16, 9))
    squarify.plot(sizes=topo["count_universo"], label=labels, color=cores,
                  ax=ax, pad=True, ec="white",
                  text_kwargs={"fontsize": 9, "color": "black"})
    ax.axis("off")
    ax.set_title("De que é feita a produção brasileira em Ciências Humanas\n"
                 "áreas (subfields) por volume de publicações, 2016–2024",
                 fontsize=14)
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
                color=[_cor(t, TETO_PAINEL) for t in d["taxa_ia_%"]])
        for y, (v, t) in enumerate(zip(d["count_universo"], d["taxa_ia_%"])):
            ax.text(v, y, f"  {int(v):,}".replace(",", ".") + f"  ·  IA {t:.1f}%",
                    va="center", fontsize=7.5)
        ax.set_title(titulo, fontsize=12, loc="left", fontweight="bold")
        ax.set_xlabel("publicações no universo de Humanidades (2016–2024)")
        ax.margins(x=0.22)

    _colorbar(fig, list(axes), TETO_PAINEL)
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
