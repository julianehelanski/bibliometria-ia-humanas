# Bibliometria da inteligência artificial nas ciências humanas brasileiras

Este repositório reúne os dados, os *scripts* e as figuras do mapeamento bibliométrico que fiz para o capítulo 2 da minha tese de doutorado, *{tecnografia} de um centro de inteligência artificial: seguindo cientistas e engenheiros, universidade afora* (Programa de Pós-Graduação em Ciências Sociais, IFCH, Unicamp, 2026). O mapeamento mede o lugar que as ciências humanas, e a antropologia dentro delas, ocupam na produção acadêmica brasileira sobre inteligência artificial, e situa a minha pesquisa nesse terreno.

## O que fiz

Cruzei três bases, no mesmo período (2021 a 2024) e com o mesmo classificador:

| Base | Coleta | Universo | Corpus em IA |
|---|---|---|---|
| Catálogo de Teses e Dissertações da CAPES | dump oficial `BR-CAPES-BTD-2021A2024-2025-12-01` (Dados Abertos CAPES) | 350.071 trabalhos | 12.995 trabalhos |
| SciELO Brasil | API ArticleMeta, todas as áreas | 98.165 artigos | 631 artigos |
| OpenAlex | API pública, *fields* de humanidades, comparação entre países (2016 a 2024) | por país | 849 obras brasileiras |

O classificador (`utils.py`) separa o campo em cinco subcampos, porque cada um tem genealogia e comunidade próprias: IA em sentido estrito, aprendizado de máquina, aprendizado profundo e redes neurais, modelos de linguagem e IA generativa, e tecnologias correlatas (robótica, PLN, *big data*, visão computacional). Um trabalho pode pertencer a mais de um subcampo. Para evitar falsos positivos, a sigla `IA` e o termo `transformer` só contam quando coocorrem com vocabulário técnico do campo; essa regra retirou 341 trabalhos que entravam no corpus da CAPES pelo sentido comum de *transformer*. Revisei a classificação nas planilhas de auditoria de cada base.

Os números usados na tese, com a coorte, a planilha de origem e a operação que produziu cada um, estão travados em [`docs/decisoes_metodologicas.md`](docs/decisoes_metodologicas.md), que prevalece sobre qualquer outro arquivo do repositório.

## Principais resultados

- **CAPES.** As ciências humanas são a maior grande área do universo de defesas (59.976), mas só 400 delas tratam de IA (0,67% da área), contra 12,0% nas engenharias e 14,3% nas ciências exatas e da terra. Entre as 400, a antropologia tem 4 trabalhos pela área de conhecimento (6 pela área de avaliação Antropologia/Arqueologia); a educação tem 154.
- **SciELO.** Nas *Human Sciences*, 72 artigos tratam do campo (0,49% da área). Os três artigos de *Mana* entre os periódicos com mais artigos, todos de 2024, entram pelo subcampo de tecnologias correlatas (*big data*).
- **Subcampos.** Na CAPES, aprendizado de máquina (5.284) supera IA em sentido estrito (3.821); no SciELO a ordem se inverte. Nas humanidades, a entrada no campo se dá pela IA como conceito e pelas tecnologias correlatas, e pouco pelas técnicas.
- **OpenAlex.** Entre os quinze países com mais obras de IA nas humanidades (2016 a 2024), o Brasil tem a menor taxa interna (1,57%), com o terceiro maior universo de obras de humanidades do grupo (636.607, atrás de Estados Unidos e Indonésia).

## O que entra na tese

No capítulo 2, seção "A emergência do campo brasileiro de estudos em inteligência artificial nas ciências humanas e sociais", entram treze figuras, todas em `figuras/`:

- CAPES: subcampos, participação por grande área, mapas de calor por área e termo e por subcampo e grande área, áreas das humanas e série temporal das humanas (`capes_11`, `capes_13`, `capes_21`, `capes_22`, `capes_h01`, `capes_h02`);
- SciELO: participação por *subject area* e subcampos (`scielo_11`, `scielo_21`);
- comparativo SciELO e CAPES (`comparativo_scielo_capes_2026.png`);
- OpenAlex: ranking de países, taxa interna por país, série brasileira e subcampos nas três bases (`openalex_01` a `openalex_04`).

A correspondência figura a figura, com o *script* de cada uma, está em [`docs/USO_NA_TESE.md`](docs/USO_NA_TESE.md) (versão tabular em [`docs/uso_na_tese.csv`](docs/uso_na_tese.csv)). As demais figuras e as legendas LaTeX prontas (`inventario_figuras_capes.md`, `docs/inventario_figuras_openalex.tex`) ficam como material de auditoria.

## Dados

- `dados_capes/`: os quatro arquivos anuais do dump oficial (via Git LFS), o dicionário de dados da CAPES e a planilha de auditoria dos 12.995 trabalhos (`capes_2021_2024_ia_auditoria.xlsx`).
- `dados_scielo/`: agregado do universo por *subject area* e planilha de auditoria dos 631 artigos (`scielo_brasil_ia_subcampos_auditoria.xlsx`). Os CSV completos do universo e o *cache* da API são regeneráveis pelo *script* e não estão versionados.
- `dados_openalex/`: corpus brasileiro, séries por ano e por país e planilha de auditoria.

