# Análise Bibliométrica: Inteligência Artificial nas Ciências Humanas Brasileiras

Scripts e dados utilizados na análise bibliométrica apresentada no Capítulo 2 da tese de doutorado *Seguindo actantes: uma etnografia da inteligência artificial no Brasil*, defendida no Programa de Pós-Graduação em Antropologia Social (PPGAS) da Universidade de São Paulo (USP).

---

## Contexto da pesquisa

Esta análise bibliométrica mapeia a produção acadêmica brasileira sobre inteligência artificial nas ciências humanas, documentando o caráter emergente desse campo de estudos. Os dados sustentam o argumento de que a Antropologia Social ocupa posição marginal num debate que cresce aceleradamente, e fundamentam o posicionamento desta tese no início dos estudos antropológicos brasileiros sobre inteligência artificial.

A análise combina dois repositórios:

- **SciELO** — Biblioteca Eletrônica Científica Online, para artigos acadêmicos
- **Catálogo de Teses e Dissertações da CAPES** — para produções de pós-graduação

Os dados foram coletados em **6 de novembro de 2025**.

---

## Estrutura do repositório

```
analise_bibliometrica_ia_ciencias_humanas/
│
├── README.md                              ← Este arquivo
│
├── scripts/
│   ├── analise_scielo_ia.py               ← Análise dos artigos SciELO
│   └── analise_capes_ia.py                ← Análise do catálogo CAPES
│
├── dados/
│   ├── scielo/
│   │   ├── export_scielo.ris              ← Exportação RIS do SciELO (não incluída por tamanho)
│   │   ├── scielo_publi_ano.csv           ← Publicações por ano
│   │   ├── scielo_periódicos.csv          ← Distribuição por periódico
│   │   ├── scielo_tipo__literatura.csv    ← Tipo de documento
│   │   └── scielo_citavel_naocitavel.csv  ← Citável vs. não citável
│   │
│   └── capes/
│       ├── catalogo_teses_analise.xlsx           ← Dataset completo CAPES (não incluído por tamanho)
│       └── resultados_detalhados_teses_ia.xlsx   ← Resultados consolidados
│
└── graficos/                              ← Gráficos gerados pelos scripts
```

