# Inventário de figuras — análise CAPES 2021–2024

Documento de apoio para a redação do Capítulo 2 da tese. Para cada figura, contém:

- **Caminho do arquivo** no repositório (`figuras/...`)
- **Bloco LaTeX pronto** com `\caption{...}`, `\label{...}` e `\source{...}` — basta copiar e colar
- **Comentário analítico** com o que destacar no texto que acompanha a figura

Convenções adotadas:

- Todas as figuras vêm do dump oficial CAPES `BR-CAPES-BTD-2021A2024-2025-12-01` (versão 3.0, gerado 24/11/2025), totalizando 350.071 trabalhos de conclusão de pós-graduação stricto sensu, dos quais 12.995 foram identificados no corpus "Tecnologias de IA, ML e aprendizado profundo" pelo classificador refinado.
- O `\source{...}` usa o comando comum em teses brasileiras; troque por `\fonte{}`, `\floatfoot{}` ou similar conforme o template do PPGAS-USP.
- As `\label{}` seguem o padrão `fig:capes_NN_descritor` para fácil referência via `\autoref{}` ou `\Cref{}`.
- O ambiente assume `\usepackage{graphicx}` e largura padrão `0.95\linewidth` — ajuste conforme o layout.

---

## Painel geral — corpus completo

### Figura 11 — Distribuição por grande área (absoluto + taxa interna)

`figuras/capes_11_grande_area_share.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{figuras/capes_11_grande_area_share.png}
  \caption{Distribuição dos 12.995 trabalhos sobre Tecnologias de IA, ML e aprendizado profundo defendidos na pós-graduação brasileira (2021--2024) por grande área de conhecimento. O painel esquerdo mostra o volume absoluto e a participação percentual no corpus; o painel direito mostra a taxa interna --- isto é, a fração das defesas da grande área que tratam do campo. Ciências Humanas (destacadas em vermelho) figuram como a maior grande área no universo total (59.976 defesas, 17,1\% do dump), mas representam apenas 3,1\% do corpus IA/ML/DL e 0,7\% das defesas da própria grande área tratam do tema --- contra 14,3\% em Ciências Exatas e 12,0\% em Engenharias.}
  \label{fig:capes_11_grande_area}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Esta é a figura-síntese da virada metodológica para "todas as áreas". Ela permite que o leitor leia a marginalidade em duas chaves complementares: (i) chave **absoluta** --- Humanas é minoria expressiva no corpus; (ii) chave **relativa** --- mesmo dentro de Humanas, IA é objeto periférico. A diferença com Exatas/Engenharias é de uma ordem de grandeza (14× a 18×). Use como abertura da seção de resultados.

---

### Figura 12 — Evolução temporal por grande área (2021–2024)

`figuras/capes_12_temporal_grande_area.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{figuras/capes_12_temporal_grande_area.png}
  \caption{Evolução anual (2021--2024) do número de defesas sobre Tecnologias de IA, ML e aprendizado profundo por grande área de conhecimento. Cada linha corresponde a uma das nove grandes áreas; Ciências Humanas aparece destacada em vermelho. A inclinação das curvas mostra que o crescimento do campo é generalizado, mas distribuído de forma desigual: Ciências Exatas e Engenharias dominam em volume e ritmo, enquanto Humanas crescem em ritmo proporcional menor.}
  \label{fig:capes_12_temporal_grande_area}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Usar para mostrar que o ponto da marginalidade não é "Humanas não está crescendo" --- está crescendo --- mas que cresce no mesmo nível baixo, sem fechar o gap com Exatas/Engenharias. A taxa de crescimento composto (CAGR) do corpus total é de cerca de 14\% a.a., similar entre grandes áreas; o que muda é o ponto de partida.

---

### Figura 13 — Heatmap grande área × keyword

