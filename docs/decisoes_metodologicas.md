# Decisões metodológicas — fonte única de verdade

Este arquivo trava os números canônicos da análise bibliométrica. Qualquer divergência entre este documento, o README e outros artefatos do repositório indica desatualização **dos outros artefatos**, não deste. **A tese cita os números desta tabela**, e quando refizermos cálculos atualizamos esta página primeiro.

A motivação para este arquivo: durante a sessão de coleta e processamento, vários relatos narrativos contendo somas manuais introduziram erros aritméticos pontuais (por exemplo, "8 artigos antes de 2021" quando o correto é 23; "2020 × 3" quando o correto é 2020 × 17). Os valores que provêm de operações pandas diretas sobre as planilhas se mantiveram corretos. **Regra adotada:** todo número que vai para a tese sai de operação atômica em pandas (ou da própria contagem nas planilhas via Excel), nunca de soma feita em prosa.

Este documento está organizado em quatro blocos: (I) números canônicos CAPES, (II) números canônicos SciELO, (III) comparativo SciELO × CAPES Humanas, (IV) coortes históricas descartadas.

---

## I. CAPES — Catálogo de Teses e Dissertações 2021–2024

### I.1. Coortes

| Coorte | Definição | N |
|---|---|---:|
| **Universo CAPES total** | Dump oficial `BR-CAPES-BTD-2021A2024-2025-12-01`, 4 XLSX concatenados, sem filtro de tema | **350.071** |
| **Corpus IA/ML/DL** | Aplicação de `utils.classificar_foco_ia` ao universo total | **12.995** |
| └ Foco Central | trabalhos com termo de IA stricto, ML, DL ou LLMs | 10.058 |
| └ Correlatos | apenas tecnologias adjacentes (robótica, NLP, big data, automação, visão computacional) ou só sigla "IA" sem co-ocorrência | 2.937 |
| Universo Humanas | Subset onde `NM_GRANDE_AREA_CONHECIMENTO = "CIÊNCIAS HUMANAS"` | 59.976 |
| **Corpus IA-Humanas** | Interseção `corpus IA × grande área Humanas` | **400** |

### I.2. Corpus IA por ano de defesa

| Ano de base | Defesas no campo IA |
|---:|---:|
| 2021 | 2.615 |
| 2022 | 2.997 |
| 2023 | 3.447 |
| 2024 | 3.936 |
| **Total** | **12.995** ✓ |

Crescimento bruto 2021→2024: +50,5%. CAGR aproximado: 14,6% a.a.

### I.3. Corpus IA por grande área (12.995) — com taxa interna

| Grande área | N IA | % do corpus | Universo da grande área | Taxa interna |
|---|---:|---:|---:|---:|
| Ciências Exatas e da Terra | 3.633 | 27,96% | 25.431 | **14,29%** |
| Engenharias | 3.590 | 27,63% | 29.880 | **12,01%** |
| Ciências Sociais Aplicadas | 1.848 | 14,22% | 53.492 | 3,45% |
| Multidisciplinar | 1.632 | 12,56% | 57.231 | 2,85% |
| Ciências Agrárias | 773 | 5,95% | 27.619 | 2,80% |
| Ciências da Saúde | 741 | 5,70% | 55.121 | 1,34% |
| **Ciências Humanas** | **400** | **3,08%** | **59.976** | **0,67%** |
| Ciências Biológicas | 238 | 1,83% | 19.461 | 1,22% |
| Linguística, Letras e Artes | 140 | 1,08% | 21.860 | 0,64% |
| **Soma corpus** | **12.995** ✓ | **100%** | 350.071 | — |

> **Marginalidade em duas leituras:** Humanas é a maior grande área no universo total (17%) mas só 3,08% do corpus IA, e apenas 0,67% das defesas de Humanas tocam o campo — contra 14,29% em Exatas e 12,01% em Engenharias.

### I.4. Corpus IA por grau acadêmico

| Grau | Defesas | % do corpus |
|---|---:|---:|
| Mestrado | 7.153 | 55,04% |
| Doutorado | 3.925 | 30,20% |
| Mestrado Profissional | 1.874 | 14,42% |
| Doutorado Profissional | 43 | 0,33% |
| **Total** | **12.995** ✓ | 100% |

