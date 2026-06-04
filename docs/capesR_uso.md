# Análise CAPES de longa duração via pacote `capesR`

Este repositório é predominantemente Python (dump oficial BR-CAPES-BTD
2021–2024). O script **`analise_capes_capesR.R`** acrescenta uma frente
complementar em R, usando o pacote [`capesR`](https://github.com/hugoavmedeiros/capesR)
de Hugo Medeiros, que dá acesso programático ao Catálogo de Teses e
Dissertações da CAPES em **série histórica longa (1987–2024)**.

## Por que usar as duas frentes

| Frente | Cobertura | Campos | Para quê |
|--------|-----------|--------|----------|
| Python (`analise_capes_2021_2024.py`) | 2021–2024 | título, resumo, palavras-chave completos | corpus profundo, subcampos, auditoria |
| R (`analise_capes_capesR.R`) | 1987–2024 | depende do schema do capesR | **longue durée**: quando a IA emerge nas Humanas |

O **regex de identificação de IA é portado de `utils.py`** para manter
coerência metodológica entre as duas frentes.

## Como rodar

```r
# 1. Instalar dependências (uma vez)
install.packages(c("capesR", "dplyr", "stringr", "ggplot2", "readr", "scales"))

# 2. Rodar (na raiz do repositório)
# Rscript analise_capes_capesR.R
```

Na primeira execução o `capesR` baixa os arquivos do OSF para
`dados_capes/capesR_cache/` (não versionado). Para um teste rápido, edite a
variável `ANOS` no topo do script (ex.: `ANOS <- 2018:2024`).

## Saídas

- `dados_capes/capes_capesR_ia_humanas.csv` — corpus auditável IA-Humanas
- `figuras/capes_r01_temporal_ia_humanas.png` — evolução anual 1987–2024
- `figuras/capes_r02_share_ia_humanas.png` — % de IA dentro de Humanas/ano
- `figuras/capes_r03_top_areas_humanas.png` — áreas de Humanas com mais IA
- `figuras/capes_r04_top_ies_humanas.png` — IES com mais teses IA-Humanas

## Notas

- O schema de colunas do `capesR` difere do dump oficial; o script faz
  **detecção defensiva de colunas** (`achar_col`), procurando nomes
  equivalentes (`ano_base`/`AN_BASE`, `titulo`/`NM_PRODUCAO` etc.).
- Se alguma coluna textual (resumo/keywords) não existir no schema do
  capesR, a classificação recai apenas sobre o título — mais conservadora.