`figuras/capes_13_heatmap_area_keyword.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{figuras/capes_13_heatmap_area_keyword.png}
  \caption{Mapa de calor da co-ocorrência entre dez termos-chave do campo das Tecnologias de IA, ML e aprendizado profundo e as nove grandes áreas de conhecimento da CAPES, sobre o corpus de 12.995 defesas. Cada célula reporta o percentual do termo na linha (subcampo) concentrado naquela grande área e, entre parênteses, a contagem absoluta. A leitura por coluna evidencia, por exemplo, que ``redes neurais'' e ``machine/deep learning'' concentram-se em Ciências Exatas e Engenharias, enquanto ``ChatGPT/GPT-N'' aparece distribuído por todas as áreas, com presença particular em Sociais Aplicadas e Humanas.}
  \label{fig:capes_13_heatmap_area_keyword}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Esta figura revela a **assinatura discursiva** de cada grande área. Humanas conversam com o campo via "IA" e termos correlatos (ChatGPT, IA generativa), mas raramente via termos técnicos (redes neurais, deep learning). Engenharias têm o padrão inverso. Útil para fundamentar a tese de que "IA" significa coisas diferentes em diferentes áreas, mesmo quando a contagem agregada parece uniforme.

---

### Figura 14 — Evolução total do corpus (Foco Central + Correlatos)

`figuras/capes_14_temporal_total.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{figuras/capes_14_temporal_total.png}
  \caption{Evolução anual do corpus completo (2021--2024) discriminado em Foco Central (presença de termos de IA, ML, DL ou LLMs) e Correlatos (presença apenas de tecnologias adjacentes como robótica, NLP, big data ou visão computacional). O total cresce de 2.716 defesas em 2021 para 4.020 em 2024 (acréscimo de 48\% em quatro anos, CAGR aproximado de 14\% a.a.). O Foco Central representa a maior parte do crescimento; Correlatos mantém-se relativamente estável em volume absoluto.}
  \label{fig:capes_14_temporal_total}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Substitui a velha métrica de "crescimento 3.000\%" baseada em base muito pequena (2013--2023, 100 trabalhos). O CAGR de 14\% sobre uma base já robusta (2.700+/ano) é uma medida muito mais defensável do crescimento do campo.

---

### Figura 15 — Nível acadêmico

`figuras/capes_15_nivel_academico.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\linewidth]{figuras/capes_15_nivel_academico.png}
  \caption{Distribuição do corpus de 12.995 defesas sobre Tecnologias de IA, ML e aprendizado profundo (2021--2024) por grau acadêmico. O Mestrado responde pela maioria das defesas (cerca de 53\%), seguido pelo Doutorado (35\%) e pelo Mestrado Profissional (12\%). O Doutorado Profissional, modalidade ainda incipiente, aparece com participação residual.}
  \label{fig:capes_15_nivel_academico}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** O Mestrado predomina em volume, o que é esperado dada a estrutura do sistema. Mas a presença significativa do Mestrado Profissional sinaliza que a modalidade tem absorvido demanda aplicada do campo.

---

### Figura 16 — Top 20 áreas de conhecimento

`figuras/capes_16_top_areas_conhecimento.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\linewidth]{figuras/capes_16_top_areas_conhecimento.png}
  \caption{Vinte áreas de conhecimento com maior volume de defesas sobre Tecnologias de IA, ML e aprendizado profundo no quadriênio 2021--2024. As barras em vermelho assinalam áreas pertencentes à grande área de Ciências Humanas; as barras em cinza, as demais grandes áreas. A predominância de Ciência da Computação, Engenharia Elétrica e áreas técnicas correlatas é evidente; as áreas de Humanas que aparecem na lista --- Educação à frente --- chegam ao top 20 pela via aplicada, não pela via teórica.}
  \label{fig:capes_16_top_areas_conhecimento}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Mostra que mesmo em granularidade de área (e não só de grande área), Humanas está sub-representada. Educação aparece no top 20 graças ao volume bruto do campo educacional, mas Antropologia, Sociologia, Filosofia ficam de fora desta lista.

---

### Figura 17 — Top 20 instituições

