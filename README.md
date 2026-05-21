# Análise Bibliométrica: Inteligência Artificial nas Ciências Humanas Brasileiras

Scripts e dados utilizados na análise bibliométrica apresentada no Capítulo 2 da tese de doutorado *Seguindo actantes: uma etnografia da inteligência artificial no Brasil*, defendida no Programa de Pós-Graduação em Antropologia Social (PPGAS) da Universidade de São Paulo (USP).

---

## Contexto da pesquisa

Esta análise bibliométrica mapeia a produção acadêmica brasileira sobre inteligência artificial nas ciências humanas, documentando o caráter emergente desse campo de estudos. Os dados sustentam o argumento de que a Antropologia Social ocupa posição marginal num debate que cresce aceleradamente, e fundamentam o posicionamento desta tese no início dos estudos antropológicos brasileiros sobre inteligência artificial.

A análise combina dois repositórios:

- **SciELO** — Biblioteca Eletrônica Científica Online, para artigos acadêmicos
- **Catálogo de Teses e Dissertações da CAPES** — para produções de pós-graduação

A coleta foi realizada em dois momentos:

- **6 de novembro de 2025** — coleta inicial via SciELO e Catálogo de Teses e Dissertações da CAPES (interface web), com filtro de grande área "Ciências Humanas". Esta coleta resultou na análise SciELO (152 artigos) e na análise CAPES restrita às Humanas (100 trabalhos, 2013–2023).
- **20 de maio de 2026** — expansão da análise CAPES para o dump oficial completo no portal de Dados Abertos da CAPES (`BR-CAPES-BTD-2021A2024-2025-12-01`, versão 3.0), cobrindo **todas as grandes áreas** do conhecimento e o quadriênio 2021–2024 (350.071 registros no universo, 13.336 trabalhos sobre IA identificados pelo classificador refinado). A virada metodológica permite situar a marginalidade das humanidades dentro do mapa mais amplo da produção brasileira sobre IA.

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
├── analise_capes.py                ← Análise CAPES (coleta inicial, 2013–2023)
├── analise_capes_2021_2024.py      ← Análise CAPES (dump oficial 2021–2024, todas as áreas)
├── analise_capes_humanas.py        ← Zoom IA em Ciências Humanas (subset do dump 2021–2024)
├── figuras_capes_2021_2024.py      ← Geração das 10 figuras da análise expandida
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
│   ├── br-capes-btd-*.xlsx             (dump oficial 2021–2024, 4 arquivos, via Git LFS)
│   ├── metadados-catalogo-de-teses-e-dissertacoes.PDF  (dicionário de dados oficial)
│   ├── resultados_detalhados_capes.xlsx        (análise antiga, 2013–2023)
│   ├── capes_2021_2024_ia.csv          (gerado pelo script, no .gitignore — 64 MB)
│   └── capes_2021_2024_ia_auditoria.xlsx       (versão slim para auditoria, 2,9 MB)
│
└── figuras/                        ← Gráficos PNG gerados pelos scripts
    ├── capes_01a..10*.png              (análise antiga, 2013–2023)
    ├── capes_11..20*.png               (análise expandida, 2021–2024)
    ├── capes_h01..h05*.png             (zoom em Ciências Humanas)
    ├── scielo_*.png                    (análise SciELO)
    └── comparativo_scielo_capes.*      (comparativo)
