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
├── README.md                       ← Este arquivo
├── LICENSE                         ← Licença MIT
├── CITATION.cff                    ← Metadados de citação (lido pelo GitHub)
├── requirements.txt                ← Dependências Python
│
├── utils.py                        ← Estilo, paleta e regex IA compartilhados
├── analise_scielo.py               ← Análise dos artigos SciELO
├── analise_capes.py                ← Análise do catálogo CAPES
├── analise_comparativa.py          ← Figura e tabelas comparativas SciELO × CAPES
├── gerar_graficos_figuras.py       ← Geração complementar de figuras
├── tabelas_comparativas.md         ← Tabelas em Markdown geradas pelo script comparativo
│
├── dados_scielo/                   ← Arquivos de entrada/saída SciELO
│   ├── export_scielo.ris               (não versionado — ver Reprodutibilidade)
│   ├── scielo_*.csv                    (não versionado)
│   ├── resultados_detalhados_scielo.xlsx
│   ├── relatorio_completo.txt          (gerado pelo script)
│   └── auditoria_foco_ia.csv           (gerado pelo script)
│
├── dados_capes/                    ← Arquivos de entrada/saída CAPES
│   ├── catalogo_teses_analise.xlsx     (não versionado — ver Reprodutibilidade)
│   └── resultados_detalhados_capes.xlsx
│
└── figuras/                        ← Gráficos PNG gerados pelos scripts
```

> **Nota:** Os arquivos de dados brutos (`export_scielo.ris` e `catalogo_teses_analise.xlsx`) não estão incluídos por conta do tamanho e das políticas de uso de cada plataforma. Instruções para reprodução da coleta estão em [Reprodutibilidade](#reprodutibilidade).

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
| Crescimento bruto (2013→2023) | 3.000% |
| CAGR (taxa anual composta) | ~41% a.a. |
| Concentração nos últimos 3 anos | 81% |

> **Por que reportar CAGR junto com crescimento bruto?** Um salto de 1 para 30 publicações representa 3.000% — número impressionante mas hiperinflado pelo denominador pequeno. A taxa anual composta (CAGR) descreve o mesmo crescimento de forma menos enganosa para comparação com outras séries.

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

## Nota metodológica sobre a classificação de foco em IA

Os scripts classificam cada trabalho em três categorias — **IA Foco Central**, **IA Foco Relacionado**, **Outros Temas** — usando expressões regulares com fronteiras de palavra (`\b`) para reduzir falsos positivos. A função compartilhada está em `utils.classificar_foco_ia`.

- **Foco Central:** o texto menciona explicitamente IA, inteligência artificial, machine learning, deep learning, redes neurais, ChatGPT, GPT, LLM ou algoritmos.
- **Foco Relacionado:** menciona apenas termos vizinhos — transhumanismo, robótica, automação, mineração de dados, big data, visão computacional, NLP.
- **Outros Temas:** não menciona nenhum desses termos.

Para fins de auditoria, ambos os scripts geram uma planilha/CSV com a classificação atribuída a cada registro (`Auditoria Foco IA` em `dados_capes/resultados_detalhados_capes.xlsx`, e `dados_scielo/auditoria_foco_ia.csv` para o SciELO). Isso permite revisão humana caso a caso.

---

## Limitações

- A análise cobre apenas materiais indexados nas fontes escolhidas, excluindo livros, capítulos de livros e anais de congressos — restrição significativa num campo onde parte da produção relevante circula nessas formas.
- A classificação por foco em IA no CAPES foi realizada primariamente com base nos títulos; quando a coluna `resumo` está presente, ela também é considerada.
- Os dados do SciELO são dinâmicos: consultas futuras podem apresentar resultados diferentes.
- A ênfase em quantidade em detrimento de qualidade é limitação inerente ao método bibliométrico.
- O crescimento bruto entre 2013 e 2023 (3.000%) é matematicamente sensível à base muito pequena do ano inicial. A coexistência com o CAGR mitiga essa distorção.

---

## Instalação e uso

### Requisitos

```bash
pip install -r requirements.txt
```

Versões fixadas em `requirements.txt`: `pandas`, `numpy`, `matplotlib`, `seaborn`, `openpyxl`.

### Script CAPES

1. Coloque o arquivo de dados em `dados_capes/`:
   - `catalogo_teses_analise.xlsx` (aba `Dados Completos`), **ou**
   - um dos nomes alternativos suportados: `catalogo_teses_analise__2_.xlsx`, `catalogo_teses_limpo__2_.csv`, `catalogodeteses__4_.csv`.

2. Execute:
   ```bash
   python analise_capes.py
   ```

3. Saídas:
   - Gráficos PNG em `figuras/`
   - Planilha consolidada em `dados_capes/resultados_detalhados_capes.xlsx` (inclui aba `Auditoria Foco IA`, `Top Termos`, `Top Bigrams`)

### Script SciELO

1. Coloque os arquivos em `dados_scielo/`:
   - `export_scielo.ris`
   - `scielo_publi_ano.csv`
   - `scielo_periódicos.csv`
   - `scielo_tipo__literatura.csv`
   - `scielo_citavel_naocitavel.csv`
   - `scielo_areas_tematicas.csv`
   - `scielo_indice_citacoes.csv`

2. Execute:
   ```bash
   python analise_scielo.py
   ```

3. Saídas:
   - Gráficos PNG em `figuras/`
   - `dados_scielo/relatorio_completo.txt` (lista detalhada por categoria temática)
   - `dados_scielo/auditoria_foco_ia.csv` (classificação por artigo)

### Análise comparativa SciELO × CAPES

Depois de rodar os dois scripts acima, gere a figura e as tabelas comparativas:

```bash
python analise_comparativa.py
```

Saídas:
- `figuras/comparativo_scielo_capes.png` e `.svg` — uma única figura com 4 painéis: evolução temporal sobreposta, concentração nos últimos anos, top 10 áreas (CAPES) e top 10 periódicos (SciELO).
- `tabelas_comparativas.md` — tabelas Markdown: sumário comparativo, publicações por ano (ambas as bases lado a lado), top 10 áreas CAPES, top 10 periódicos SciELO.
- `tabela_sumario.csv` e `tabela_publicacoes_por_ano.csv` — versões CSV.

O script aplica também a consolidação de "Ciência Política" (duas grafias com espaçamento diferente nos dados brutos).

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
3. Use uma ferramenta de extração automatizada (ex.: extensão de raspagem de dados para navegador) para exportar os resultados em CSV
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

O arquivo [`CITATION.cff`](CITATION.cff) também é fornecido para citação automatizada pelo GitHub.

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
