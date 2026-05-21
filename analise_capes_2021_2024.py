# -*- coding: utf-8 -*-
"""Análise CAPES 2021-2024: IA em todas as grandes áreas do conhecimento.

Carrega o dump oficial do Catálogo de Teses e Dissertações da CAPES
(BR-CAPES-BTD-2021A2024, versão 3.0, ~350 mil registros), aplica o regex
refinado de identificação de IA — agora sem restrição de área — e gera
três figuras novas que situam a marginalidade das humanidades no mapa
mais amplo da produção pós-graduada brasileira sobre IA.

Saídas:
  dados_capes/capes_2021_2024_ia.csv      planilha auditável dos trabalhos IA
  figuras/capes_11_grande_area_share.png   distribuição IA por grande área
  figuras/capes_12_temporal_grande_area.png evolução 2021-2024 por grande área
  figuras/capes_13_heatmap_area_keyword.png heatmap área × keyword

Uso:
    python analise_capes_2021_2024.py

Variáveis de ambiente:
    CAPES_DATA_DIR  diretório com os 4 XLSX (default: ./dados_capes)
                    útil quando o LFS está apenas com ponteiros locais.
"""

from __future__ import annotations

import os
import re
import sys
import glob
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from utils import (
    BASE_DIR,
    CORES_INTERMEDIARIAS,
    DADOS_CAPES_DIR,
    FIGURAS_DIR,
    RE_IA_NUCLEO,
    RE_IA_SIGLA,
    RE_IA_RELACIONADA,
    aplicar_estilo_padrao,
    classificar_foco_ia,
    garantir_diretorio,
)

aplicar_estilo_padrao()
garantir_diretorio(FIGURAS_DIR)
garantir_diretorio(DADOS_CAPES_DIR)

CAPES_DATA_DIR = os.environ.get("CAPES_DATA_DIR", DADOS_CAPES_DIR)

COLS_TEXTO = ["NM_PRODUCAO", "DS_RESUMO", "DS_PALAVRA_CHAVE", "DS_ABSTRACT", "DS_KEYWORD"]
COLS_AREA = [
    "NM_GRANDE_AREA_CONHECIMENTO",
    "NM_AREA_CONHECIMENTO",
    "NM_SUBAREA_CONHECIMENTO",
    "NM_AREA_AVALIACAO",
]
COLS_META = [
    "AN_BASE",
    "DT_TITULACAO",
    "NM_GRAU_ACADEMICO",
    "NM_ENTIDADE_ENSINO",
    "SG_ENTIDADE_ENSINO",
    "NM_REGIAO",
    "SG_UF_IES",
    "NM_UF_IES",
    "NR_PAGINAS",
    "NM_IDIOMA",
    "NM_ORIENTADOR",
    "NM_PROGRAMA",
    "ID_PRODUCAO_INTELECTUAL",
    "DS_URL_TEXTO_COMPLETO",
]
COLS_KEEP = COLS_META + COLS_AREA + COLS_TEXTO


def localizar_xlsx() -> list[Path]:
    """Encontra os 4 XLSX do dump CAPES. Aceita LFS pointer files vazios,
    nesse caso re-aponta para CAPES_DATA_DIR se diferente do default."""
    candidatos = sorted(glob.glob(os.path.join(CAPES_DATA_DIR, "br-capes-btd-*.xlsx")))
    paths = [Path(c) for c in candidatos]
    # Verifica se algum arquivo é só ponteiro LFS (< 1KB)
    pequenos = [p for p in paths if p.stat().st_size < 1024]
    if pequenos:
        sys.stderr.write(
            f"[aviso] {len(pequenos)} arquivos em {CAPES_DATA_DIR} parecem ser "
            f"ponteiros LFS (< 1KB). Defina CAPES_DATA_DIR para a pasta com os "
            f"XLSX binários completos.\n"
        )
    return paths


def carregar_dump(paths: list[Path]) -> pd.DataFrame:
    """Lê os 4 XLSX, mantém só colunas usadas, concatena."""
    partes = []
    for p in paths:
        print(f"  lendo {p.name} ...", flush=True)
        df = pd.read_excel(p, engine="openpyxl")
        # Mantém só as colunas que existem (defensivo contra schema variável)
        cols_existem = [c for c in COLS_KEEP if c in df.columns]
        partes.append(df[cols_existem])
    full = pd.concat(partes, ignore_index=True)
    return full


