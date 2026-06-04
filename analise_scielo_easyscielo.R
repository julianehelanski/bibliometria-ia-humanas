# -*- coding: utf-8 -*-
# =============================================================================
# Análise SciELO via pacote easyScieloPack (triangulação da frente Python)
# -----------------------------------------------------------------------------
# Complementa o pipeline Python deste repositório. Enquanto
# `analise_scielo_articlemeta.py` coleta via API oficial ArticleMeta
# (percorrendo periódicos de Ciências Humanas do SciELO Brasil), este script
# usa o pacote easyScieloPack (Programa-ISA / Pablo Ixcamparij), que faz buscas
# na interface de pesquisa do SciELO. São DOIS caminhos de coleta distintos
# sobre a mesma base — útil para TRIANGULAR resultados: se as duas frentes
# convergem na tendência temporal da IA, o achado fica mais robusto.
#
# O regex de identificação de IA e os subcampos são portados de `utils.py`
# para manter coerência metodológica com o lado Python.
#
# Saídas:
#   dados_scielo/scielo_easyscielo_ia.csv          corpus auditável IA
#   figuras/scielo_es01_temporal_ia.png            evolução anual por foco
#   figuras/scielo_es02_subcampos.png              distribuição por subcampo
#   figuras/scielo_es03_top_termos.png             termos mais frequentes
#   figuras/scielo_es04_acumulado.png              crescimento acumulado
#
# Pré-requisitos (instale uma vez):
#   install.packages(c("remotes","dplyr","stringr","ggplot2","readr","tidyr"))
#   remotes::install_github("Programa-ISA/easyScieloPack")
#
# Uso:
#   Rscript analise_scielo_easyscielo.R
#
# ATENÇÃO: easyScieloPack faz scraping da busca do SciELO. Cada filtro aceita
# UM valor por consulta e o site pode retornar 403 (anti-scraping). Por isso o
# script itera termo a termo, com pausa entre chamadas, e tolera falhas.
# =============================================================================

suppressPackageStartupMessages({
  # O nome do pacote no library() é "easyScieloPak" (sem o 2º 'c'); o repo é
  # "easyScieloPack". Tentamos os dois para robustez.
  ok <- suppressWarnings(require(easyScieloPak, quietly = TRUE)) ||
        suppressWarnings(require(easyScieloPack, quietly = TRUE))
  if (!ok) stop("Pacote easyScielo não instalado. Rode:\n",
                "  remotes::install_github(\"Programa-ISA/easyScieloPack\")")
  library(dplyr)
  library(stringr)
  library(ggplot2)
  library(readr)
  library(tidyr)
})

# -----------------------------------------------------------------------------
# Configuração
# -----------------------------------------------------------------------------
BASE_DIR     <- tryCatch(dirname(normalizePath(sys.frame(1)$ofile)), error = function(e) getwd())
DADOS_SCIELO <- file.path(BASE_DIR, "dados_scielo")
FIGURAS_DIR  <- file.path(BASE_DIR, "figuras")

dir.create(DADOS_SCIELO, showWarnings = FALSE, recursive = TRUE)
dir.create(FIGURAS_DIR, showWarnings = FALSE, recursive = TRUE)

# Coleção SciELO Brasil. Intervalo temporal (SciELO começa ~1997-1998).
COLECAO    <- "Brazil"
ANO_INICIO <- 1998
ANO_FIM    <- 2024
N_MAX      <- 2000          # teto por consulta (NULL = deixa o pacote decidir)
PAUSA_SEG  <- 3            # pausa entre chamadas para evitar bloqueio 403

# Termos de busca de IA. Como cada consulta aceita um termo, iteramos a lista.
# Cobrimos PT/EN/ES dos núcleos central e correlato.
TERMOS_BUSCA <- c(
  "inteligência artificial", "artificial intelligence", "inteligencia artificial",
  "aprendizado de máquina", "machine learning", "aprendizaje automático",
  "aprendizado profundo", "deep learning", "redes neurais", "neural networks",
  "modelos de linguagem", "large language models", "chatgpt", "ia generativa",
  "processamento de linguagem natural", "natural language processing"
)

