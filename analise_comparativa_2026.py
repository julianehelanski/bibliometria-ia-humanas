# -*- coding: utf-8 -*-
"""Análise comparativa SciELO × CAPES — versão 2026.

Substitui o analise_comparativa.py antigo. Lê os outputs novos de
ambas as bases (SciELO via ArticleMeta + CAPES via dump oficial),
restringe a 2021-2024 estrito, e produz figura comparativa + tabelas.

Pré-requisitos:
- dados_scielo/scielo_ia_subcampos.csv (gerado por
  analise_scielo_articlemeta.py)
- dados_capes/capes_2021_2024_ia_auditoria.xlsx (gerado por
  analise_capes_2021_2024.py)

Saídas:
- figuras/comparativo_scielo_capes_2026.png
- tabelas_comparativas_2026.md
"""

from __future__ import annotations

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from utils import (
    CORES_INTERMEDIARIAS,
    DADOS_CAPES_DIR,
    DADOS_SCIELO_DIR,
    FIGURAS_DIR,
    aplicar_estilo_padrao,
    garantir_diretorio,
)

aplicar_estilo_padrao()
garantir_diretorio(FIGURAS_DIR)

COR_SCIELO = CORES_INTERMEDIARIAS[3]   # azul
COR_CAPES = CORES_INTERMEDIARIAS[0]    # vermelho

ANO_MIN = 2021
ANO_MAX = 2024

SUBCAMPOS = [
    ("SUBCAMPO_IA_STRICTO", "IA em sentido estrito"),
    ("SUBCAMPO_ML", "Aprendizado de máquina (ML)"),
    ("SUBCAMPO_DL", "Aprendizado profundo & redes neurais"),
    ("SUBCAMPO_LLM", "Modelos de linguagem & IA generativa"),
    ("SUBCAMPO_CORRELATOS", "Tecnologias correlatas"),
]


def _bool(s):
    if s.dtype == bool:
        return s
    return s.astype(str).str.lower().isin(["true", "1"])


def carregar_scielo() -> pd.DataFrame:
    df = pd.read_csv(os.path.join(DADOS_SCIELO_DIR, "scielo_ia_subcampos.csv"), low_memory=False)
    df["ano"] = pd.to_numeric(df["ano"], errors="coerce").astype("Int64")
    n_pre = len(df)
    df = df[(df["ano"] >= ANO_MIN) & (df["ano"] <= ANO_MAX)].copy()
    print(f"SciELO: {n_pre} → {len(df)} após restrição a {ANO_MIN}-{ANO_MAX}")
    return df


def carregar_capes() -> pd.DataFrame:
    """Carrega CAPES IA-Humanas (restrito a grande área Ciências Humanas)
    para comparabilidade com SciELO (que também é só Humanas + Sociais
    Aplicadas + Letras)."""
    df = pd.read_excel(os.path.join(DADOS_CAPES_DIR, "capes_2021_2024_ia_auditoria.xlsx"),
                       engine="openpyxl")
    df["AN_BASE"] = pd.to_numeric(df["AN_BASE"], errors="coerce").astype("Int64")
    df = df[df["NM_GRANDE_AREA_CONHECIMENTO"].str.contains("HUMANAS", case=False, na=False)]
    df = df[(df["AN_BASE"] >= ANO_MIN) & (df["AN_BASE"] <= ANO_MAX)].copy()
    print(f"CAPES Humanas: {len(df)} ({ANO_MIN}-{ANO_MAX})")
    return df