Os dados da CAPES são abertos; os do SciELO e do OpenAlex seguem as políticas de uso de cada plataforma.

## Como reproduzir

```bash
pip install -r requirements.txt

# CAPES (dump em dados_capes/, ou CAPES_DATA_DIR apontando para ele)
python analise_capes_2021_2024.py
python figuras_capes_2021_2024.py
python analise_capes_humanas.py

# SciELO, universo Brasil
python analise_scielo_articlemeta.py --todas-as-areas
python figuras_scielo_articlemeta.py

# OpenAlex (informar um e-mail em --mailto)
python analise_openalex.py --modo agregado --mailto seu@email
python analise_openalex.py --modo corpus --pais BR --mailto seu@email
python figuras_openalex.py

# comparativo SciELO e CAPES
python analise_comparativa_2026.py
```

Instruções detalhadas do OpenAlex em [`docs/openalex_uso.md`](docs/openalex_uso.md). Os *scripts* em R (`analise_capes_capesR.R`, `analise_scielo_easyscielo.R`, documentados em `docs/capesR_uso.md` e `docs/easyscielo_uso.md`) são frentes de triangulação e não geram figuras da tese.

## Estrutura

```
utils.py                          classificador de subcampos, estilo e paleta
analise_capes_2021_2024.py        corpus CAPES; figuras_capes_2021_2024.py, analise_capes_humanas.py
analise_scielo_articlemeta.py     corpus SciELO; figuras_scielo_articlemeta.py
analise_openalex.py               corpus OpenAlex; figuras_openalex*.py
analise_comparativa_2026.py       comparativo SciELO e CAPES; tabelas_comparativas_2026.md
analise_capes.py, analise_scielo.py, analise_comparativa.py
                                  levantamento exploratório de 2025 (interface web), fora da tese
dados_capes/, dados_scielo/, dados_openalex/
figuras/
docs/                             decisões metodológicas, uso na tese, guias das frentes R e OpenAlex
```

## Limitações

A análise cobre o que as três bases indexam e deixa de fora livros, capítulos e anais. A classificação depende de expressões regulares sobre título, resumo e palavras-chave; o classificador é conservador por desenho (o termo `algoritmo`, sozinho, não basta). No SciELO, a API filtra por data de indexação, e por isso apliquei depois o recorte por ano de publicação (631 dos 659 artigos coletados). O OpenAlex privilegia metadados em inglês, o que tende a subestimar a produção brasileira.

## Uso de inteligência artificial generativa

Fiz os *scripts* deste repositório com o Claude Code e com o Claude, a partir das especificações metodológicas que defini e registrei em `docs/decisoes_metodologicas.md`. O Claude Code é a interface de linha de comando da Anthropic que dá ao modelo de linguagem acesso aos arquivos do projeto, para ler, escrever e executar *scripts*. Com eles escrevi e executei a coleta (dump da CAPES, API ArticleMeta do SciELO, OpenAlex), o classificador de subcampos, as tabelas e as figuras. São minhas a definição das bases e dos recortes, as regras do classificador, as decisões sobre falsos positivos, a revisão das planilhas de auditoria e a interpretação dos resultados no capítulo 2.

**Modelos registrados no histórico de versões:** Claude Opus 4.7, Claude Opus 4.8, Claude Opus 5.5 e Claude Sonnet 5.5 (abril a outubro de 2026). Os *commits* mais antigos não registram a versão do modelo.

Os *commits* com autor `Claude`, ou com a linha `Co-Authored-By: Claude …`, foram feitos em sessões do Claude Code; a marcação é gerada pela ferramenta e registra em que pontos do histórico o modelo participou do trabalho. A autoria e a responsabilidade pelo conteúdo são minhas e, conforme a Deliberação CONSU-A-005/2026 da Unicamp, as ferramentas de IA generativa não figuram como coautoras. A declaração formal de uso de IA generativa da tese está no [Anexo 1](https://github.com/julianehelanski/tecno-etnografia-centro-ia/blob/main/ex_ane1.tex).

## Citação

> HELANSKI, Juliane. *Bibliometria da inteligência artificial nas ciências humanas brasileiras*: dados e *scripts*. Campinas: Unicamp, 2026. Disponível em: https://github.com/julianehelanski/bibliometria-ia-humanas.

> HELANSKI, Juliane. *{tecnografia} de um centro de inteligência artificial*: seguindo cientistas e engenheiros, universidade afora. 2026. Tese (Doutorado em Ciências Sociais) – Instituto de Filosofia e Ciências Humanas, Universidade Estadual de Campinas, Campinas, 2026.

Metadados de citação em [`CITATION.cff`](CITATION.cff).

## Licença

Código sob licença [MIT](LICENSE). Os dados da CAPES, do SciELO e do OpenAlex seguem as políticas de uso de cada plataforma.