### I.5. Corpus IA por subcampo (multi-label; soma > 100%)

| Subcampo | Defesas | % do corpus |
|---|---:|---:|
| Aprendizado de máquina (ML) | 5.284 | 40,66% |
| Tecnologias correlatas | 4.972 | 38,26% |
| Aprendizado profundo & redes neurais | 4.326 | 33,29% |
| IA em sentido estrito | 3.821 | 29,40% |
| Modelos de linguagem & IA generativa | 506 | 3,89% |

> **Achado:** ML supera IA stricta em volume (5.284 vs 3.821). LLMs é o menor dos cinco (506) após a correção do regex `transformer` — antes da correção, era 876, inflado por falsos positivos de "transformer" no sentido literal (transformador elétrico, "social transformer" em textos não-técnicos).

### I.6. CAPES IA-Humanas (400) — duas taxonomias

A CAPES opera com **duas classificações distintas** que precisam ser declaradas. O `XLSX` traz ambas como colunas (`NM_AREA_CONHECIMENTO` e `NM_AREA_AVALIACAO`). Os números abaixo são lidos diretamente da planilha; em ambas as colunas a soma fecha em 400.

**Por área de conhecimento (NM_AREA_CONHECIMENTO):**

| Área de conhecimento | Defesas | % de IA-Humanas |
|---|---:|---:|
| Educação | 154 | 38,50% |
| Geografia | 64 | 16,00% |
| Psicologia | 56 | 14,00% |
| Ciência Política | 40 | 10,00% |
| Filosofia | 39 | 9,75% |
| Sociologia | 25 | 6,25% |
| História | 12 | 3,00% |
| **Antropologia** | **4** | **1,00%** |
| Teologia | 4 | 1,00% |
| Arqueologia | 2 | 0,50% |
| **Soma** | **400** ✓ | 100% |

**Por área de avaliação (NM_AREA_AVALIACAO — taxonomia administrativa da CAPES):**

| Área de avaliação CAPES | Defesas |
|---|---:|
| Educação | 154 |
| Geografia | 64 |
| Psicologia | 56 |
| Ciência Política e Relações Internacionais | 40 |
| Filosofia | 39 |
| Sociologia | 25 |
| História | 12 |
| **Antropologia / Arqueologia** | **6** |
| Ciências da Religião e Teologia | 4 |
| **Soma** | **400** ✓ |

**Diferenças entre as duas taxonomias:**

| Área de conhecimento | Área de avaliação | Mudança |
|---|---|---|
| Antropologia (4) + Arqueologia (2) | **Antropologia / Arqueologia (6)** | **Agrupamento** (CAPES une as duas no organograma de programas) |
| Ciência Política (40) | Ciência Política e Relações Internacionais (40) | Mesmo número, nome ampliado |
| Teologia (4) | Ciências da Religião e Teologia (4) | Mesmo número, nome ampliado |
| Educação, Geografia, Psicologia, Filosofia, Sociologia, História | (idem) | Nome idêntico |

### I.6.1. Implicação para a tese — Antropologia 4 ou 6?

A tese pode dizer qualquer um dos dois números, **desde que declare o critério**:

- "**4 defesas em Antropologia**, segundo a área de conhecimento (NM_AREA_CONHECIMENTO) da CAPES" → recorte estrito da disciplina antropológica.
- "**6 defesas na área de avaliação Antropologia / Arqueologia**, segundo o organograma administrativo da CAPES (NM_AREA_AVALIACAO)" → recorte institucional, que reflete como os programas de pós-graduação são, de fato, organizados pela agência.

A recomendação para o texto é **declarar ambos**:

> "A área de Antropologia registra **4 defesas sobre IA** em 2021–2024 (área de conhecimento); na taxonomia de avaliação da CAPES, que agrupa Antropologia e Arqueologia em uma única área administrativa, são **6 defesas**. Ambos os recortes apontam para presença muito baixa frente a Educação (154) ou Geografia (64) — a marginalidade do tema na Antropologia brasileira independe do critério taxonômico adotado."

Essa formulação blinda a tese contra a arguição "4 pela área de conhecimento ou 6 pela área de avaliação?", e mostra domínio das duas chaves de classificação.