`figuras/capes_17_top_instituicoes.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\linewidth]{figuras/capes_17_top_instituicoes.png}
  \caption{Vinte instituições de ensino superior com maior volume de defesas sobre Tecnologias de IA, ML e aprendizado profundo no quadriênio 2021--2024. A concentração nas universidades públicas federais e estaduais é expressiva; USP, UFRJ, UFMG, UNICAMP, UFRGS e UFPE figuram entre as principais.}
  \label{fig:capes_17_top_instituicoes}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Reforça a centralidade do sistema público de pós-graduação no campo. A ausência de instituições privadas no topo ressoa o argumento da tese sobre a infraestrutura institucional da pesquisa em IA no Brasil.

---

### Figura 18 — Distribuição regional e por UF

`figuras/capes_18_regiao_uf.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{figuras/capes_18_regiao_uf.png}
  \caption{Distribuição geográfica do corpus de defesas sobre Tecnologias de IA, ML e aprendizado profundo (2021--2024). À esquerda, o total por região; à direita, as 15 unidades federativas com maior volume. A concentração no Sudeste (em particular SP, RJ e MG) é a característica dominante, seguida pelo Sul. O eixo Norte permanece marginal --- padrão estrutural da pós-graduação brasileira.}
  \label{fig:capes_18_regiao_uf}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Documenta a desigualdade regional, que se reproduz quase intacta dentro do campo de IA.

---

### Figura 19 — Distribuição de páginas

`figuras/capes_19_paginas.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\linewidth]{figuras/capes_19_paginas.png}
  \caption{Histograma do número de páginas das defesas do corpus (excluindo casos com menos de 20 ou mais de 800 páginas, prováveis erros de digitação). A linha vermelha marca a mediana. A distribuição é assimétrica à direita: a maior parte das defesas tem entre 80 e 200 páginas, com cauda longa de teses mais volumosas.}
  \label{fig:capes_19_paginas}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Métrica de apoio. Útil se o capítulo discutir características formais das defesas (tamanho típico, dispersão).

---

### Figura 20 — Top termos em títulos

`figuras/capes_20_top_termos.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\linewidth]{figuras/capes_20_top_termos.png}
  \caption{Vinte e cinco termos mais frequentes nos títulos das 12.995 defesas do corpus, após remoção de stopwords e dos próprios termos canônicos do regex de IA (inteligência, artificial, machine, deep, learning etc.). O ranking revela o entorno semântico do campo --- vocabulários de aplicação (saúde, educação, classificação, predição) e de objetos (dados, sistemas, modelos) --- sem ser dominado pelos termos que definem o filtro.}
  \label{fig:capes_20_top_termos}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Útil como tabela complementar para discutir o vocabulário aplicado do campo. Considerar se pares ou trios de termos (bigrams) seriam mais informativos do que tokens isolados.

---

## Análise por subcampo

### Figura 21 — Distribuição por subcampo

`figuras/capes_21_subcampos_distribuicao.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\linewidth]{figuras/capes_21_subcampos_distribuicao.png}
  \caption{Distribuição das 12.995 defesas do corpus pelos cinco subcampos do classificador (presença pode ocorrer simultaneamente em múltiplos subcampos). Aprendizado de máquina (ML) é o subcampo mais frequente (5.284 defesas, 40,7\%), seguido por Tecnologias correlatas (38,3\%) e Aprendizado profundo \& redes neurais (33,3\%). IA em sentido estrito vem em quarto lugar (29,4\%), o que contraria a expectativa de que ``IA'' seja o rótulo dominante. Modelos de linguagem \& IA generativa é o menor subcampo em volume (506), mas o que mais cresce em ritmo.}
  \label{fig:capes_21_subcampos_distribuicao}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Figura central da argumentação contra o uso aglutinador do termo "IA". Sustenta empiricamente a tese de que tratar IA, ML, DL e LLMs como sinônimos mascara hierarquias relevantes do campo brasileiro.

---

### Figura 22 — Heatmap subcampo × grande área

`figuras/capes_22_heatmap_subcampo_grande_area.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{figuras/capes_22_heatmap_subcampo_grande_area.png}
  \caption{Mapa de calor da concentração dos cinco subcampos do classificador entre as nove grandes áreas. Cada linha (subcampo) está normalizada para somar 100\%, mostrando, para cada técnica, onde ela se concentra. Aprendizado profundo e redes neurais concentram-se massivamente em Ciências Exatas e Engenharias; Modelos de linguagem \& IA generativa, em contraste, distribui-se de forma mais espalhada, com presença notável em Sociais Aplicadas, Multidisciplinar e Humanas. Tecnologias correlatas (NLP, big data, robótica, automação) têm distribuição intermediária.}
  \label{fig:capes_22_heatmap_subcampo_grande_area}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Achado relevante para o argumento da tese: **LLMs/IA generativa é o subcampo que mais atravessa fronteiras**. Quando uma defesa fora das exatas toca o campo, é mais provável que toque por LLMs do que por redes neurais. Isso resoa com a hipótese antropológica sobre o ChatGPT como ponto de virada da entrada da IA no discurso público e humanístico.