```

> **Nota:** Os arquivos `export_scielo.ris` (SciELO) e os 4 XLSX do dump CAPES não cabem confortavelmente em git padrão. O dump CAPES é versionado via **Git LFS**; o export SciELO segue a política de coleta caso a caso. Instruções de reprodução em [Reprodutibilidade](#reprodutibilidade).

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

### CAPES (2021–2024, todas as áreas) — 13.336 trabalhos sobre IA

Análise baseada no dump oficial `BR-CAPES-BTD-2021A2024-2025-12-01` do portal de Dados Abertos da CAPES. O universo total do dump (350.071 trabalhos de conclusão de pós-graduação stricto sensu) é classificado pelo regex refinado de IA, sem restrição prévia de área.

| Indicador | Valor |
|-----------|-------|
| Universo total (2021–2024) | 350.071 |
| **IA — Foco Central** | **10.412** |
| **IA — Foco Relacionado** | **2.924** |
| **Total IA (Central + Relacionado)** | **13.336 (3,81% do universo)** |
| Mestrado | 7.066 (53%) |
| Doutorado | 4.601 (35%) |
| Mestrado Profissional | 1.629 (12%) |
| Crescimento 2021→2024 (CAGR) | ~14% a.a. (2.716 → 4.020 trabalhos/ano) |

**Distribuição IA por grande área (corpus IA = 13.336):**

| Grande área | IA | % do corpus IA | Total geral | Taxa interna IA |
|-------------|---:|---:|---:|---:|
| Engenharias | 3.818 | 28,6% | 29.880 | **12,8%** |
| Ciências Exatas e da Terra | 3.645 | 27,3% | 25.431 | **14,3%** |
| Ciências Sociais Aplicadas | 1.865 | 14,0% | 53.492 | 3,5% |
| Multidisciplinar | 1.660 | 12,4% | 57.231 | 2,9% |
| Ciências Agrárias | 774 | 5,8% | 27.619 | 2,8% |
| Ciências da Saúde | 747 | 5,6% | 55.121 | 1,4% |
| **Ciências Humanas** | **441** | **3,3%** | **59.976** | **0,7%** |
| Ciências Biológicas | 240 | 1,8% | 19.461 | 1,2% |
| Linguística, Letras e Artes | 146 | 1,1% | 21.860 | 0,7% |

**Marginalidade em duas leituras:** Ciências Humanas é a maior grande área no universo total (17% das defesas), mas só 3,3% do corpus IA, e apenas 0,7% das defesas em Humanas tratam de IA — contra 12,8% em Engenharias e 14,3% em Exatas (diferença de uma ordem de grandeza).

---

### CAPES — Zoom em Ciências Humanas (2021–2024) — 441 trabalhos sobre IA

| Área de conhecimento | Trabalhos | % de IA-Humanas |
|----------------------|---:|---:|
| Educação | 174 | 39,5% |
| Geografia | 71 | 16,1% |
| Psicologia | 59 | 13,4% |
| Filosofia | 43 | 9,8% |
| Ciência Política | 40 | 9,1% |
| Sociologia | 26 | 5,9% |
| História | 16 | 3,6% |
| **Antropologia** | **5** | **1,1%** |
| Teologia | 5 | 1,1% |
| Arqueologia | 2 | 0,5% |

**Top 10 IES em IA-Humanas:** UnB (30), USP (27), UFRJ (18), UFRN (13), UFMG (12), UFC (12), UFRGS (11), UNICAMP (10), UFRRJ (9), UFPE (8).

**Concentração regional:** Sudeste 200 (45,4%), Sul 96 (21,8%), Nordeste 79 (17,9%), Centro-Oeste 59 (13,4%), Norte 7 (1,6%).

**Marginalidade em camadas (confirmação empírica do argumento da tese):**
- IA é marginal em Humanas (0,7% da produção da grande área)
- A Antropologia é marginal dentro do corpus IA-Humanas (1,1% das 441 defesas em IA-Humanas)
- Cinco trabalhos sobre IA em Antropologia em quatro anos — densidade muito baixa frente a Educação (174) ou Geografia (71).

---

### CAPES (2013–2023, coleta inicial restrita a Humanas) — 100 teses e dissertações

A análise inicial cobriu o período 2013–2023 com filtro de grande área aplicado no próprio catálogo web. Os resultados desta análise se mantêm no repositório por referência histórica e metodológica; as figuras correspondentes têm prefixo `capes_01a..10`. Os números abaixo permanecem válidos no recorte mais estreito.


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

### Versão refinada (análise 2021–2024, todas as áreas)

A expansão da análise para todas as grandes áreas exigiu apertar o classificador para evitar falsos positivos massivos em Engenharias, Computação e áreas correlatas. As mudanças em relação à versão anterior:

- **Foco Central — núcleo (alta precisão):** `inteligência artificial`, `artificial intelligence`, `machine learning`, `deep learning`, `aprendizado de máquina`, `aprendizado profundo`, `redes neurais`, `neural networks`, `modelos de linguagem`, `large language models` / `LLM`, `transformer`, `ChatGPT`, `GPT-N`, `IA generativa`, `generative AI`.
- **Sigla `IA` (regra de co-ocorrência):** a sigla `IA` isolada **não é mais suficiente** para classificar como foco central. Ela precisa coocorrer no mesmo texto com termo do núcleo ou da lista relacionada. Isso elimina falsos positivos em "Iniciação Científica", "Imposto Adicional", "Inteligência de Mercado" e nomes próprios.
- **Termo `algoritmo` removido do núcleo:** sem o filtro de área, `algoritmo` capturava praticamente toda a Computação/Engenharia/Estatística. Quem usa apenas `algoritmo` sem outros termos passa a entrar em "Outros Temas" — ajuste necessário para o panorama "todas as áreas".
- **Foco Relacionado:** `transhumanismo`, `pós-humanismo`, `robótica`, `automação`, `mineração de dados`, `big data`, `visão computacional`, `processamento de linguagem natural` / `NLP`.

### Versão original (análise 2013–2023, só Humanas)

Mais inclusiva, justificável pelo recorte estreito de área que já filtrava o ruído computacional. Inclui `algoritmo` e a sigla `IA` sem co-ocorrência. Mantida no histórico do utils como retrocompatibilidade dos scripts antigos.

### Auditoria

Para fins de revisão humana caso a caso, os scripts geram planilhas/CSV com a classificação por registro:
- `dados_capes/capes_2021_2024_ia_auditoria.xlsx` — versão slim (sem resumos integrais) para os 13.336 trabalhos IA da análise expandida.
- `dados_capes/capes_2021_2024_ia.csv` — versão completa (com resumos), regenerável; não versionada.
- `dados_capes/resultados_detalhados_capes.xlsx` — aba `Auditoria Foco IA` da análise antiga.
- `dados_scielo/auditoria_foco_ia.csv` — auditoria do SciELO.

---

## Limitações

- A análise cobre apenas materiais indexados nas fontes escolhidas, excluindo livros, capítulos de livros e anais de congressos — restrição significativa num campo onde parte da produção relevante circula nessas formas.
- A classificação por foco em IA no CAPES expandido considera título + resumo + palavras-chave (campos `NM_PRODUCAO`, `DS_RESUMO`, `DS_PALAVRA_CHAVE`, `DS_ABSTRACT`, `DS_KEYWORD` do dump oficial), reduzindo o viés "só pelo título" da coleta inicial.
- Os dados do SciELO são dinâmicos: consultas futuras podem apresentar resultados diferentes.
- A ênfase em quantidade em detrimento de qualidade é limitação inerente ao método bibliométrico.
- O dump CAPES traz dados consolidados pela Plataforma Sucupira: programas podem reabrir o calendário de envio dentro do quadriênio, gerando pequenas atualizações retroativas. A versão usada nesta análise é a 3.0 publicada em 01/12/2025.
- O crescimento bruto entre 2013 e 2023 (3.000%) é matematicamente sensível à base muito pequena do ano inicial. A coexistência com o CAGR mitiga essa distorção.
- A taxa interna de IA por grande área (Engenharias 12,8%, Humanas 0,7%) depende do regex aplicado. O regex refinado é conservador por desenho: trabalhos de Computação que mencionem só "algoritmo" deixam de ser contados como IA — fronteira deliberada para que "IA" não se confunda com "Computação em geral".

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

### Coleta CAPES — versão 2021–2024 (expandida, recomendada)

1. Acesse o portal de Dados Abertos da CAPES:
   - [Catálogo de Teses e Dissertações – Brasil](https://dadosabertos.capes.gov.br/group/catalogo-de-teses-e-dissertacoes-brasil)
2. Baixe o dataset `[2021 a 2024] Catálogo de Teses e Dissertações da CAPES` em formato XLSX. São 4 arquivos (`br-capes-btd-2021-*.xlsx`, …, `br-capes-btd-2024-*.xlsx`), cerca de 150–200 MB cada.
3. Baixe também o PDF de metadados (`metadados-catalogo-de-teses-e-dissertacoes.PDF`) — é o dicionário oficial das 59 colunas do dump e referência metodológica para citação.
4. Coloque os 4 XLSX + o PDF em `dados_capes/`. Use Git LFS para versionar (ver `.gitattributes`).
5. Execute:
   ```bash
   python analise_capes_2021_2024.py   # gera o subset IA (13k trabalhos)
   python figuras_capes_2021_2024.py   # gera as 10 figuras panorâmicas (capes_11..20)
   python analise_capes_humanas.py     # gera o zoom Humanas (capes_h01..h05)
   ```
   Variável de ambiente opcional `CAPES_DATA_DIR` permite apontar para outro diretório (útil quando o LFS local só tem ponteiros).

### Coleta CAPES — versão 2013–2023 (histórica)

1. Acesse o [Catálogo de Teses e Dissertações da CAPES](https://catalogodeteses.capes.gov.br) (interface web)
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

*Última atualização: 21 de maio de 2026 — expansão para o dump CAPES 2021–2024 (todas as grandes áreas, 13.336 trabalhos sobre IA identificados, dos quais 441 em Ciências Humanas e 5 em Antropologia).*