### I.6.2. Implicação para Teologia e Ciência Política

- **Teologia** mantém 4 defesas em ambas as colunas, mas o nome oficial CAPES (que entrará na tese se o critério for área de avaliação) é **"Ciências da Religião e Teologia"**, não apenas "Teologia".
- **Ciência Política** mantém 40 defesas em ambas as colunas, mas o nome oficial é **"Ciência Política e Relações Internacionais"**. Essa é a denominação que aparece em currículos Lattes, comitês de avaliação e portarias da CAPES.

Decisão recomendada: **na narrativa da tese, usar os nomes da NM_AREA_AVALIACAO** (que são os formalmente reconhecidos pela CAPES), com a especificação entre parênteses quando relevante.

### I.7. CAPES IA-Humanas — top 10 IES e regiões

**Top 10 IES** (de 400):
UnB (29), USP (26), UFRJ (17), UFMG (12), UFC (12), UFRN (11), UNICAMP (10), UFPE (8), UFRGS (8), UFF (8).

**Distribuição regional** (de 400):
Sudeste 183 (45,75%), Sul 84 (21,00%), Nordeste 71 (17,75%), Centro-Oeste 55 (13,75%), Norte 7 (1,75%).

### I.8. Fonte dos números

- Universo total: contagem de linhas dos 4 XLSX `dados_capes/2021-2024/br-capes-btd-*.xlsx` (Git LFS).
- Universo por grande área: `dados_capes/capes_2021_2024_universo_por_grande_area.csv` (cache leve gerado pelo `figuras_capes_2021_2024.py` ao percorrer os 4 XLSX uma vez).
- Corpus IA (12.995) e detalhamentos: `dados_capes/capes_2021_2024_ia_auditoria.xlsx`.
- Subset IA-Humanas (400) e detalhamentos: `dados_capes/capes_2021_2024_ia_humanas_completo.xlsx`.

---

## II. SciELO — coleção Brasil 2021–2024 via API ArticleMeta

### II.1. Coortes

| Coorte | Definição | N |
|---|---|---:|
| Universo SciELO bruto | Todos os artigos da coleta API com `from=2021-01-01 & until=2024-12-31`. Filtro from/until opera sobre `processing_date` (data de indexação no SciELO), não sobre `publication_date` | 98.165 |
| **Universo SciELO do recorte** | Universo restrito a `ano de publicação` 2021–2024 (denominador correto da taxa interna) | **90.360** |
| Corpus IA bruto (`scielo_brasil_ia_subcampos_auditoria.xlsx`) | Subset de IA do universo bruto, sem filtro de ano | 659 |
| **Corpus IA recorte estrito** | Subset IA restrito a `ano de publicação` 2021–2024 | **631** |
| └ Foco Central | 502 |
| └ Correlatos | 129 |
| **Human Sciences puro** | Recorte estrito + `subject_areas_periodico` exatamente igual a "Human Sciences" (sem multi-área) | **72** |

> **Nota sobre o filtro temporal da API:** dos 659 artigos brutos, 28 caem fora da janela de publicação. Eles entram no resultado porque a API filtra `processing_date` (indexação), não `publication_date`. Esses 28 são descartados em todas as análises da tese.

### II.2. Decomposição verificada dos 28 stragglers

| Ano de publicação | Artigos | Subtotal |
|---|---:|---|
| 1986 | 1 | |
| 1990 | 1 | |
| 1992 | 1 | |
| 2004 | 1 | |
| 2019 | 2 | |
| 2020 | 17 | **pré-2021: 23** |
| 2025 | 5 | **pós-2024: 5** |
| **Total fora da janela** | **28** ✓ | |

Soma: 23 + 5 = 28; 28 + 631 = 659 ✓.

### II.3. Corpus IA SciELO recorte (631) por ano de publicação

| Ano | Artigos |
|---:|---:|
| 2021 | 107 |
| 2022 | 145 |
| 2023 | 154 |
| 2024 | 225 |
| **Total** | **631** ✓ |

Crescimento bruto 2021→2024: +110%. CAGR aproximado: 28% a.a. (ritmo mais acelerado que o do CAPES, refletindo ciclo editorial mais curto dos periódicos vs ciclo longo das defesas).