# Categorias temáticas de Ciências Humanas no SciELO. Filtro server-side
# (opcional). Deixe NULL para buscar em TODAS as áreas e recortar depois.
# Ajuste os nomes conforme as categorias aceitas pelo SciELO se necessário.
CATEGORIAS_HUMANAS <- NULL
# Ex.: c("Human Sciences", "Applied Social Sciences", "Linguistics, Letters and Arts")

# -----------------------------------------------------------------------------
# Estilo visual (replica utils.py)
# -----------------------------------------------------------------------------
CORES_INTERMEDIARIAS <- c(
  "#E57373", "#FFB74D", "#81C784", "#64B5F6", "#BA68C8", "#FFF176",
  "#F06292", "#4DB6AC", "#A1887F", "#90A4AE", "#B0BEC5", "#E0E0E0"
)
COR_PRINCIPAL <- CORES_INTERMEDIARIAS[4]
COR_OUTRAS    <- CORES_INTERMEDIARIAS[10]

tema_padrao <- theme_minimal(base_size = 11) +
  theme(
    panel.grid.major = element_line(linetype = "dashed", linewidth = 0.3, colour = "grey80"),
    panel.grid.minor = element_blank(),
    axis.line        = element_line(colour = "grey40", linewidth = 0.3),
    plot.title       = element_text(size = 12, face = "plain"),
    plot.subtitle    = element_text(size = 10, colour = "grey30"),
    plot.background  = element_rect(fill = "white", colour = NA),
    panel.background = element_rect(fill = "white", colour = NA),
    legend.position  = "top"
  )

salvar <- function(plot, nome, w = 10, h = 6) {
  caminho <- file.path(FIGURAS_DIR, nome)
  ggsave(caminho, plot, width = w, height = h, dpi = 300, bg = "white")
  message("  figura -> ", caminho)
}

# -----------------------------------------------------------------------------
# Regex de IA portado de utils.py (subcampos + foco)
# -----------------------------------------------------------------------------
RE_IA_STRICT <- "\\b(intelig[êe]ncia\\s+artificial|artificial\\s+intelligence)\\b"
RE_ML        <- "\\b(machine\\s+learning|aprendizado\\s+de\\s+m[áa]quina)\\b"
RE_DL        <- "\\b(deep\\s+learning|aprendizado\\s+profundo|redes?\\s+neurais|neural\\s+networks?)\\b"
RE_LLM       <- paste0("\\b(llms?|large\\s+language\\s+models?|modelos?\\s+de\\s+linguagem|",
                       "chatgpt|gpt-\\d|ia\\s+generativa|generative\\s+ai)\\b")
RE_CORRELATOS <- paste0("\\b(transhumanismo|p[óo]s-humanismo|rob[óo]tica|rob[ôo]s|",
                        "automa[çc][ãa]o|automation|minera[çc][ãa]o\\s+de\\s+dados|data\\s+mining|",
                        "big\\s+data|vis[ãa]o\\s+computacional|computer\\s+vision|",
                        "processamento\\s+de\\s+linguagem\\s+natural|natural\\s+language\\s+processing|nlp)\\b")
RE_IA_NUCLEO <- paste(RE_IA_STRICT, RE_ML, RE_DL, RE_LLM, sep = "|")
RE_TRANSFORMER <- "\\btransformer[s]?\\b"
RE_CTX_NEURAL  <- paste0("\\b(neural|atten[çc][ãa]o|attention|bert|encoder|decoder|",
                         "self-?attention|pre-?train|fine-?tun|embedding|deep\\s+learning|",
                         "aprendizado\\s+profundo|natural\\s+language|processamento\\s+de\\s+linguagem|",
                         "nlp|language\\s+model|modelo\\s+de\\s+linguagem|huggingface)\\b")

SUBCAMPOS <- list(
  "IA em sentido estrito"                = RE_IA_STRICT,
  "Aprendizado de máquina (ML)"          = RE_ML,
  "Aprendizado profundo & redes neurais" = RE_DL,
  "Modelos de linguagem & IA generativa" = RE_LLM,
  "Tecnologias correlatas"               = RE_CORRELATOS
)
SUBCAMPOS_CENTRAIS <- names(SUBCAMPOS)[1:4]

detecta <- function(x, padrao) str_detect(x, regex(padrao, ignore_case = TRUE))

