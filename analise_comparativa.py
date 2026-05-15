# -*- coding: utf-8 -*-
"""
Análise comparativa SciELO × CAPES.

Lê os XLSX consolidados gerados por `analise_scielo.py` e `analise_capes.py`
e produz:

1. Uma única figura multipainel (`figuras/comparativo_scielo_capes.png` e .svg)
2. Tabelas em Markdown (`tabelas_comparativas.md`) e CSVs auxiliares
   em `dados_scielo/` e `dados_capes/`.

Uso:
    python analise_comparativa.py
"""

import os
import sys
from io import StringIO

import pandas as pd
import matplotlib.pyplot as plt

from utils import (
    BASE_DIR,
    DADOS_CAPES_DIR,
    DADOS_SCIELO_DIR,
    FIGURAS_DIR,
    aplicar_estilo_padrao,
    garantir_diretorio,
)


CAPES_XLSX = os.path.join(DADOS_CAPES_DIR, 'resultados_detalhados_capes.xlsx')
SCIELO_XLSX = os.path.join(DADOS_SCIELO_DIR, 'resultados_detalhados_scielo.xlsx')

# Cores fixas por base, da paleta tab10. Usar as mesmas em todos os painéis
# facilita a leitura.
COR_SCIELO = plt.cm.tab10.colors[0]   # azul
COR_CAPES = plt.cm.tab10.colors[3]    # vermelho


def carregar_dados():
    """Carrega as abas relevantes de cada XLSX. Falha cedo se faltar arquivo."""
    for p in (CAPES_XLSX, SCIELO_XLSX):
        if not os.path.isfile(p):
            print(f"[ERRO] Arquivo não encontrado: {p}")
            print("       Rode antes os scripts analise_scielo.py e analise_capes.py.")
            sys.exit(1)

    capes_areas = pd.read_excel(CAPES_XLSX, sheet_name='Todas as Áreas')
    # Consolida grafias com espaçamento variável ("CIÊNCIA POLÍTICA" vs
    # "CIÊNCIA  POLÍTICA") — problema conhecido nos dados brutos da CAPES,
    # já documentado no README.
    capes_areas['area_normalizada'] = (
        capes_areas['area_normalizada'].astype(str)
        .str.replace(r'\s+', ' ', regex=True)
        .str.strip()
    )
    capes_areas = (capes_areas.groupby('area_normalizada', as_index=False)['Quantidade']
                   .sum()
                   .sort_values('Quantidade', ascending=False))

    capes = {
        'ano': pd.read_excel(CAPES_XLSX, sheet_name='Publicações por Ano'),
        'areas': capes_areas,
        'foco': pd.read_excel(CAPES_XLSX, sheet_name='Foco em IA'),
    }
    scielo = {
        'ano': pd.read_excel(SCIELO_XLSX, sheet_name='Publicações por Ano'),
        'periodicos': pd.read_excel(SCIELO_XLSX, sheet_name='Periódicos'),
        'tipo': pd.read_excel(SCIELO_XLSX, sheet_name='Tipo de Literatura'),
        'citavel': pd.read_excel(SCIELO_XLSX, sheet_name='Citável vs Não Citável'),
    }
    return scielo, capes