def construir_texto_classificacao(df: pd.DataFrame) -> pd.Series:
    """Concatena os campos textuais para a classificação por regex."""
    s = df["NM_PRODUCAO"].fillna("").astype(str)
    for c in ["DS_RESUMO", "DS_PALAVRA_CHAVE", "DS_ABSTRACT", "DS_KEYWORD"]:
        if c in df.columns:
            s = s + " | " + df[c].fillna("").astype(str)
    return s


def classificar(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona coluna FOCO_IA usando o classificador do utils."""
    texto = construir_texto_classificacao(df)
    df = df.copy()
    df["FOCO_IA"] = texto.map(classificar_foco_ia)
    return df


def relatorio_resumo(df: pd.DataFrame) -> None:
    print("\n" + "=" * 60)
    print("RESUMO DO DUMP CAPES 2021-2024")
    print("=" * 60)
    print(f"Total de registros: {len(df):,}")
    print()
    print("Por ano base:")
    print(df["AN_BASE"].value_counts().sort_index().to_string())
    print()
    print("Por grande área (top 10):")
    print(df["NM_GRANDE_AREA_CONHECIMENTO"].value_counts().head(10).to_string())
    print()
    print("Por foco em IA (classificação refinada):")
    print(df["FOCO_IA"].value_counts().to_string())
    pct_ia = (df["FOCO_IA"] != "Outros Temas").mean() * 100
    print(f"\nShare IA (Central + Relacionado): {pct_ia:.3f}% do universo")


if __name__ == "__main__":
    paths = localizar_xlsx()
    if len(paths) < 4:
        sys.exit(
            f"ERRO: esperados 4 XLSX em {CAPES_DATA_DIR}/, encontrados {len(paths)}.\n"
            f"Defina CAPES_DATA_DIR ou coloque os arquivos br-capes-btd-*.xlsx em "
            f"{CAPES_DATA_DIR}/."
        )
    print(f"Lendo dump CAPES de {CAPES_DATA_DIR} ({len(paths)} arquivos)...")
    df = carregar_dump(paths)
    print(f"  total carregado: {len(df):,} registros")

    print("\nClassificando foco em IA...")
    df = classificar(df)

    relatorio_resumo(df)

    # Salva subset IA para auditoria e uso pelas figuras
    ia = df[df["FOCO_IA"] != "Outros Temas"].copy()
    saida = os.path.join(DADOS_CAPES_DIR, "capes_2021_2024_ia.csv")
    ia.to_csv(saida, index=False)
    print(f"\nSubset IA salvo em {saida} ({len(ia):,} registros)")

    # Versão slim para o repo: drop dos campos de texto longo (resumo/abstract),
    # mantendo o suficiente para auditoria humana da classificação.
    slim_cols = [
        "ID_PRODUCAO_INTELECTUAL", "AN_BASE", "DT_TITULACAO",
        "NM_GRANDE_AREA_CONHECIMENTO", "NM_AREA_CONHECIMENTO",
        "NM_SUBAREA_CONHECIMENTO", "NM_AREA_AVALIACAO",
        "NM_GRAU_ACADEMICO", "NM_ENTIDADE_ENSINO", "SG_ENTIDADE_ENSINO",
        "NM_REGIAO", "SG_UF_IES", "NM_ORIENTADOR", "NM_PROGRAMA",
        "NM_PRODUCAO", "DS_PALAVRA_CHAVE", "DS_KEYWORD",
        "NR_PAGINAS", "NM_IDIOMA", "FOCO_IA",
    ]
    slim = ia[[c for c in slim_cols if c in ia.columns]].copy()
    saida_slim = os.path.join(DADOS_CAPES_DIR, "capes_2021_2024_ia_auditoria.xlsx")
    slim.to_excel(saida_slim, index=False, engine="openpyxl")
    print(f"Versão slim (auditoria) salva em {saida_slim}")