### II.4. SciELO recorte 631 — distribuição por subject_area, com taxa interna

| Subject area | N IA | % do corpus | Universo do recorte | Taxa interna |
|---|---:|---:|---:|---:|
| Health Sciences | 200 | 31,70% | 35.704 | 0,56% |
| Agricultural Sciences | 98 | 15,53% | 9.810 | 1,00% |
| Multidisciplinar (*sintética*) | 84 | 13,31% | 10.163 | 0,83% |
| Engineering | 78 | 12,36% | 4.551 | **1,71%** |
| **Human Sciences** | **72** | **11,41%** | **14.806** | **0,49%** |
| Applied Social Sciences | 66 | 10,46% | 6.100 | 1,08% |
| Exact and Earth Sciences | 25 | 3,96% | 2.032 | 1,23% |
| Biological Sciences | 5 | 0,79% | 4.598 | 0,11% |
| Linguistics, Letters and Arts | 3 | 0,48% | 2.596 | 0,12% |
| **Soma** | **631** ✓ | 100% | **90.360** | — |

Taxa SciELO geral: 631/90.360 = 0,70%.

> **Atenção terminológica:** SciELO tem **8 subject_areas canônicas**. "Multidisciplinar" não é uma — é bucket sintético do nosso pipeline para periódicos cujo `subject_areas_periodico` lista mais de uma área. **Não dizer "9 subject_areas" na tese.** Formulação precisa: "as 8 subject_areas do SciELO, mais uma categoria 'Multidisciplinar' para periódicos com classificação múltipla".

> **Atenção ao denominador:** as taxas internas acima usam o universo do recorte estrito 2021–2024 (90.360), NÃO o universo bruto da coleta (98.165). Numerador e denominador são apples-to-apples.

### II.5. SciELO recorte 631 — distribuição por subcampo (multi-label; soma > 100%)

| Subcampo | Artigos | % do corpus |
|---|---:|---:|
| IA em sentido estrito | 187 | 29,64% |
| Aprendizado profundo & redes neurais | 158 | 25,04% |
| Tecnologias correlatas | 140 | 22,19% |
| Aprendizado de máquina (ML) | 138 | 21,87% |
| Modelos de linguagem & IA generativa | 45 | 7,13% |

> **Comparação com CAPES (bloco I.5):** o SciELO inverte a hierarquia. No CAPES, ML lidera (40,66%) e IA stricto é o quarto (29,40%); no SciELO, IA stricto lidera (29,64%) e ML é o quarto (21,87%). Padrão coerente com a tese de que periódicos publicam mais "IA como conceito" e defesas trabalham mais com técnica aplicada.

### II.6. SciELO Human Sciences puro (72) — top 10 periódicos

Subset que vai para o comparativo SciELO × CAPES.

| Periódico | Artigos |
|---|---:|
| Estudos Avançados | 13 |
| Trans/Form/Ação | 9 |
| Filosofia Unisinos | 6 |
| Revista Brasileira de Ensino de Física | 6 |
| Ciência & Educação (Bauru) | 5 |
| Psicologia: Reflexão e Crítica | 3 |
| **Mana** | **3** |
| Educação em Revista | 3 |
| Mercator (Fortaleza) | 2 |
| Revista Brasileira de Inovação | 2 |

> **Achado para a Antropologia:** dos **3 artigos publicados em Mana** (periódico antropológico de referência do PPGAS-MN/UFRJ), **todos são de 2024** e **todos tocam o tema via big data** (subcampo Correlatos), não via IA stricta. Títulos: "Reflexões sobre big data, sexualidades, datificação e moralidades no pornô digital"; "Quem Precisa de Big Data?: sobre dados e informação na agricultura de precisão"; "Big Data: Modos de fazer, comparar e governar". A Antropologia, quando entra na conversa nos periódicos, entra pela porta dos correlatos (não pela IA stricto sensu) e em 2024 (recente). Isso fortalece o argumento da tese sobre a emergência tardia e tematicamente desviada do tema no campo antropológico.

### II.7. Fonte dos números