---

### Figura 23 — Evolução temporal por subcampo

`figuras/capes_23_temporal_subcampos.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{figuras/capes_23_temporal_subcampos.png}
  \caption{Evolução temporal (2021--2024) das defesas em cada um dos cinco subcampos. Aprendizado de máquina mantém-se como o subcampo de maior volume ao longo de todo o período. Modelos de linguagem \& IA generativa, ainda que seja o menor em volume absoluto, apresenta o crescimento proporcionalmente mais expressivo em 2024 --- corolário da popularização do ChatGPT (lançado em novembro de 2022) e da entrada do tema na pauta pública e acadêmica.}
  \label{fig:capes_23_temporal_subcampos}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Documenta a "virada generativa" de 2024 com dados oficiais. O salto de LLMs/Generativa é proporcionalmente o maior --- ainda que em base baixa --- e marca o momento em que o campo da IA generativa começa a ser absorvido pela pós-graduação brasileira.

---

## Zoom em Ciências Humanas

### Figura H01 — Áreas de conhecimento em IA-Humanas

`figuras/capes_h01_areas_humanas.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\linewidth]{figuras/capes_h01_areas_humanas.png}
  \caption{Distribuição das 400 defesas no campo das Tecnologias de IA, ML e aprendizado profundo dentro da grande área de Ciências Humanas (2021--2024), por área de conhecimento. Educação responde por 38,5\% das defesas em IA/Humanas; Geografia (16,0\%), Psicologia (14,0\%), Ciência Política (10,0\%) e Filosofia (9,8\%) compõem o segundo bloco. A Antropologia, em destaque, aparece com quatro defesas (1,0\% do total), evidenciando posição marginal dentro do já marginal recorte de Humanas.}
  \label{fig:capes_h01_areas_humanas}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Figura central da argumentação da tese. A leitura é em duas camadas: dentro de Humanas, IA é um nicho (0,7\% das defesas) --- e dentro desse nicho, a Antropologia é marginal (1\% de um nicho). A marginalidade da Antropologia é, portanto, **dupla**.

---

### Figura H02 — Evolução temporal IA-Humanas por nível

`figuras/capes_h02_temporal_humanas.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\linewidth]{figuras/capes_h02_temporal_humanas.png}
  \caption{Evolução anual (2021--2024) das defesas em Ciências Humanas no campo das Tecnologias de IA, ML e aprendizado profundo, empilhadas por grau acadêmico (Mestrado, Doutorado, Mestrado Profissional). O crescimento é consistente, de cerca de 80 defesas em 2021 para mais de 150 em 2024 --- aproximadamente o dobro, em ritmo proporcionalmente maior do que o do corpus total no mesmo período. O Mestrado responde pela maior parte do crescimento.}
  \label{fig:capes_h02_temporal_humanas}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** Mostra que as Humanas estão se aproximando do tema --- mas a partir de uma base muito pequena. Importante para nuançar o argumento da marginalidade: ele descreve o estado presente, não uma tendência estática.

---

### Figura H03 — Top 15 IES em IA-Humanas

`figuras/capes_h03_top_ies_humanas.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\linewidth]{figuras/capes_h03_top_ies_humanas.png}
  \caption{Quinze instituições de ensino superior com maior volume de defesas sobre Tecnologias de IA, ML e aprendizado profundo em Ciências Humanas (2021--2024). UnB, USP e UFRJ lideram o conjunto; a presença simultânea de instituições do Sudeste (USP, UFRJ, UFMG, UNICAMP), do Sul (UFRGS) e do Nordeste (UFRN, UFC, UFPE) sugere algum descentramento regional, embora o eixo Sudeste-Sul ainda predomine.}
  \label{fig:capes_h03_top_ies_humanas}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** A USP, instituição da pesquisadora, aparece em segundo lugar (27 defesas), o que situa esta tese dentro do contexto institucional onde o tema ganhou tração nas Humanas.

