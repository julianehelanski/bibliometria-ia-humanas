# Decisões metodológicas — fonte única de verdade

Este arquivo trava os números canônicos da análise bibliométrica. Qualquer divergência entre este documento, o README e outros artefatos do repositório indica desatualização **dos outros artefatos**, não deste. **A tese cita os números desta tabela**, e quando refizermos cálculos atualizamos esta página primeiro.

A motivação para este arquivo: durante a sessão de coleta e processamento, vários relatos narrativos contendo somas manuais introduziram erros aritméticos pontuais (por exemplo, "8 artigos antes de 2021" quando o correto é 23; "2020 × 3" quando o correto é 2020 × 17). Os valores que provêm de operações pandas diretas sobre as planilhas se mantiveram corretos. **Regra adotada:** todo número que vai para a tese sai de operação atômica em pandas (ou da própria contagem nas planilhas via Excel), nunca de soma feita em prosa.

---

## Coortes — definição precisa

| Coorte | Definição | N |
|---|---|---:|
| **CAPES universo total** | Dump oficial `BR-CAPES-BTD-2021A2024-2025-12-01`, 4 XLSX concatenados, sem filtro de tema | 350.071 |
| CAPES Humanas universo | Subset onde `NM_GRANDE_AREA_CONHECIMENTO = "CIÊNCIAS HUMANAS"` | 59.976 |
| **CAPES corpus IA/ML/DL** | Aplicação de `utils.classificar_foco_ia` ao universo total | 12.995 |
| CAPES corpus IA-Humanas | Interseção das duas linhas acima | 400 |
| **SciELO bruto** | Coleta da API ArticleMeta com `from=2021-01-01 & until=2024-12-31`, todas as subject_areas, classificador IA aplicado. Filtro from/until opera sobre `processing_date` | 659 |
| **SciELO recorte estrito** | Linhas do bruto com `ano de publicação` entre 2021 e 2024 inclusive | **631** |
| SciELO Human Sciences puro | Recorte estrito + `subject_areas_periodico` exatamente igual a "Human Sciences" (sem multi-área) | 72 |
| SciELO Brasil universo bruto | Universo bruto da coleta (todas subject_areas, todos os anos retornados pela API, antes de classificar IA) | 98.165 |
| **SciELO Brasil universo do recorte** | Universo restrito a `ano de publicação` 2021–2024 (denominador da taxa interna) | **90.360** |

> **Onde a tese cita:** "**631 artigos no recorte estrito** 2021–2024" para o panorama SciELO; "**72 artigos**" para o subset Human Sciences puro usado no comparativo com CAPES Humanas.

---

## Os 28 stragglers SciELO — decomposição verificada

Diferença entre coleta bruta (659) e recorte estrito (631).

| Ano de publicação | Artigos |
|---|---:|
| 1986 | 1 |
| 1990 | 1 |
| 1992 | 1 |
| 2004 | 1 |
| 2019 | 2 |
| 2020 | 17 |
| 2025 | 5 |
| **Total** | **28** |

Subtotal pré-2021: **23**. Subtotal pós-2024: **5**. Verificação: 23 + 5 = 28; 28 + 631 = 659. ✓

**Origem da divergência:** o filtro `from`/`until` da API ArticleMeta opera sobre `processing_date` (data de indexação na SciELO), não sobre `publication_date`. Artigos publicados antes de 2021 e re-indexados durante 2021–2024 entram no resultado; artigos publicados em 2025 que entraram no índice ainda em 2024 também. A análise descarta os 28 e trabalha com 631.

---

## SciELO recorte 631 — distribuição por subject_area

8 categorias oficiais SciELO + 1 categoria sintética "Multidisciplinar" (para periódicos cuja `subject_areas_periodico` lista mais de uma área).

| Subject area | N |
|---|---:|
| Health Sciences | 200 |
| Agricultural Sciences | 98 |
| Multidisciplinar (*sintética*) | 84 |
| Engineering | 78 |
| Human Sciences | 72 |
| Applied Social Sciences | 66 |
| Exact and Earth Sciences | 25 |
| Biological Sciences | 5 |
| Linguistics, Letters and Arts | 3 |
| **Soma** | **631** ✓ |

> **Atenção terminológica:** SciELO tem **8 subject_areas canônicas**. "Multidisciplinar" não é uma — é bucket nosso para evitar dupla contagem. **Não dizer "9 subject_areas" na tese**; a formulação precisa é "as 8 subject_areas do SciELO, mais uma categoria 'Multidisciplinar' para periódicos com classificação múltipla".

---

## SciELO Brasil universo do recorte (90.360) — distribuição por subject_area

Necessário para calcular taxa interna por área. Fonte: `dados_scielo/scielo_brasil_universo_agregado.csv`.