def construir_figura(scielo, capes, destino_sem_extensao):
    """Monta uma figura 2x2 com os comparativos. Salva em PNG e SVG."""
    fig, axes = plt.subplots(2, 2, figsize=(13, 10), constrained_layout=True)
    fig.suptitle('Produção brasileira sobre Inteligência Artificial '
                 'nas Ciências Humanas: SciELO × CAPES',
                 fontsize=13)

    # ----- (A) Evolução temporal: ambas as bases sobrepostas -----
    ax = axes[0, 0]
    sc = scielo['ano'].rename(columns={'ano_publicacao': 'ano', 'quantidade': 'n'})
    cp = capes['ano'].rename(columns={'ano_defesa': 'ano', 'quantidade': 'n'})
    sc['ano'] = pd.to_numeric(sc['ano'], errors='coerce')
    cp['ano'] = pd.to_numeric(cp['ano'], errors='coerce')
    sc = sc.dropna().sort_values('ano')
    cp = cp.dropna().sort_values('ano')

    ax.plot(sc['ano'], sc['n'], marker='o', label=f"SciELO (n={int(sc['n'].sum())})",
            color=COR_SCIELO, linewidth=2)
    ax.plot(cp['ano'], cp['n'], marker='s', label=f"CAPES (n={int(cp['n'].sum())})",
            color=COR_CAPES, linewidth=2)
    ax.set_title('A. Evolução temporal das publicações')
    ax.set_xlabel('Ano')
    ax.set_ylabel('Publicações')
    ax.legend(frameon=False)

    # ----- (B) Concentração nos últimos 3 anos (≥2022) -----
    ax = axes[0, 1]
    def pct_recente(df, limite=2022):
        total = df['n'].sum()
        recente = df.loc[df['ano'] >= limite, 'n'].sum()
        return 100 * recente / total if total else 0

    bases = ['SciELO', 'CAPES']
    valores = [pct_recente(sc), pct_recente(cp)]
    cores = [COR_SCIELO, COR_CAPES]
    bars = ax.bar(bases, valores, color=cores, width=0.5)
    for bar, v in zip(bars, valores):
        ax.text(bar.get_x() + bar.get_width() / 2, v, f'{v:.1f}%',
                ha='center', va='bottom', fontsize=10)
    ax.set_title('B. Concentração nos últimos anos (≥ 2022)')
    ax.set_ylabel('% do total da base')
    ax.set_ylim(0, max(valores) * 1.25 if max(valores) > 0 else 1)

    # ----- (C) Top 10 áreas CAPES -----
    ax = axes[1, 0]
    top_areas = capes['areas'].nlargest(10, 'Quantidade').iloc[::-1]
    ax.barh(top_areas['area_normalizada'].astype(str).str.title(),
            top_areas['Quantidade'], color=COR_CAPES)
    for i, v in enumerate(top_areas['Quantidade']):
        ax.text(v, i, f' {int(v)}', va='center', fontsize=9)
    ax.set_title('C. CAPES — Top 10 áreas de conhecimento')
    ax.set_xlabel('Defesas')

    # ----- (D) Top 10 periódicos SciELO -----
    ax = axes[1, 1]
    top_per = scielo['periodicos'].nlargest(10, 'quantidade').iloc[::-1]
    nomes = top_per['periodico'].astype(str).str.slice(0, 45)
    ax.barh(nomes, top_per['quantidade'], color=COR_SCIELO)
    for i, v in enumerate(top_per['quantidade']):
        ax.text(v, i, f' {int(v)}', va='center', fontsize=9)
    ax.set_title('D. SciELO — Top 10 periódicos')
    ax.set_xlabel('Artigos')

    png = destino_sem_extensao + '.png'
    svg = destino_sem_extensao + '.svg'
    fig.savefig(png, dpi=300, bbox_inches='tight')
    fig.savefig(svg, bbox_inches='tight')
    plt.close(fig)
    print(f"  > {png}")
    print(f"  > {svg}")
    return png, svg


def _df_ano_combinada(scielo, capes):
    """Une as séries por ano em uma só tabela, com colunas SciELO/CAPES."""
    sc = scielo['ano'].rename(columns={'ano_publicacao': 'ano', 'quantidade': 'SciELO'})
    cp = capes['ano'].rename(columns={'ano_defesa': 'ano', 'quantidade': 'CAPES'})
    sc['ano'] = pd.to_numeric(sc['ano'], errors='coerce')
    cp['ano'] = pd.to_numeric(cp['ano'], errors='coerce')
    combinada = pd.merge(sc, cp, on='ano', how='outer').sort_values('ano')
    combinada = combinada.fillna(0)
    combinada['SciELO'] = combinada['SciELO'].astype(int)
    combinada['CAPES'] = combinada['CAPES'].astype(int)
    combinada['Total'] = combinada['SciELO'] + combinada['CAPES']
    combinada['ano'] = combinada['ano'].astype(int)
    return combinada


