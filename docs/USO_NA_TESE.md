# Uso deste repositório na tese

Documento gerado em 09/10/2026 a partir da leitura dos arquivos `ex_cap*.tex` do repositório da tese (`julianehelanski/tecno-etnografia-centro-ia`, commit 3f0f671 (2026-10-08)). Repositório descrito: `julianehelanski/bibliometria-ia-humanas`. A versão tabular está em `docs/uso_na_tese.csv`.

## Onde entra na tese

Capítulo 2, seção "A emergência do campo brasileiro de estudos em inteligência artificial nas ciências humanas e sociais" (`sec:emergencia_campo_brasileiro`). As figuras abaixo aparecem nessa seção e as notas de rodapé das figuras remetem a este repositório.

## Como os dados foram usados

O mapeamento combina três bases. (1) Catálogo de Teses e Dissertações da CAPES, dump `BR-CAPES-BTD-2021A2024-2025-12-01` (350.071 trabalhos de 2021 a 2024), classificado por expressões regulares em cinco subcampos (IA em sentido estrito, aprendizado de máquina, aprendizado profundo e redes neurais, modelos de linguagem e IA generativa, tecnologias correlatas), que produzem o corpus de 12.995 trabalhos após a auditoria do falso positivo de `transformer`. (2) SciELO Brasil, via API ArticleMeta, universo de 98.165 artigos de 2021 a 2024 e corpus de 631 artigos. (3) OpenAlex, para a comparação internacional e a taxa interna por país. A coleta inicial por interface web (6 de novembro de 2025; SciELO com 152 artigos, CAPES Humanas com 100 trabalhos, 2013 a 2023) permanece versionada por referência metodológica. O classificador está em `utils.py` e o histórico de decisões em `docs/decisoes_metodologicas.md`.

## Figuras da tese que vêm deste repositório

| Capítulo | Seção da tese | Rótulo | Arquivo no repositório | Script | Estado da cópia na tese |
|---|---|---|---|---|---|
| capítulo 2 | Os estudos sobre inteligência artificial nas ciências humanas e sociai | `fig:capes_subcampos` | `figuras/capes_21_subcampos_distribuicao.png` | figuras_capes_2021_2024.py | cópia na tese idêntica à do repositório |
| capítulo 2 | Os estudos sobre inteligência artificial nas ciências humanas e sociai | `fig:capes_grande_area` | `figuras/capes_11_grande_area_share.png` | figuras_capes_2021_2024.py | cópia na tese idêntica à do repositório |
| capítulo 2 | Os estudos sobre inteligência artificial nas ciências humanas e sociai | `fig:capes_heatmap_keyword` | `figuras/capes_13_heatmap_area_keyword.png` | figuras_capes_2021_2024.py | cópia na tese idêntica à do repositório |
| capítulo 2 | Os estudos sobre inteligência artificial nas ciências humanas e sociai | `fig:capes_heatmap_subcampo` | `figuras/capes_22_heatmap_subcampo_grande_area.png` | figuras_capes_2021_2024.py | cópia na tese idêntica à do repositório |
| capítulo 2 | Os estudos sobre inteligência artificial nas ciências humanas e sociai | `fig:capes_humanas_area` | `figuras/capes_h01_areas_humanas.png` | `analise_capes_humanas.py` | cópia na tese idêntica à do repositório |
| capítulo 2 | Os estudos sobre inteligência artificial nas ciências humanas e sociai | `fig:capes_temporal` | `figuras/capes_h02_temporal_humanas.png` | `analise_capes_humanas.py` | cópia na tese idêntica à do repositório |
| capítulo 2 | Os estudos sobre inteligência artificial nas ciências humanas e sociai | `fig:scielo_subject_area` | `figuras/scielo_11_subject_area_share.png` | figuras_scielo_articlemeta.py | cópia na tese idêntica à do repositório |
| capítulo 2 | Os estudos sobre inteligência artificial nas ciências humanas e sociai | `fig:scielo_subcampos` | `figuras/scielo_21_subcampos_distribuicao.png` | figuras_scielo_articlemeta.py | cópia na tese idêntica à do repositório |
| capítulo 2 | Os estudos sobre inteligência artificial nas ciências humanas e sociai | `fig:comparativo_scielo_capes` | `figuras/comparativo_scielo_capes_2026.png` | `analise_comparativa_2026.py` | cópia na tese idêntica à do repositório |
| capítulo 2 | Os estudos sobre inteligência artificial nas ciências humanas e sociai | `fig:openalex_ranking_paises` | `figuras/openalex_01_ranking_paises.png` | figuras_openalex.py | cópia na tese idêntica à do repositório |
| capítulo 2 | Os estudos sobre inteligência artificial nas ciências humanas e sociai | `fig:openalex_taxa_interna` | `figuras/openalex_02_taxa_interna_paises.png` | figuras_openalex.py | cópia na tese idêntica à do repositório |
| capítulo 2 | Os estudos sobre inteligência artificial nas ciências humanas e sociai | `fig:openalex_brasil_temporal` | `figuras/openalex_03_brasil_temporal.png` | figuras_openalex.py | cópia na tese idêntica à do repositório |
| capítulo 2 | Os estudos sobre inteligência artificial nas ciências humanas e sociai | `fig:openalex_subcampos_3bases` | `figuras/openalex_04_subcampos_3bases.png` | figuras_openalex.py | cópia na tese idêntica à do repositório |

## Material do repositório sem uso direto na tese

Das 105 figuras em `figuras/`, 92 não aparecem em `ex_cap*.tex` (variantes temporais, rankings de instituições, regiões, páginas, entre outras). Permanecem como material de auditoria, e as legendas LaTeX prontas estão em `inventario_figuras_capes.md` e `docs/inventario_figuras_openalex.tex`.

## Dados e direitos

Os dados CAPES são de domínio público (Dados Abertos). Os dumps pesados estão em `dados_capes/` (Git LFS, ver README). Os arquivos `dados_scielo/*universo*.csv` e `scielo_*_ia_subcampos.csv` não são versionados integralmente (ver README); o recorte agregado `scielo_brasil_universo_agregado.csv` é versionado.