classificar_foco <- function(texto) {
  central <- detecta(texto, RE_IA_NUCLEO) |
             (detecta(texto, RE_TRANSFORMER) & detecta(texto, RE_CTX_NEURAL))
  correlato <- detecta(texto, RE_CORRELATOS)
  ifelse(central, "Foco Central", ifelse(correlato, "Correlato", "Outros Temas"))
}

# -----------------------------------------------------------------------------
# Stopwords (PT + EN) para a nuvem de termos
# -----------------------------------------------------------------------------
STOPWORDS <- c(
  "a","o","as","os","um","uma","de","da","do","das","dos","em","na","no","nas","nos",
  "para","por","com","sem","sobre","entre","e","ou","que","se","como","ao","aos",
  "estudo","análise","analise","pesquisa","trabalho","uso","caso","partir","través",
  "the","of","and","in","on","for","to","a","an","with","from","by","study","analysis",
  "research","using","based","case","this","is","are","la","el","los","las","de","y","en"
)

# =============================================================================
# 1. Coleta: itera termos de busca
# =============================================================================
buscar_termo <- function(termo) {
  message("  buscando: '", termo, "' ...")
  args <- list(query = termo, collections = COLECAO,
               year_start = ANO_INICIO, year_end = ANO_FIM, n_max = N_MAX)
  if (!is.null(CATEGORIAS_HUMANAS)) args$categories <- CATEGORIAS_HUMANAS[1]
  res <- tryCatch(do.call(search_scielo, args),
                  error = function(e) { message("    [falha] ", conditionMessage(e)); NULL })
  Sys.sleep(PAUSA_SEG)
  if (is.null(res) || nrow(res) == 0) return(NULL)
  res$termo_busca <- termo
  res
}

message("==> Coletando do SciELO ", COLECAO, " (", ANO_INICIO, "-", ANO_FIM, ") via easyScielo")
partes <- lapply(TERMOS_BUSCA, buscar_termo)
partes <- Filter(Negate(is.null), partes)
if (length(partes) == 0) {
  stop("Nenhum resultado retornado. Verifique conexão / possível bloqueio 403 do SciELO.")
}

bruto <- bind_rows(partes)
message("    registros brutos (com repetição entre termos): ", nrow(bruto))
message("    colunas retornadas: ", paste(names(bruto), collapse = ", "))

# Detecção defensiva das colunas-chave do retorno (title/abstract/year/doi)
col <- function(cands) {
  hit <- names(bruto)[tolower(names(bruto)) %in% tolower(cands)]
  if (length(hit)) hit[1] else NA_character_
}
c_title <- col(c("title","titulo")); c_abs <- col(c("abstract","resumo"))
c_year  <- col(c("year","ano","publication_year")); c_doi <- col(c("doi"))

# =============================================================================
# 2. Dedupe + classificação
# =============================================================================
bruto$.chave <- if (!is.na(c_doi)) {
  ifelse(is.na(bruto[[c_doi]]) | bruto[[c_doi]] == "",
         tolower(trimws(as.character(bruto[[c_title]]))),
         tolower(trimws(as.character(bruto[[c_doi]]))))
} else tolower(trimws(as.character(bruto[[c_title]])))

dados <- bruto %>% distinct(.chave, .keep_all = TRUE)
message("    registros únicos após dedupe: ", nrow(dados))

texto <- paste(
  if (!is.na(c_title)) coalesce(as.character(dados[[c_title]]), "") else "",
  if (!is.na(c_abs))   coalesce(as.character(dados[[c_abs]]), "")   else ""
)
dados$FOCO_IA <- classificar_foco(texto)
dados$.texto  <- texto

# Subcampos (um trabalho pode estar em vários)
for (nm in names(SUBCAMPOS)) {
  dados[[paste0("SUB_", nm)]] <- detecta(texto, SUBCAMPOS[[nm]])
}
# regra do transformer -> conta como LLM
llm_col <- paste0("SUB_", "Modelos de linguagem & IA generativa")
dados[[llm_col]] <- dados[[llm_col]] |
  (detecta(texto, RE_TRANSFORMER) & detecta(texto, RE_CTX_NEURAL))

ia <- dados %>% filter(FOCO_IA %in% c("Foco Central","Correlato"))
message("    trabalhos classificados como IA (Central+Correlato): ", nrow(ia))