> **Atenção ao denominador:** as taxas internas abaixo usam o universo do recorte estrito 2021–2024 (90.360 artigos), NÃO o universo bruto da coleta (98.165). A diferença de ~7.800 artigos corresponde a artigos com data de publicação fora da janela 2021–2024 que a API devolveu por filtrar `processing_date`. A taxa geral SciELO (631/90.360 = 0,70%) é apples-to-apples: numerador e denominador no mesmo recorte temporal.

| Subject area | N | Taxa interna IA |
|---|---:|---:|
| Health Sciences | 35.704 | 0,56% |
| Human Sciences | 14.806 | **0,49%** |
| Multidisciplinar | 10.163 | 0,83% |
| Agricultural Sciences | 9.810 | 1,00% |
| Applied Social Sciences | 6.100 | 1,08% |
| Biological Sciences | 4.598 | 0,11% |
| Engineering | 4.551 | **1,71%** |
| Linguistics, Letters and Arts | 2.596 | 0,12% |
| Exact and Earth Sciences | 2.032 | 1,23% |

> **Engineering tem a maior taxa interna** (1,71%). Human Sciences tem 0,49%, magnitude próxima dos 0,67% de CAPES Humanas (validação independente da marginalidade).

---

## CAPES corpus IA-Humanas (400) — distribuição por área

Subset da CAPES restrito a `NM_GRANDE_AREA_CONHECIMENTO = CIÊNCIAS HUMANAS` no recorte 2021–2024. Cálculos no XLSX `dados_capes/capes_2021_2024_ia_humanas_completo.xlsx`.

| Área | N |
|---|---:|
| Educação | 154 |
| Geografia | 64 |
| Psicologia | 56 |
| Ciência Política | 40 |
| Filosofia | 39 |
| Sociologia | 25 |
| História | 12 |
| **Antropologia** | **4** |
| Teologia | 4 |
| Arqueologia | 2 |

---

## Comparativo SciELO Human Sciences puro × CAPES Humanas — paridade real

Apples-to-apples: SciELO restrito a 72 artigos com `subject_area = "Human Sciences"` puro contra os 400 da grande área Ciências Humanas no CAPES. Tabela completa em `tabelas_comparativas_2026.md`.

| Indicador | SciELO Human Sciences | CAPES Humanas |
|---|---:|---:|
| Total no campo | 72 | 400 |
| Foco Central | 52 | 234 |
| Correlatos | 20 | 166 |
| Crescimento 2021→2024 | 16 → 34 (+113%) | 69 → 142 (+106%) |

---

## Coortes históricas (NÃO usar como fonte para a tese)

Estas coortes foram superadas durante o trabalho. **Persistem no repositório** por reprodutibilidade do processo, **não como evidência válida**.

| Coorte | N | Por que foi descartada |
|---|---:|---|
| SciELO 1983–2025 (coleta web inicial) | 152 | Coleta manual via interface web; substituída pela coleta programática 631. |
| SciELO recorte 3 áreas-alvo (coleta intermediária) | 179 (estrito) / 188 (bruto) | Recorte arbitrário de 3 subject_areas; substituído pelo universo Brasil completo 631 a partir do qual derivamos Human Sciences puro = 72. |
| CAPES 2013–2023 web inicial | 100 | Coleta via scraping do catálogo web; substituída pelo dump oficial 2021–2024 = 12.995 / 400 em Humanas. |
| Health Sciences = 207 | — | Era da coorte bruta 659; o número certo da coorte estrita 631 é **200**. |
| Human Sciences = 74 | — | Era da coorte bruta 659; o número certo da coorte estrita 631 é **72**. |

---

## Como atualizar este arquivo

1. Quando refizer uma coleta ou um recorte, ATUALIZE este arquivo **antes** de mudar o README ou qualquer figura.
2. Para cada número novo, anote a coorte, o XLSX/CSV fonte, e a operação pandas que o produziu.
3. Faça um commit dedicado ("decisoes_metodologicas: atualiza N para Y após verificação de X") — não junte com mudança de figura ou texto.
4. Em seguida, sincronize README, inventário e tabelas para citar deste arquivo.

*Última verificação: 23 de maio de 2026 — auditoria completa do XLSX `scielo_brasil_ia_subcampos_auditoria.xlsx` (659 linhas brutas, 631 no recorte) e do agregado `scielo_brasil_universo_agregado.csv` (90.360 no recorte estrito 2021–2024, 98.165 no bruto da coleta API; 8 subject_areas oficiais + categoria sintética "Multidisciplinar"). Verificação cruzada com `capes_2021_2024_ia_humanas_completo.xlsx` confirma 400 IA-Humanas, distribuição por área conforme a tabela, e correção das estatísticas regionais e top IES que tinham ficado em coorte antiga (441) no README/inventário.*