> **Nota:** Os arquivos de dados brutos (`export_scielo.ris` e `catalogo_teses_analise.xlsx`) não estão incluídos neste repositório por conta do tamanho. As instruções para reprodução da coleta estão na seção [Reprodutibilidade](#reprodutibilidade).

---

## Principais resultados

### SciELO (1983–2025) — 152 artigos

| Indicador | Valor |
|-----------|-------|
| Total de artigos identificados | 152 |
| Período | 1983–2025 |
| Publicados em 2024–2025 | 96 (63,2%) |
| Publicados a partir de 2020 | 136 (89,5%) |
| Tipo predominante | Artigo (136; 89,5%) |
| Citáveis | 140 (92,1%) |

**Periódicos com maior volume:**

| Periódico | Artigos |
|-----------|---------|
| Estudos Avançados | 21 |
| Texto Livre | 16 |
| Filosofia Unisinos | 12 |
| Revista Bioética | 9 |
| Trans/Form/Ação | 9 |
| Educação e Pesquisa | 7 |
| Educação em Revista | 6 |
| Brazilian Journal of Political Economy | 5 |

**Presença da Antropologia:** *Horizontes Antropológicos* contribuiu com 1 artigo; *Sociologia & Antropologia*, com 2. A ausência da Antropologia não é apenas numérica: é estrutural, revelada pelo tipo de veículo em que o campo publicou quando publicou.

---

### CAPES (2013–2023) — 100 teses e dissertações

| Indicador | Valor |
|-----------|-------|
| Total de trabalhos | 100 |
| Período | 2013–2023 |
| Mestrados | 61 (61%) |
| Doutorados | 39 (39%) |
| Foco central em IA | 59 (59%) |
| Foco relacionado | 5 (5%) |
| Outros temas | 36 (36%) |
| Número de áreas | 29 |
| Número de instituições | 48 |
| Crescimento (2013→2023) | 3.000% |
| Concentração nos últimos 3 anos | 81% |

**Distribuição por área de conhecimento (CAPES):**

| Área | Defesas |
|------|---------|
| Educação | 29 |
| Filosofia | 16 |
| Geografia | 11 |
| Sociologia | 5 |
| Psicologia | 4 |
| Ciência Política | 3 |
| **Antropologia Social** | **3** |
| Relações Internacionais | 3 |

> **Nota de normalização:** A categoria "Ciência Política" aparece nos dados brutos com duas grafias distintas (com um e com dois espaços entre palavras), totalizando 5 registros. Os scripts consolidam essas entradas em uma única categoria. O valor 3 na tabela acima refere-se à grafia normalizada; os 2 registros adicionais estão incluídos nos totais gerais.

---

## Nota metodológica sobre a categoria "ciências humanas"

O termo **ciências humanas** segue a taxonomia adotada pelo SciELO e pela CAPES como filtro de busca. Na classificação da CAPES, a grande área *Ciências Humanas* engloba Antropologia, Ciência Política, Educação, Filosofia, Geografia, História, Psicologia e Sociologia. O uso de *ciências sociais* como filtro teria excluído Antropologia e Sociologia, que a CAPES não classifica em *Ciências Sociais Aplicadas* — área reservada a Direito, Comunicação, Economia e Administração, entre outras.

A escolha do filtro foi determinada pela arquitetura taxonômica das bases consultadas, não por uma delimitação disciplinar prévia. Ela revela a interdisciplinaridade constitutiva do tema: a inteligência artificial como objeto de pesquisa nas humanidades aparece distribuída por categorias tão distintas quanto Educação, Filosofia e Sociologia, disciplinas que na CAPES habitam grandes áreas diferentes.

---

## Limitações

- A análise cobre apenas materiais indexados nas fontes escolhidas, excluindo livros, capítulos de livros e anais de congressos — restrição significativa num campo onde parte da produção relevante circula nessas formas.
- A classificação por foco em IA no CAPES foi realizada com base nos títulos dos trabalhos, dado que resumos não são indexados pelo catálogo.
- Os dados do SciELO são dinâmicos: consultas futuras podem apresentar resultados diferentes.
- A ênfase em quantidade em detrimento de qualidade é limitação inerente ao método bibliométrico.

---

## Instalação e uso

### Requisitos

```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

### Script SciELO

```bash
# 1. Ajuste os caminhos no início do script:
BASE_DIR = r'caminho/para/seus/dados'
OUTPUT_DIR = r'caminho/para/resultados'

# 2. Execute:
python analise_scielo_ia.py
```

**Arquivos de entrada necessários:**
- `export_scielo.ris` — exportação RIS do SciELO
- `scielo_publi_ano.csv`
- `scielo_periódicos.csv`
- `scielo_tipo__literatura.csv`
- `scielo_citavel_naocitavel.csv`

**Saídas geradas:**
- Gráficos PNG na pasta `resultados_analise/`
- `relatorio_completo.txt` com lista detalhada de artigos por categoria temática

### Script CAPES

```bash
# 1. Certifique-se de que o arquivo de dados está na mesma pasta:
#    catalogo_teses_analise.xlsx  (aba: "Dados Completos")

# 2. Execute:
python analise_capes_ia.py
```

**Saídas geradas:**
- Gráficos PNG na pasta `graficos/`
- `resultados_detalhados_teses_ia.xlsx` com todas as análises em abas separadas

---

## Reprodutibilidade

### Coleta SciELO

1. Acesse [scielo.org](https://scielo.org)
2. Filtre por **Brasil** > **Ciências Humanas**
3. Busque por `inteligência artificial`
4. Exporte: tabelas CSV personalizadas + arquivo de citação RIS
5. Salve os CSVs gerados pela plataforma (distribuição por ano, periódico, tipo de literatura, citabilidade)

### Coleta CAPES

1. Acesse o [Catálogo de Teses e Dissertações da CAPES](https://catalogodeteses.capes.gov.br)
2. Busque por `inteligência artificial` com filtro de grande área **Ciências Humanas**
3. Use uma ferramenta de extração automatizada (ex: extensão de raspagem de dados para navegador) para exportar os resultados em CSV
4. Importe o CSV, limpe e organize no Excel; salve como `.xlsx` com aba `Dados Completos`

---

## Contribuição da IA generativa

Os scripts Python foram desenvolvidos com auxílio de **Claude** (Anthropic), assistente de inteligência artificial, a partir de especificações metodológicas da pesquisadora. A limpeza, organização e verificação dos dados, bem como a interpretação analítica dos resultados, foram realizadas integralmente pela pesquisadora.

---

## Citação

Se você usar estes scripts ou dados, por favor cite:

```
HELANSKI, Juliane. Análise Bibliométrica: Inteligência Artificial nas Ciências Humanas Brasileiras.
Repositório de dados e scripts. GitHub, 2025.
Disponível em: https://github.com/julianehelanski/analise_bibliometrica_ia_ciencias_humanas
```

A tese completa que contextualiza esta análise:

```
HELANSKI, Juliane. Seguindo actantes: uma etnografia da inteligência artificial no Brasil.
Tese (Doutorado em Antropologia Social) — Programa de Pós-Graduação em Antropologia Social,
Universidade de São Paulo, São Paulo, 2026.
```

---

## Licença

Este repositório está disponível sob a licença [MIT](LICENSE). Os dados coletados do SciELO e da CAPES seguem as políticas de uso de cada plataforma.

---

*Última atualização: novembro de 2025*