def _df_sumario(scielo, capes):
    """Sumário lado a lado dos números principais."""
    def get(df, ano_col, n_col):
        total = int(df[n_col].sum())
        anos = pd.to_numeric(df[ano_col], errors='coerce').dropna()
        periodo = f"{int(anos.min())}–{int(anos.max())}" if not anos.empty else 'n/d'
        df2 = df.copy()
        df2[ano_col] = pd.to_numeric(df2[ano_col], errors='coerce')
        recente = int(df2.loc[df2[ano_col] >= 2022, n_col].sum())
        pct = 100 * recente / total if total else 0
        return total, periodo, recente, pct

    sc = get(scielo['ano'], 'ano_publicacao', 'quantidade')
    cp = get(capes['ano'], 'ano_defesa', 'quantidade')

    foco_capes = capes['foco'].set_index('foco_ia')['Quantidade']
    top_area_capes = capes['areas'].nlargest(1, 'Quantidade').iloc[0]
    top_periodico = scielo['periodicos'].nlargest(1, 'quantidade').iloc[0]

    return pd.DataFrame({
        'Indicador': [
            'Total de registros',
            'Período coberto',
            'Publicações ≥ 2022',
            '% do total em ≥ 2022',
            'Foco central em IA (CAPES)',
            'Top 1 área / periódico',
        ],
        'SciELO (artigos)': [
            sc[0], sc[1], sc[2], f'{sc[3]:.1f}%',
            '—',
            f"{top_periodico['periodico']} ({int(top_periodico['quantidade'])})",
        ],
        'CAPES (teses/dissertações)': [
            cp[0], cp[1], cp[2], f'{cp[3]:.1f}%',
            f"{int(foco_capes.get('IA - Foco Central', 0))} "
            f"({100 * foco_capes.get('IA - Foco Central', 0) / cp[0]:.1f}%)",
            f"{str(top_area_capes['area_normalizada']).title()} "
            f"({int(top_area_capes['Quantidade'])})",
        ],
    })


def gerar_tabelas(scielo, capes, destino_md):
    """Escreve um documento Markdown com todas as tabelas comparativas."""
    sumario = _df_sumario(scielo, capes)
    serie_ano = _df_ano_combinada(scielo, capes)
    top_areas = capes['areas'].nlargest(10, 'Quantidade').reset_index(drop=True)
    top_areas['area_normalizada'] = top_areas['area_normalizada'].astype(str).str.title()
    top_areas.index = top_areas.index + 1
    top_areas.columns = ['Área', 'Defesas']
    top_periodicos = scielo['periodicos'].nlargest(10, 'quantidade').reset_index(drop=True)
    top_periodicos.index = top_periodicos.index + 1
    top_periodicos.columns = ['Periódico', 'Artigos']

    buf = StringIO()
    buf.write('# Tabelas comparativas SciELO × CAPES\n\n')
    buf.write('Geradas automaticamente por `analise_comparativa.py` a partir '
              'dos XLSX consolidados.\n\n')

    buf.write('## Tabela 1. Sumário comparativo\n\n')
    buf.write(sumario.to_markdown(index=False))
    buf.write('\n\n')

    buf.write('## Tabela 2. Publicações por ano\n\n')
    buf.write(serie_ano.to_markdown(index=False))
    buf.write('\n\n')

    buf.write('## Tabela 3. Top 10 áreas de conhecimento (CAPES)\n\n')
    buf.write(top_areas.to_markdown())
    buf.write('\n\n')

    buf.write('## Tabela 4. Top 10 periódicos (SciELO)\n\n')
    buf.write(top_periodicos.to_markdown())
    buf.write('\n')

    with open(destino_md, 'w', encoding='utf-8') as f:
        f.write(buf.getvalue())
    print(f"  > {destino_md}")

    # Versões CSV individuais, úteis para reutilização.
    serie_ano.to_csv(os.path.join(BASE_DIR, 'tabela_publicacoes_por_ano.csv'), index=False)
    sumario.to_csv(os.path.join(BASE_DIR, 'tabela_sumario.csv'), index=False)
    print(f"  > tabela_publicacoes_por_ano.csv")
    print(f"  > tabela_sumario.csv")


def main():
    aplicar_estilo_padrao()
    garantir_diretorio(FIGURAS_DIR)

    print('Carregando XLSX consolidados...')
    scielo, capes = carregar_dados()

    print('\nGerando figura comparativa...')
    construir_figura(scielo, capes,
                     os.path.join(FIGURAS_DIR, 'comparativo_scielo_capes'))

    print('\nGerando tabelas...')
    gerar_tabelas(scielo, capes, os.path.join(BASE_DIR, 'tabelas_comparativas.md'))

    print('\nConcluído.')


if __name__ == '__main__':
    main()
