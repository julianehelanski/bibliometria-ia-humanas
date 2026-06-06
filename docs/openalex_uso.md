# Análise OpenAlex — IA nas Humanidades por país e ano

O script **`analise_openalex.py`** acrescenta uma terceira fonte ao projeto, ao
lado de CAPES (teses/dissertações) e SciELO (periódicos). O
[OpenAlex](https://openalex.org) é um catálogo aberto e global (~250M de obras),
o que dá ao trabalho duas coisas que as bases brasileiras não dão:

1. **Recorte internacional** — produção de IA nas Humanidades por país/ano, no
   estilo do gráfico OWID/CSET, mas com o filtro de **área do conhecimento** que
   aquela base não tinha (lá "Field" = subcampo *técnico* da IA, não disciplina).
2. **Interseção IA × Humanidades** de verdade, cruzando o conceito "Artificial
   intelligence" com a classificação por *field* (Scopus/ASJC) do OpenAlex.

A coerência metodológica é garantida porque o script aplica o **mesmo
`classificar_subcampos` de `utils.py`** (IA stricto, ML, DL, LLMs, correlatos)
usado nos pipelines CAPES e SciELO. Os subcampos ficam comparáveis entre as três
bases.

## Por que triangular

| Fonte | Caminho de coleta | Recorte | Para quê |
|-------|-------------------|---------|----------|
| CAPES (`analise_capes*.py`) | dump oficial XLSX | teses/dissertações BR 2021–2024 | corpus nacional de pós-graduação |
| SciELO (`analise_scielo_articlemeta.py`) | API ArticleMeta | periódicos BR de Humanas | corpus nacional de periódicos |
| **OpenAlex (`analise_openalex.py`)** | API REST global | obras IA×Humanidades, qualquer país | **contexto internacional** e validação cruzada |

## Pré-requisitos

```bash
pip install -r requirements.txt   # já inclui requests
```

Informe sempre um e-mail real em `--mailto` (o "polite pool" do OpenAlex evita
throttling). Sem ele a API responde, mas com prioridade menor.

## Como rodar

```bash
# 0) PRIMEIRO confirme o ID do campo "Arts and Humanities" no estado atual da API.
#    A taxonomia do OpenAlex evolui; o default do script (field id 12) PRECISA
#    ser conferido aqui antes de confiar nos números.
python analise_openalex.py --listar-campos --mailto voce@exemplo.com

# 1) Panorama internacional IA×Humanidades por país e ano (rápido, minutos).
#    Usa group_by da API; NÃO baixa obra por obra. Já calcula a taxa interna
#    (IA∩Humanidades / universo de Humanidades), métrica canônica do projeto.
python analise_openalex.py --modo agregado --mailto voce@exemplo.com

# 2) Corpus detalhado de um país, com subcampos (lento, baixa obra por obra).
python analise_openalex.py --modo corpus --pais BR --mailto voce@exemplo.com
```

### Parâmetros úteis

| Flag | Default | Para quê |
|------|---------|----------|
| `--modo` | `agregado` | `agregado` = contagens via group_by; `corpus` = baixa obras e classifica subcampos |
| `--pais` | (global) | código ISO-2 (ex.: `BR`, `US`). No modo agregado, sem país sai também o ranking por país |
| `--ano-inicial` / `--ano-final` | 2016 / 2024 | janela temporal (alinhada ao OWID/CSET) |
| `--humanidades-filtro` | `primary_topic.field.id:12` | recorte de Humanidades — **confirme com `--listar-campos`**. Para incluir Ciências Sociais use OR: `primary_topic.field.id:12\|33` |
| `--ia-filtro` | `concepts.id:C154945302` | conceito "Artificial intelligence" |
| `--listar-campos` | — | lista os IDs de field da API e sai |

## Saídas (em `dados_openalex/`)

| Arquivo | Modo | Conteúdo |
|---------|------|----------|
| `openalex_ia_humanas_por_ano_*.csv` | agregado | IA∩Humanidades por ano + universo de Humanidades + taxa interna |
| `openalex_ia_humanas_por_pais_global.csv` | agregado (global) | mesmas métricas por país, ranqueadas |
| `openalex_ia_humanas_corpus_*.csv` | corpus | uma linha por obra×país, com subcampos (gitignored, regenerável) |
| `openalex_ia_humanas_auditoria_*.xlsx` | corpus | obras únicas para auditoria manual (vai ao repo) |

## Ressalvas metodológicas (declarar na tese)

- **Contagem por país segue a regra do OWID/CSET:** uma obra conta uma vez para
  *cada* país presente nas afiliações dos autores. Para contagem única por obra,
  deduplique por `openalex_id`.
- **Definição de "Humanidades" é uma escolha.** O default usa o *field* "Arts and
  Humanities" do OpenAlex. As Ciências Sociais ficam num *field* separado — se o
  recorte da tese for mais largo (como o "Ciências Humanas" da CAPES, que inclui
  Educação, Geografia, Psicologia etc.), amplie o filtro e declare o critério.
- **Cobertura difere das bases nacionais.** O OpenAlex indexa sobretudo o que tem
  metadados em inglês/internacionais; não substitui CAPES nem SciELO para o
  recorte brasileiro, complementa-os.
- **`primary_topic`** reflete o tópico principal atribuído por modelo do OpenAlex;
  obras multidisciplinares podem ser classificadas em um único *field*.
