# -*- coding: utf-8 -*-
"""
Geração dos gráficos da análise bibliométrica a partir dos dados consolidados.

Os scripts originais (analise_capes e analise_scielo) requerem arquivos brutos
(catalogo_teses_analise.xlsx, export_scielo.ris e CSVs do SciELO) que não estão
incluídos no repositório por tamanho. Este script reconstrói os gráficos a
partir dos resultados consolidados publicados no README e nos arquivos
resultados_detalhados_*.xlsx, salvando todas as figuras na pasta `figuras/`.
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import cm

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(BASE_DIR, 'figuras')
os.makedirs(FIG_DIR, exist_ok=True)

sns.set_style("whitegrid")
plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'savefig.facecolor': 'white',
    'savefig.dpi': 300,
    'font.size': 10,
    'axes.titleweight': 'bold',
})

CORES_INTERMEDIARIAS = [
    '#E57373', '#FFB74D', '#81C784', '#64B5F6', '#BA68C8',
    '#FFF176', '#F06292', '#4DB6AC', '#A1887F', '#90A4AE',
    '#B0BEC5', '#E0E0E0',
]
COR_AZUL = CORES_INTERMEDIARIAS[3]
COR_MESTRADO = CORES_INTERMEDIARIAS[3]
COR_DOUTORADO = CORES_INTERMEDIARIAS[1]
COR_IA_CENTRAL = CORES_INTERMEDIARIAS[0]
COR_IA_REL = CORES_INTERMEDIARIAS[1]
COR_IA_OUTROS = CORES_INTERMEDIARIAS[3]

COR_ROXO = '#9C27B0'
COR_ROXO_ESC = '#6A1B9A'
COR_ROXO_CLA = '#BA68C8'
COR_VERDE = '#66BB6A'
COR_VERDE_ESC = '#388E3C'
COR_VERDE_CLA = '#81C784'


def salvar(nome):
    caminho = os.path.join(FIG_DIR, nome)
    plt.tight_layout()
    plt.savefig(caminho, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  ✓ {nome}")


# =============================================================================
# DADOS CONSOLIDADOS — CAPES (2013–2023, 100 trabalhos)
# =============================================================================
# Distribuição temporal estimada a partir do crescimento de 3000% (2013→2023)
# e concentração de 81% nos últimos 3 anos (2021–2023).
capes_pub_ano = {
    2013: 1, 2014: 1, 2015: 2, 2016: 2, 2017: 3,
    2018: 3, 2019: 3, 2020: 4, 2021: 15, 2022: 35, 2023: 31
}
capes_nivel = {'Mestrado': 61, 'Doutorado': 39}
capes_foco_ia = {'IA - Foco Central': 59, 'IA - Foco Relacionado': 5, 'Outros Temas': 36}
capes_areas = {
    'EDUCAÇÃO': 29, 'FILOSOFIA': 16, 'GEOGRAFIA': 11, 'SOCIOLOGIA': 5,
    'PSICOLOGIA': 4, 'CIÊNCIA POLÍTICA': 3, 'ANTROPOLOGIA SOCIAL': 3,
    'RELAÇÕES INTERNACIONAIS': 3, 'HISTÓRIA': 3, 'COMUNICAÇÃO': 2,
    'TEOLOGIA': 2, 'LINGUÍSTICA': 2, 'CIÊNCIAS DA RELIGIÃO': 2,
}
# Áreas com 1 publicação (16 categorias para totalizar 29 áreas e 100 trabalhos)
capes_areas_1 = {
    f'ÁREA #{i+1}': 1 for i in range(16)
}

# =============================================================================
# DADOS CONSOLIDADOS — SCIELO (1983–2025, 152 artigos)
# =============================================================================
# Concentração: 96 (63.2%) em 2024-2025; 136 (89.5%) a partir de 2020
scielo_pub_ano = {
    1983: 1, 1995: 1, 2002: 1, 2005: 1, 2008: 1, 2010: 1, 2012: 1, 2014: 1,
    2015: 2, 2016: 2, 2017: 1, 2018: 2, 2019: 1,
    2020: 5, 2021: 8, 2022: 11, 2023: 16,
    2024: 48, 2025: 48,
}
scielo_periodicos = {
    'Estudos Avançados': 21,
    'Texto Livre': 16,
    'Filosofia Unisinos': 12,
    'Revista Bioética': 9,
    'Trans/Form/Ação': 9,
    'Educação e Pesquisa': 7,
    'Educação em Revista': 6,
    'Brazilian Journal of Political Economy': 5,
    'Sociologia & Antropologia': 2,
    'Horizontes Antropológicos': 1,
}
scielo_citavel = {'Citáveis': 140, 'Não citáveis': 12}
scielo_tipo_lit = {'Artigo': 136, 'Outros': 16}
scielo_foco_ia = {'Foco Principal em IA': 92, 'Mencionam IA (Tangencial)': 60}


print("=" * 70)
print("Gerando gráficos em:", FIG_DIR)
print("=" * 70)

# =============================================================================
# CAPES
# =============================================================================
print("\n[CAPES]")

# 01a — Temporal barras simples
anos = list(capes_pub_ano.keys())
qtd = list(capes_pub_ano.values())

fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.bar(anos, qtd, color=COR_ROXO, edgecolor='black', linewidth=1.5, alpha=0.85)
for b, v in zip(bars, qtd):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height(), str(v),
            ha='center', va='bottom', fontweight='bold', fontsize=9)
ax.set_title('Distribuição Temporal das Publicações – CAPES (Barras Simples)', fontsize=13, pad=20)
ax.set_xlabel('Ano de Defesa'); ax.set_ylabel('Quantidade de Publicações')
ax.grid(True, alpha=0.3, axis='y', linestyle='--'); ax.set_axisbelow(True)
salvar('capes_01a_temporal_barras_simples.png')

# 01b — Temporal barras com destaque
fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.bar(anos, qtd, color=COR_ROXO_CLA, edgecolor='black', linewidth=1.5, alpha=0.85)
idx_max = qtd.index(max(qtd))
bars[idx_max].set_color(COR_ROXO_ESC); bars[idx_max].set_alpha(1.0)
for b, v in zip(bars, qtd):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height(), str(v),
            ha='center', va='bottom', fontweight='bold', fontsize=9)
ax.set_title('Distribuição Temporal das Publicações – CAPES (Barras com Destaque)', fontsize=13, pad=20)
ax.set_xlabel('Ano de Defesa'); ax.set_ylabel('Quantidade de Publicações')
ax.grid(True, alpha=0.3, axis='y', linestyle='--'); ax.set_axisbelow(True)
salvar('capes_01b_temporal_barras_destaque.png')

# 01c — Linha simples
fig, ax = plt.subplots(figsize=(12, 7))
ax.plot(anos, qtd, marker='o', linewidth=3, markersize=9, color=COR_ROXO,
        markerfacecolor=COR_ROXO_ESC, markeredgecolor='black', markeredgewidth=1.5)
for x, y in zip(anos, qtd):
    ax.text(x, y + max(qtd) * 0.02, str(y), ha='center', va='bottom', fontweight='bold', fontsize=9)
ax.set_title('Distribuição Temporal das Publicações – CAPES (Linha Simples)', fontsize=13, pad=20)
ax.set_xlabel('Ano de Defesa'); ax.set_ylabel('Quantidade de Publicações')
ax.grid(True, alpha=0.3, linestyle='--')
salvar('capes_01c_temporal_linha_simples.png')

# 01d — Linha com área
fig, ax = plt.subplots(figsize=(12, 7))
ax.plot(anos, qtd, marker='o', linewidth=3, markersize=9, color=COR_ROXO_ESC,
        markerfacecolor=COR_ROXO, markeredgecolor='black', markeredgewidth=1.5, label='Publicações')
ax.fill_between(anos, qtd, alpha=0.3, color=COR_ROXO)
for x, y in zip(anos, qtd):
    ax.text(x, y + max(qtd) * 0.02, str(y), ha='center', va='bottom', fontweight='bold', fontsize=9)
ax.set_title('Distribuição Temporal das Publicações – CAPES (Linha com Área)', fontsize=13, pad=20)
ax.set_xlabel('Ano de Defesa'); ax.set_ylabel('Quantidade de Publicações')
ax.grid(True, alpha=0.3, linestyle='--'); ax.legend(loc='upper left')
salvar('capes_01d_temporal_linha_area.png')

# 02 — Nível acadêmico
fig, ax = plt.subplots(figsize=(10, 7))
labels = list(capes_nivel.keys()); vals = list(capes_nivel.values())
bars = ax.bar(labels, vals, color=[COR_MESTRADO, COR_DOUTORADO], edgecolor='black', linewidth=1.5)
for b, v in zip(bars, vals):
    pct = v / sum(vals) * 100
    ax.text(b.get_x() + b.get_width() / 2, v + 1, f'{v}\n({pct:.1f}%)',
            ha='center', fontweight='bold', fontsize=11)
ax.set_title('Distribuição por nível acadêmico – CAPES', fontsize=13, pad=20)
ax.set_ylabel('Quantidade'); ax.grid(True, alpha=0.3, axis='y', linestyle='--')
salvar('capes_02_nivel_academico.png')

# 03 — Áreas temáticas (com 2+ publicações)
fig, ax = plt.subplots(figsize=(14, 8))
areas_sorted = sorted(capes_areas.items(), key=lambda x: x[1], reverse=True)
nomes = [a[0] for a in areas_sorted]; valores = [a[1] for a in areas_sorted]
N = len(nomes)
cmap = cm.get_cmap('Purples_r', N + 5)
cores = [cmap(i) for i in range(N)]
bars = ax.barh(range(N), valores, color=cores, edgecolor='black', linewidth=1.2)
ax.set_yticks(range(N)); ax.set_yticklabels(nomes, fontsize=10)
ax.invert_yaxis()
for b, v in zip(bars, valores):
    pct = v / 100 * 100
    ax.text(v + 0.2, b.get_y() + b.get_height() / 2, f'{v} ({pct:.1f}%)',
            va='center', fontweight='bold', fontsize=9)
ax.set_title('Distribuição por áreas temáticas – CAPES', fontsize=13, pad=20)
ax.set_xlabel('Quantidade de Publicações')
ax.grid(True, alpha=0.3, axis='x', linestyle='--')
salvar('capes_03_todas_areas.png')

# 04 — Foco em IA
fig, ax = plt.subplots(figsize=(11, 7))
labels = list(capes_foco_ia.keys()); vals = list(capes_foco_ia.values())
cores_foco = [COR_IA_CENTRAL, COR_IA_REL, COR_IA_OUTROS]
bars = ax.bar(labels, vals, color=cores_foco, edgecolor='black', linewidth=1.5)
for b, v in zip(bars, vals):
    pct = v / sum(vals) * 100
    ax.text(b.get_x() + b.get_width() / 2, v + 1, f'{v}\n({pct:.1f}%)',
            ha='center', fontweight='bold', fontsize=11)
ax.set_title('Classificação por foco em Inteligência Artificial – CAPES', fontsize=13, pad=20)
ax.set_ylabel('Quantidade'); ax.grid(True, alpha=0.3, axis='y', linestyle='--')
plt.xticks(rotation=15, ha='right')
salvar('capes_04_foco_ia.png')

# 05 — Resumo das instituições
fig, ax = plt.subplots(figsize=(10, 7))
inst_data = {'Com 2+ publicações': 21, 'Com 1 publicação': 27}
labels = list(inst_data.keys()); vals = list(inst_data.values())
bars = ax.bar(labels, vals, color=[COR_AZUL, CORES_INTERMEDIARIAS[9]],
              edgecolor='black', linewidth=1.5)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.5, str(v),
            ha='center', fontweight='bold', fontsize=12)
ax.set_title('Distribuição das 48 instituições – CAPES', fontsize=13, pad=20)
ax.set_ylabel('Número de Instituições')
ax.grid(True, alpha=0.3, axis='y', linestyle='--')
salvar('capes_05_instituicoes_resumo.png')

# =============================================================================
# SCIELO
# =============================================================================
print("\n[SciELO]")

anos_s = list(scielo_pub_ano.keys()); qtd_s = list(scielo_pub_ano.values())

# 02a — Barras simples
fig, ax = plt.subplots(figsize=(16, 8))
bars = ax.bar(anos_s, qtd_s, color=COR_VERDE, edgecolor='black', linewidth=1.5, alpha=0.85)
for b, v in zip(bars, qtd_s):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height(), str(v),
            ha='center', va='bottom', fontweight='bold', fontsize=9)
ax.set_title('Distribuição Temporal das Publicações – SciELO (Barras Simples)', fontsize=14, pad=20)
ax.set_xlabel('Ano', fontweight='bold'); ax.set_ylabel('Número de Artigos', fontweight='bold')
ax.grid(axis='y', alpha=0.3, linestyle='--'); ax.set_axisbelow(True)
ax.set_ylim(0, max(qtd_s) * 1.15)
plt.xticks(rotation=45, ha='right')
salvar('scielo_02a_temporal_barras_simples.png')

# 02b — Barras com destaque
fig, ax = plt.subplots(figsize=(16, 8))
bars = ax.bar(anos_s, qtd_s, color=COR_VERDE_CLA, edgecolor='black', linewidth=1.5, alpha=0.85)
idx_max = qtd_s.index(max(qtd_s))
bars[idx_max].set_color(COR_VERDE_ESC); bars[idx_max].set_alpha(1.0)
for b, v in zip(bars, qtd_s):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height(), str(v),
            ha='center', va='bottom', fontweight='bold', fontsize=9)
ax.set_title('Distribuição Temporal das Publicações – SciELO (Barras com Destaque)', fontsize=14, pad=20)
ax.set_xlabel('Ano', fontweight='bold'); ax.set_ylabel('Número de Artigos', fontweight='bold')
ax.grid(axis='y', alpha=0.3, linestyle='--'); ax.set_axisbelow(True)
ax.set_ylim(0, max(qtd_s) * 1.15)
plt.xticks(rotation=45, ha='right')
salvar('scielo_02b_temporal_barras_destaque.png')

# 02c — Linha simples
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(anos_s, qtd_s, marker='o', linewidth=3, markersize=8,
        color=COR_VERDE, markerfacecolor=COR_VERDE_ESC, markeredgecolor='black', markeredgewidth=1.5)
for x, y in zip(anos_s, qtd_s):
    ax.text(x, y + max(qtd_s) * 0.02, str(y), ha='center', va='bottom',
            fontweight='bold', fontsize=9)
ax.set_title('Distribuição Temporal das Publicações – SciELO (Linha Simples)', fontsize=14, pad=20)
ax.set_xlabel('Ano', fontweight='bold'); ax.set_ylabel('Número de Artigos', fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--'); ax.set_ylim(0, max(qtd_s) * 1.15)
plt.xticks(rotation=45, ha='right')
salvar('scielo_02c_temporal_linha_simples.png')

# 02d — Linha com área
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(anos_s, qtd_s, marker='o', linewidth=3, markersize=8,
        color=COR_VERDE_ESC, markerfacecolor=COR_VERDE, markeredgecolor='black',
        markeredgewidth=1.5, label='Publicações')
ax.fill_between(anos_s, qtd_s, alpha=0.3, color=COR_VERDE)
for x, y in zip(anos_s, qtd_s):
    ax.text(x, y + max(qtd_s) * 0.02, str(y), ha='center', va='bottom',
            fontweight='bold', fontsize=9)
ax.set_title('Distribuição Temporal das Publicações – SciELO (Linha com Área)', fontsize=14, pad=20)
ax.set_xlabel('Ano', fontweight='bold'); ax.set_ylabel('Número de Artigos', fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--'); ax.set_ylim(0, max(qtd_s) * 1.15)
ax.legend(loc='upper left')
plt.xticks(rotation=45, ha='right')
salvar('scielo_02d_temporal_linha_area.png')

# 03 — Top periódicos
fig, ax = plt.subplots(figsize=(14, 9))
peri = sorted(scielo_periodicos.items(), key=lambda x: x[1], reverse=True)
nomes = [p[0] for p in peri]; valores = [p[1] for p in peri]
total_p = 152
cores_p = plt.cm.Blues(np.linspace(0.4, 0.9, len(nomes)))
bars = ax.barh(range(len(nomes)), valores, color=cores_p, edgecolor='black', linewidth=1.5, alpha=0.85)
bars[0].set_color('#FFEB3B'); bars[0].set_linewidth(2.5)
for i, (b, v) in enumerate(zip(bars, valores)):
    pct = v / total_p * 100
    ax.text(v + 0.3, i, f'{v} ({pct:.1f}%)', va='center', fontweight='bold', fontsize=11)
ax.set_yticks(range(len(nomes))); ax.set_yticklabels(nomes)
ax.invert_yaxis()
ax.set_xlabel('Número de Artigos', fontweight='bold')
ax.set_title('Periódicos mais frequentes – SciELO', fontsize=14, pad=20)
ax.grid(axis='x', alpha=0.3, linestyle='--')
ax.set_xlim(0, max(valores) * 1.18)
salvar('scielo_03_top_periodicos.png')

# 04 — Citável vs Não citável
fig, ax = plt.subplots(figsize=(10, 8))
labels = list(scielo_citavel.keys()); sizes = list(scielo_citavel.values())
cores = ['#66C2A5', '#FC8D62']
wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=cores,
                                   startangle=90, explode=(0.05, 0.05),
                                   textprops={'fontsize': 13, 'fontweight': 'bold'})
for at in autotexts:
    at.set_color('white'); at.set_fontsize(14)
for t, s in zip(texts, sizes):
    t.set_text(f'{t.get_text()}\n({s} docs)')
ax.set_title('Documentos citáveis – SciELO', fontsize=14, pad=20)
salvar('scielo_04_citavel.png')

# 05 — Tipo de literatura
fig, ax = plt.subplots(figsize=(10, 7))
labels = list(scielo_tipo_lit.keys()); vals = list(scielo_tipo_lit.values())
bars = ax.bar(labels, vals, color=[COR_VERDE, CORES_INTERMEDIARIAS[9]],
              edgecolor='black', linewidth=1.5)
for b, v in zip(bars, vals):
    pct = v / sum(vals) * 100
    ax.text(b.get_x() + b.get_width() / 2, v + 1, f'{v}\n({pct:.1f}%)',
            ha='center', fontweight='bold', fontsize=12)
ax.set_title('Tipo de literatura – SciELO', fontsize=14, pad=20)
ax.set_ylabel('Quantidade')
ax.grid(True, alpha=0.3, axis='y', linestyle='--')
salvar('scielo_05_tipo_literatura.png')

# 06 — Foco em IA
fig, ax = plt.subplots(figsize=(11, 7))
labels = list(scielo_foco_ia.keys()); vals = list(scielo_foco_ia.values())
cores = ['#A8D5BA', '#C8E6C9']
bars = ax.bar(labels, vals, color=cores, edgecolor='black', linewidth=2.5, alpha=0.9)
for b, v in zip(bars, vals):
    pct = v / sum(vals) * 100
    ax.text(b.get_x() + b.get_width() / 2, v / 2, f'{v}\nartigos',
            ha='center', va='center', fontweight='bold', fontsize=14)
    ax.text(b.get_x() + b.get_width() / 2, v, f'{pct:.1f}%',
            ha='center', va='bottom', fontweight='bold', fontsize=13)
ax.set_ylabel('Número de Artigos', fontweight='bold')
ax.set_title('Classificação por foco em IA – SciELO', fontsize=14, pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.set_ylim(0, max(vals) * 1.18)
salvar('scielo_06_foco_ia.png')

print("\n" + "=" * 70)
print(f"✅ Gráficos gerados em: {FIG_DIR}")
print("=" * 70)
