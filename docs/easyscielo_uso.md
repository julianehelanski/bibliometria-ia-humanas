# Análise SciELO via pacote `easyScieloPack`

O script **`analise_scielo_easyscielo.R`** acrescenta uma frente em R que usa o
pacote [`easyScieloPack`](https://github.com/Programa-ISA/easyScieloPack)
(Programa-ISA / Pablo Ixcamparij) para buscar artigos na interface de pesquisa
do SciELO. É uma frente de **triangulação** do pipeline Python
`analise_scielo_articlemeta.py`.

## Por que triangular

| Frente | Caminho de coleta | Recorte | Para quê |
|--------|-------------------|---------|----------|
| Python (`analise_scielo_articlemeta.py`) | API oficial ArticleMeta (periódico → PID → artigo) | periódicos de Humanas, com `subject_areas` | corpus principal, subcampos, auditoria |
| R (`analise_scielo_easyscielo.R`) | scraping da busca do SciELO (`search_scielo`) | busca por termos de IA na coleção Brasil | **validação cruzada** da tendência temporal |

Dois caminhos independentes sobre a mesma base: se convergem na tendência da
IA, o achado fica mais robusto. O **regex de IA e os subcampos são portados de
`utils.py`** — mesmo critério dos dois lados.

## Como rodar

```r
# 1. Instalar (uma vez)
install.packages(c("remotes","dplyr","stringr","ggplot2","readr","tidyr"))
remotes::install_github("Programa-ISA/easyScieloPack")

# 2. Rodar (na raiz do repositório)
# Rscript analise_scielo_easyscielo.R
```

## Saídas

- `dados_scielo/scielo_easyscielo_ia.csv` — corpus auditável IA
- `figuras/scielo_es01_temporal_ia.png` — evolução anual por foco
- `figuras/scielo_es02_subcampos.png` — distribuição por subcampo
- `figuras/scielo_es03_top_termos.png` — termos mais frequentes
- `figuras/scielo_es04_acumulado.png` — crescimento acumulado

## Limitações importantes (do próprio pacote)

- `search_scielo` retorna **apenas 5 campos**: `title`, `authors`, `year`,
  `doi`, `abstract`. **Não** traz periódico, área temática nem idioma — por isso
  as figuras se apoiam em ano + texto, e o recorte de Humanas, se desejado,
  precisa ser feito **server-side** pelo filtro `categories` (variável
  `CATEGORIAS_HUMANAS` no topo do script; deixei `NULL` por padrão).
- **Cada filtro aceita um único valor por consulta.** Por isso o script itera
  termo a termo (`TERMOS_BUSCA`) e depois deduplica por DOI/título.
- O SciELO pode bloquear scraping intensivo (**erro 403**). Há pausa de 3 s
  entre chamadas (`PAUSA_SEG`); aumente se necessário.
- Para teste rápido, reduza `TERMOS_BUSCA` e/ou `ANO_INICIO`/`ANO_FIM`.

## Conferir convergência com a frente Python

Depois de rodar as duas, compare as séries temporais:
`dados_scielo/scielo_easyscielo_ia.csv` (R) vs `dados_scielo/scielo_ia_subcampos.csv`
(Python). A tendência de crescimento deve ser semelhante mesmo com volumes
absolutos diferentes (caminhos de coleta distintos).