out_csv <- file.path(DADOS_SCIELO, "scielo_easyscielo_ia.csv")
write_csv(ia %>% select(-.texto, -.chave), out_csv)
message("    corpus salvo -> ", out_csv)

if (nrow(ia) == 0) { message("Sem IA no recorte; encerrando."); quit(save = "no") }

# =============================================================================
# 3. Figuras
# =============================================================================

# --- es01: evolução anual por foco -------------------------------------------
if (!is.na(c_year)) {
  serie <- ia %>%
    mutate(ano = suppressWarnings(as.integer(substr(as.character(.data[[c_year]]), 1, 4)))) %>%
    filter(!is.na(ano), ano >= ANO_INICIO, ano <= ANO_FIM) %>%
    count(ano, FOCO_IA)

  p1 <- ggplot(serie, aes(ano, n, fill = FOCO_IA)) +
    geom_col(width = 0.85) +
    scale_fill_manual(values = c("Foco Central" = COR_PRINCIPAL, "Correlato" = COR_OUTRAS),
                      name = NULL) +
    labs(title = "IA em artigos do SciELO Brasil (via easyScielo)",
         subtitle = "Artigos por ano e foco — triangulação da frente ArticleMeta",
         x = NULL, y = "Nº de artigos") +
    tema_padrao
  salvar(p1, "scielo_es01_temporal_ia.png")

  # --- es04: crescimento acumulado ------------------------------------------
  acum <- serie %>% group_by(ano) %>% summarise(n = sum(n), .groups = "drop") %>%
    arrange(ano) %>% mutate(acumulado = cumsum(n))
  p4 <- ggplot(acum, aes(ano, acumulado)) +
    geom_area(fill = COR_PRINCIPAL, alpha = 0.25) +
    geom_line(colour = COR_PRINCIPAL, linewidth = 0.9) +
    geom_point(colour = COR_PRINCIPAL, size = 1.6) +
    labs(title = "Crescimento acumulado de artigos sobre IA (SciELO Brasil)",
         subtitle = "Soma corrida ano a ano", x = NULL, y = "Nº acumulado de artigos") +
    tema_padrao
  salvar(p4, "scielo_es04_acumulado.png")
}

# --- es02: distribuição por subcampo -----------------------------------------
sub_counts <- sapply(names(SUBCAMPOS), function(nm) sum(ia[[paste0("SUB_", nm)]], na.rm = TRUE))
sub_df <- tibble(subcampo = names(sub_counts), n = as.integer(sub_counts)) %>%
  mutate(tipo = ifelse(subcampo %in% SUBCAMPOS_CENTRAIS, "Central", "Correlato")) %>%
  arrange(n)

p2 <- ggplot(sub_df, aes(reorder(subcampo, n), n, fill = tipo)) +
  geom_col() +
  coord_flip() +
  scale_fill_manual(values = c("Central" = COR_PRINCIPAL, "Correlato" = COR_OUTRAS), name = NULL) +
  labs(title = "Subcampos de IA no corpus SciELO Brasil",
       subtitle = "Um artigo pode pertencer a mais de um subcampo",
       x = NULL, y = "Nº de artigos") +
  tema_padrao
salvar(p2, "scielo_es02_subcampos.png", h = 5)

# --- es03: termos mais frequentes --------------------------------------------
tokens <- ia$.texto %>%
  str_to_lower() %>%
  str_replace_all("[^a-záàâãéêíóôõúüç ]", " ") %>%
  str_split("\\s+") %>%
  unlist()
tokens <- tokens[nchar(tokens) >= 4 & !(tokens %in% STOPWORDS)]
top_termos <- tibble(termo = tokens) %>% count(termo, sort = TRUE) %>% slice_head(n = 20)

p3 <- ggplot(top_termos, aes(reorder(termo, n), n)) +
  geom_col(fill = COR_PRINCIPAL) +
  coord_flip() +
  labs(title = "Termos mais frequentes no corpus IA (SciELO Brasil)",
       subtitle = "Títulos + resumos, sem stopwords (PT/EN)", x = NULL, y = "Frequência") +
  tema_padrao
salvar(p3, "scielo_es03_top_termos.png", h = 7)

message("==> Concluído. Corpus em ", out_csv, " e figuras em ", FIGURAS_DIR)