def fig_comparativa(sci: pd.DataFrame, cap: pd.DataFrame) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(13, 10), constrained_layout=True)

    # ----- (A) Evolução temporal sobreposta -----
    ax = axes[0, 0]
    s_ano = sci.groupby("ano").size().reindex(range(ANO_MIN, ANO_MAX + 1), fill_value=0)
    c_ano = cap.groupby("AN_BASE").size().reindex(range(ANO_MIN, ANO_MAX + 1), fill_value=0)
    ax.plot(s_ano.index, s_ano.values, marker="o", color=COR_SCIELO, linewidth=2.5,
            label=f"SciELO (n={s_ano.sum()})")
    ax.plot(c_ano.index, c_ano.values, marker="s", color=COR_CAPES, linewidth=2.5,
            label=f"CAPES Humanas (n={c_ano.sum()})")
    for x, y in zip(s_ano.index, s_ano.values):
        ax.text(x, y + 3, f"{y}", ha="center", color=COR_SCIELO, fontsize=8)
    for x, y in zip(c_ano.index, c_ano.values):
        ax.text(x, y + 3, f"{y}", ha="center", color=COR_CAPES, fontsize=8)
    ax.set_title("Evolução 2021–2024", fontsize=10)
    ax.set_xlabel("Ano")
    ax.set_ylabel("Publicações sobre IA/ML/DL")
    ax.set_xticks(range(ANO_MIN, ANO_MAX + 1))
    ax.legend(loc="upper left", frameon=False)

    # ----- (B) Distribuição por subcampo (lado a lado) -----
    ax = axes[0, 1]
    labels = [l for _, l in SUBCAMPOS]
    sci_vals = []
    cap_vals = []
    for col, _ in SUBCAMPOS:
        sci_vals.append(int(_bool(sci[col]).sum()) if col in sci.columns else 0)
        cap_vals.append(int(_bool(cap[col]).sum()) if col in cap.columns else 0)
    # Normaliza pra ficar % de cada base
    sci_pct = np.array(sci_vals) / max(len(sci), 1) * 100
    cap_pct = np.array(cap_vals) / max(len(cap), 1) * 100
    x = np.arange(len(labels))
    w = 0.38
    ax.barh(x + w/2, sci_pct, w, color=COR_SCIELO, label="SciELO", edgecolor="white")
    ax.barh(x - w/2, cap_pct, w, color=COR_CAPES, label="CAPES Humanas", edgecolor="white")
    for i, (sv, cv) in enumerate(zip(sci_pct, cap_pct)):
        ax.text(sv + 1, i + w/2, f"{sv:.1f}%", va="center", fontsize=7, color=COR_SCIELO)
        ax.text(cv + 1, i - w/2, f"{cv:.1f}%", va="center", fontsize=7, color=COR_CAPES)
    ax.set_yticks(x)
    ax.set_yticklabels([l.replace(" & ", "\n& ").replace(" (", "\n(") for l in labels], fontsize=8)
    ax.set_xlabel("% do corpus que toca o subcampo")
    ax.set_title("Distribuição por subcampo (% do corpus de cada base)", fontsize=10)
    ax.legend(loc="lower right", frameon=False)

    # ----- (C) Top periódicos SciELO -----
    ax = axes[1, 0]
    top_per = sci["periodico"].fillna("(s/info)").value_counts().head(10).sort_values()
    bars = ax.barh(top_per.index, top_per.values, color=COR_SCIELO, edgecolor="white", linewidth=0.5)
    for bar, val in zip(bars, top_per.values):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f"{val}", va="center", fontsize=8)
    ax.set_title("SciELO: top 10 periódicos", fontsize=10)
    ax.set_xlabel("Artigos sobre IA/ML/DL")
    ax.set_xlim(0, max(top_per.values) * 1.18)
    # Trunca labels longas
    ax.set_yticklabels([t[:38] + "…" if len(t) > 38 else t for t in top_per.index], fontsize=8)

    # ----- (D) Top áreas CAPES Humanas -----
    ax = axes[1, 1]
    top_area = cap["NM_AREA_CONHECIMENTO"].fillna("(s/info)").value_counts().head(10).sort_values()
    bars = ax.barh(top_area.index, top_area.values, color=COR_CAPES, edgecolor="white", linewidth=0.5)
    for bar, val in zip(bars, top_area.values):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                f"{val}", va="center", fontsize=8)
    ax.set_title("CAPES Humanas: top 10 áreas de conhecimento", fontsize=10)
    ax.set_xlabel("Defesas sobre IA/ML/DL")
    ax.set_xlim(0, max(top_area.values) * 1.18)

    out = os.path.join(FIGURAS_DIR, "comparativo_scielo_capes_2026.png")
    plt.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.savefig(out.replace(".png", ".svg"), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  → {out}")


def tabela_markdown(sci: pd.DataFrame, cap: pd.DataFrame) -> None:
    linhas = []
    linhas.append("# Tabelas comparativas SciELO × CAPES (2026)\n")
    linhas.append("Coleta: SciELO via API ArticleMeta + CAPES via dump oficial 2021-2024.")
    linhas.append("Classificação: regex de subcampos do `utils.classificar_subcampos`,")
    linhas.append("com regra de co-ocorrência para `transformer` e para a sigla 'IA'.\n")

    # Sumário
    linhas.append("## Sumário (2021–2024)\n")
    linhas.append("| Indicador | SciELO | CAPES Humanas |")
    linhas.append("|---|---:|---:|")
    linhas.append(f"| Total no campo | {len(sci):,} | {len(cap):,} |")
    sci_central = (sci["FOCO_IA"] == "Tecnologias IA/ML/DL - Foco Central").sum()
    cap_central = (cap["FOCO_IA"] == "Tecnologias IA/ML/DL - Foco Central").sum()
    linhas.append(f"| Foco Central | {sci_central} | {cap_central} |")
    linhas.append(f"| Correlatos | {len(sci)-sci_central} | {len(cap)-cap_central} |")

    # Subcampos
    linhas.append("\n## Distribuição por subcampo\n")
    linhas.append("| Subcampo | SciELO | % SciELO | CAPES | % CAPES |")
    linhas.append("|---|---:|---:|---:|---:|")
    for col, label in SUBCAMPOS:
        s = int(_bool(sci[col]).sum()) if col in sci.columns else 0
        c = int(_bool(cap[col]).sum()) if col in cap.columns else 0
        linhas.append(f"| {label} | {s} | {s/max(len(sci),1)*100:.1f}% | {c} | {c/max(len(cap),1)*100:.1f}% |")

    # Temporal
    linhas.append("\n## Evolução temporal\n")
    linhas.append("| Ano | SciELO | CAPES |")
    linhas.append("|---:|---:|---:|")
    for ano in range(ANO_MIN, ANO_MAX + 1):
        s = int((sci["ano"] == ano).sum())
        c = int((cap["AN_BASE"] == ano).sum())
        linhas.append(f"| {ano} | {s} | {c} |")

    # Top periódicos / top áreas
    linhas.append("\n## SciELO — top 10 periódicos\n")
    linhas.append("| Periódico | Artigos |")
    linhas.append("|---|---:|")
    for per, n in sci["periodico"].fillna("(s/info)").value_counts().head(10).items():
        linhas.append(f"| {per} | {n} |")

    linhas.append("\n## CAPES Humanas — top 10 áreas\n")
    linhas.append("| Área | Defesas |")
    linhas.append("|---|---:|")
    for area, n in cap["NM_AREA_CONHECIMENTO"].fillna("(s/info)").value_counts().head(10).items():
        linhas.append(f"| {area} | {n} |")

    out = "tabelas_comparativas_2026.md"
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")
    print(f"  → {out}")


if __name__ == "__main__":
    print("Carregando SciELO ...")
    sci = carregar_scielo()
    print("Carregando CAPES Humanas ...")
    cap = carregar_capes()
    print("\nGerando comparativo:")
    fig_comparativa(sci, cap)
    tabela_markdown(sci, cap)
    print("\nPronto.")