---

### Figura H04 — Distribuição regional IA-Humanas

`figuras/capes_h04_regiao_humanas.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.75\linewidth]{figuras/capes_h04_regiao_humanas.png}
  \caption{Distribuição regional das defesas em Ciências Humanas no campo das Tecnologias de IA, ML e aprendizado profundo (2021--2024). O Sudeste concentra cerca de 45\% das defesas (em particular SP e RJ); o Sul (UFRGS, UFPR) e o Nordeste (UFC, UFRN, UFPE) compõem a maior parte do restante. O Norte aparece com presença residual.}
  \label{fig:capes_h04_regiao_humanas}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** O recorte de Humanas reproduz, com pequenas variações, a desigualdade regional do conjunto do dump (Figura 18).

---

### Figura H05 — Top termos em IA-Humanas

`figuras/capes_h05_top_termos_humanas.png`

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\linewidth]{figuras/capes_h05_top_termos_humanas.png}
  \caption{Vinte e cinco termos mais frequentes nos títulos das 400 defesas sobre Tecnologias de IA, ML e aprendizado profundo em Ciências Humanas (2021--2024), após remoção de stopwords e dos termos canônicos do regex de IA. O ranking revela o vocabulário próprio do recorte: termos como ``ensino'', ``educação'', ``ética'', ``trabalho'', ``escola'' e ``política'' indicam que a leitura humanística sobre IA aplica-se primariamente a contextos institucionais (escola, mercado de trabalho, política pública) e a problemas normativos (ética, regulação).}
  \label{fig:capes_h05_top_termos_humanas}
  \source{Elaboração própria a partir do Catálogo de Teses e Dissertações da CAPES (BR-CAPES-BTD-2021A2024-2025-12-01).}
\end{figure}
```

**Comentário analítico.** A diferença de vocabulário entre IA-Humanas (educação, ética, trabalho) e o corpus completo (sistemas, dados, predição --- ver Fig. 20) é uma evidência adicional da assinatura discursiva distinta das Humanas no campo.

---

## Cheat-sheet para referência cruzada no texto

| Argumento da tese | Figura(s) de apoio |
|---|---|
| Marginalidade das Humanas no campo de IA (em volume e em taxa interna) | Fig. 11, Fig. 16 |
| Marginalidade dupla da Antropologia (Humanas é margem, Antro é margem da margem) | Fig. H01 |
| Crescimento do campo sem fechamento do gap | Fig. 12, Fig. 14, Fig. H02 |
| Assinatura discursiva: Humanas usam "IA" e correlatos, não "redes neurais" | Fig. 13, Fig. 22 |
| ML supera "IA" no Brasil --- crítica ao uso aglutinador do termo | Fig. 21 |
| Virada generativa em 2024 | Fig. 23 |
| Concentração institucional e regional | Fig. 17, Fig. 18, Fig. H03, Fig. H04 |
| Vocabulário aplicado das Humanas (educação, ética, trabalho) | Fig. H05 |

---

## Bloco LaTeX de definição auxiliar (opcional, no preâmbulo)

Se o seu template ainda não tem o comando `\source`, ele pode ser definido assim:

```latex
\usepackage{caption}
\newcommand{\source}[1]{\caption*{\hfill\footnotesize\textit{Fonte:} #1}}
```

Ou, para uma versão que aparece logo abaixo da caption normal:

```latex
\newcommand{\source}[1]{\par\medskip\noindent\hfill\footnotesize\textit{Fonte:} #1}
```

---

*Documento gerado em 21 de maio de 2026, junto ao branch `claude/analyze-capes-catalog-dEzme` do repositório.*