- Universo bruto e recorte: `dados_scielo/scielo_brasil_ia_subcampos_auditoria.xlsx` (659 linhas brutas, 631 no recorte).
- Universo por subject_area (recorte): `dados_scielo/scielo_brasil_universo_agregado.csv` (90.360 totalizados).
- Cache completo da coleta: `dados_scielo/cache_articlemeta/` (~98k JSONs, gitignored).

---

## III. Comparativo SciELO Human Sciences puro × CAPES Humanas

Único cruzamento direto na tese. Paridade real apples-to-apples: SciELO restrito a `subject_area = "Human Sciences"` puro (sem multi-área) contra CAPES grande área "Ciências Humanas". Tabela completa em `tabelas_comparativas_2026.md`.

| Indicador | SciELO Human Sciences | CAPES Humanas |
|---|---:|---:|
| Total no campo IA/ML/DL | 72 | 400 |
| Foco Central | 52 | 234 |
| Correlatos | 20 | 166 |
| Universo (denominador) | 14.806 | 59.976 |
| **Taxa interna** | **0,49%** | **0,67%** |
| Crescimento 2021→2024 | 16 → 34 (+113%) | 69 → 142 (+106%) |

> **Não confundir** com a taxa SciELO geral (0,70%), que se refere ao universo SciELO total 631/90.360, não ao recorte Human Sciences puro.

---

## IV. Coortes históricas (NÃO usar como fonte para a tese)

Estas coortes foram superadas durante o trabalho. **Persistem no repositório** por reprodutibilidade do processo, **não como evidência válida**.

| Coorte | N | Status |
|---|---:|---|
| SciELO 1983–2025 (coleta web inicial) | 152 | Substituída pela coleta API. |
| SciELO recorte 3 áreas-alvo (coleta intermediária) | 179 (estrito) / 188 (bruto) | Substituída pelo universo Brasil completo 631 e pelo Human Sciences puro 72. |
| CAPES 2013–2023 web inicial | 100 | Substituída pelo dump oficial 2021–2024 = 12.995. |
| CAPES IA total ANTES da correção `transformer` | 13.336 | Substituída por **12.995** (pós-correção do regex). |
| LLM CAPES antes da correção `transformer` | 876 | Substituído por **506**. |
| Health Sciences (SciELO) na coorte bruta 659 | 207 | Na coorte estrita 631: **200**. |
| Human Sciences (SciELO) na coorte bruta 659 | 74 | Na coorte estrita 631: **72**. |
| CAPES Humanas ANTES da correção `transformer` | 441 | Substituída por **400**. |
| Top IES CAPES Humanas antes da correção | UnB 30, USP 27, UFRJ 18 | Após correção: UnB 29, USP 26, UFRJ 17. |
| Sudeste 200 / Sul 96 / NE 79 (CAPES, antes) | — | Após correção: 183 / 84 / 71. |
| Crescimento CAPES 2.716 → 4.020 (coorte 13.336) | — | Coorte atual: **2.615 → 3.936**. |

---

## V. Como atualizar este arquivo

1. Quando refizer uma coleta ou um recorte, ATUALIZE este arquivo **antes** de mudar o README ou qualquer figura.
2. Para cada número novo, anote a coorte, o XLSX/CSV fonte, e a operação pandas que o produziu.
3. Faça um commit dedicado ("decisoes_metodologicas: atualiza N para Y após verificação de X") — não junte com mudança de figura ou texto.
4. Em seguida, sincronize README, inventário e tabelas para citar deste arquivo.
5. **Regra de método:** todo número desta página sai de operação atômica em pandas (`len`, `value_counts`, `groupby().size()`, divisão direta), nunca de soma feita em prosa.

*Última verificação completa: 23 de maio de 2026 — auditoria cruzada de `capes_2021_2024_ia_auditoria.xlsx`, `capes_2021_2024_ia_humanas_completo.xlsx`, `capes_2021_2024_universo_por_grande_area.csv`, `scielo_brasil_ia_subcampos_auditoria.xlsx` e `scielo_brasil_universo_agregado.csv`. Todos os números acima foram lidos via pandas diretamente das fontes primárias, não inferidos. Bloco I.6 expandido com a distinção entre NM_AREA_CONHECIMENTO (taxonomia disciplinar) e NM_AREA_AVALIACAO (taxonomia administrativa CAPES), que afeta especialmente a contagem de Antropologia (4 vs 6).*
