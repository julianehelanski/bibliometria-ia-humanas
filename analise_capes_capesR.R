# -*- coding: utf-8 -*-
# =============================================================================
# Análise CAPES de longa duração (1987-2024) via pacote capesR
# -----------------------------------------------------------------------------
# Complementa o pipeline Python deste repositório. Enquanto os scripts
# `analise_capes_2021_2024.py` / `analise_capes_humanas.py` trabalham o dump
# oficial BR-CAPES-BTD restrito a 2021-2024 (com resumo e palavras-chave
# completos), este script usa o pacote capesR (Hugo Medeiros) para puxar o
# Catálogo de Teses e Dissertações em série histórica longa e responder a
# uma pergunta que o dump curto não alcança:
#
#   Quando e como a IA emerge na produção pós-graduada das CIÊNCIAS HUMANAS
#   brasileiras ao longo de quase quatro décadas?
#
# O regex de identificação de IA é portado de `utils.py` para manter coerência
# metodológica entre as duas frentes (Python e R).
#
# Saídas:
#   dados_capes/capes_capesR_ia_humanas.csv     corpus auditável IA-Humanas
#   figuras/capes_r01_temporal_ia_humanas.png   evolução anual 1987-2024
#   figuras/capes_r02_share_ia_humanas.png      % de IA dentro de Humanas/ano
#   figuras/capes_r03_top_areas_humanas.png     áreas de Humanas com mais IA
#   figuras/capes_r04_top_ies_humanas.png       IES com mais teses IA-Humanas
#
# Pré-requisitos (instale uma vez):
#   install.packages(c("capesR", "dplyr", "stringr", "ggplot2", "readr", "scales"))
#
# Uso:
#   Rscript analise_capes_capesR.R
#
# Observação: capesR baixa os arquivos do OSF na primeira execução; para não
# rebaixar a cada vez, definimos um diretório persistente em DESTINO_DADOS.
# =============================================================================

suppressPackageStartupMessages({
  library(capesR)
  library(dplyr)
  library(stringr)
  library(ggplot2)
  library(readr)
  library(scales)
})

# -----------------------------------------------------------------------------
# Configuração
# -----------------------------------------------------------------------------
BASE_DIR     <- tryCatch(dirname(normalizePath(sys.frame(1)$ofile)), error = function(e) getwd())
DADOS_CAPES  <- file.path(BASE_DIR, "dados_capes")
FIGURAS_DIR  <- file.path(BASE_DIR, "figuras")
DESTINO_DADOS <- file.path(DADOS_CAPES, "capesR_cache")   # cache dos downloads OSF

# Janela temporal. capesR cobre 1987-2024. Para um teste rápido, reduza este
# vetor (ex.: 2018:2024) — baixar todos os anos pode levar tempo e disco.
ANOS <- 1987:2024

dir.create(DADOS_CAPES, showWarnings = FALSE, recursive = TRUE)
dir.create(FIGURAS_DIR, showWarnings = FALSE, recursive = TRUE)
dir.create(DESTINO_DADOS, showWarnings = FALSE, recursive = TRUE)

# -----------------------------------------------------------------------------
# Estilo visual: replica o "padrão Python" de utils.py (whitegrid sóbrio,
# paleta muted, spines limpos, 300 dpi).
# -----------------------------------------------------------------------------
CORES_INTERMEDIARIAS <- c(
  "#E57373", "#FFB74D", "#81C784", "#64B5F6", "#BA68C8", "#FFF176",
  "#F06292", "#4DB6AC", "#A1887F", "#90A4AE", "#B0BEC5", "#E0E0E0"
)
COR_ANTROPOLOGIA <- CORES_INTERMEDIARIAS[7]   # destaque do argumento da tese
COR_OUTRAS       <- CORES_INTERMEDIARIAS[10]
COR_PRINCIPAL    <- CORES_INTERMEDIARIAS[4]

tema_padrao <- theme_minimal(base_size = 11) +
  theme(
    panel.grid.major   = element_line(linetype = "dashed", linewidth = 0.3, colour = "grey80"),
    panel.grid.minor   = element_blank(),
    axis.line          = element_line(colour = "grey40", linewidth = 0.3),
    plot.title         = element_text(size = 12, face = "plain"),
    plot.subtitle      = element_text(size = 10, colour = "grey30"),
    plot.background    = element_rect(fill = "white", colour = NA),
    panel.background   = element_rect(fill = "white", colour = NA),
    legend.position    = "top"
  )

salvar <- function(plot, nome, w = 10, h = 6) {
  caminho <- file.path(FIGURAS_DIR, nome)
  ggsave(caminho, plot, width = w, height = h, dpi = 300, bg = "white")
  message("  figura -> ", caminho)
}

# -----------------------------------------------------------------------------
# Regex de IA portado de utils.py (mantém a coerência com o lado Python).
# perl = TRUE habilita \b (word boundaries); ignore.case = TRUE.
# -----------------------------------------------------------------------------
RE_IA_STRICT <- "\\b(intelig[êe]ncia\\s+artificial|artificial\\s+intelligence)\\b"
RE_ML        <- "\\b(machine\\s+learning|aprendizado\\s+de\\s+m[áa]quina)\\b"
RE_DL        <- "\\b(deep\\s+learning|aprendizado\\s+profundo|redes?\\s+neurais|neural\\s+networks?)\\b"
RE_LLM       <- paste0(
  "\\b(llms?|large\\s+language\\s+models?|modelos?\\s+de\\s+linguagem|",
  "chatgpt|gpt-\\d|ia\\s+generativa|generative\\s+ai)\\b"
)
RE_CORRELATOS <- paste0(
  "\\b(transhumanismo|p[óo]s-humanismo|rob[óo]tica|rob[ôo]s|",
  "automa[çc][ãa]o|automation|minera[çc][ãa]o\\s+de\\s+dados|data\\s+mining|",
  "big\\s+data|vis[ãa]o\\s+computacional|computer\\s+vision|",
  "processamento\\s+de\\s+linguagem\\s+natural|natural\\s+language\\s+processing|nlp)\\b"
)
# Núcleo central (1-4): define "Foco Central". Correlatos (5) é o entorno.
RE_IA_NUCLEO <- paste(RE_IA_STRICT, RE_ML, RE_DL, RE_LLM, sep = "|")

# 'transformer' isolado dá falso positivo (transformador elétrico, uso
# metafórico). Só conta se coocorrer com contexto técnico de NN/NLP.
RE_TRANSFORMER <- "\\btransformer[s]?\\b"
RE_CTX_NEURAL  <- paste0(
  "\\b(neural|atten[çc][ãa]o|attention|bert|encoder|decoder|",
  "self-?attention|pre-?train|fine-?tun|embedding|deep\\s+learning|",
  "aprendizado\\s+profundo|natural\\s+language|processamento\\s+de\\s+linguagem|",
  "nlp|language\\s+model|modelo\\s+de\\s+linguagem|huggingface)\\b"
)

detecta <- function(x, padrao) str_detect(x, regex(padrao, ignore_case = TRUE))

classificar_foco <- function(texto) {
  central <- detecta(texto, RE_IA_NUCLEO) |
             (detecta(texto, RE_TRANSFORMER) & detecta(texto, RE_CTX_NEURAL))
  correlato <- detecta(texto, RE_CORRELATOS)
  ifelse(central, "Foco Central",
         ifelse(correlato, "Correlato", "Outros Temas"))
}

# -----------------------------------------------------------------------------
# Detecção defensiva de colunas: o schema do capesR difere do dump oficial.
# Procuramos o primeiro nome existente entre os candidatos (case-insensitive).
# -----------------------------------------------------------------------------
achar_col <- function(df, candidatos) {
  nomes <- names(df)
  for (c in candidatos) {
    hit <- nomes[tolower(nomes) == tolower(c)]
    if (length(hit) > 0) return(hit[1])
  }
  # fallback: match parcial
  for (c in candidatos) {
    hit <- nomes[str_detect(tolower(nomes), fixed(tolower(c)))]
    if (length(hit) > 0) return(hit[1])
  }
  NA_character_
}

COLMAP <- list(
  ano        = c("ano_base", "an_base", "base_year", "ano"),
  titulo     = c("titulo", "nm_producao", "title", "nm_titulo"),
  resumo     = c("resumo", "ds_resumo", "abstract", "ds_abstract"),
  keywords   = c("palavras_chave", "ds_palavra_chave", "ds_keyword", "keywords"),
  grande_area= c("grande_area_conhecimento", "nm_grande_area_conhecimento",
                 "grande_area", "area_avaliacao", "nm_area_avaliacao"),
  area       = c("area_conhecimento", "nm_area_conhecimento", "area"),
  grau       = c("grau_academico", "nm_grau_academico", "tipo", "type"),
  ies        = c("ies", "nm_entidade_ensino", "instituicao", "institution"),
  regiao     = c("regiao", "nm_regiao", "region"),
  uf         = c("uf", "sg_uf_ies", "estado", "state")
)

# =============================================================================
# 1. Baixar e carregar os dados
# =============================================================================
message("==> Baixando/lendo dados CAPES via capesR (anos: ",
        min(ANOS), "-", max(ANOS), ")")

arquivos <- download_capes_data(ANOS, destination = DESTINO_DADOS)
dados    <- read_capes_data(arquivos)

message("    registros lidos: ", format(nrow(dados), big.mark = "."))
message("    colunas: ", paste(head(names(dados), 30), collapse = ", "))

cols <- lapply(COLMAP, function(cands) achar_col(dados, cands))
faltando <- names(cols)[is.na(unlist(cols))]
if (length(faltando) > 0) {
  message("[aviso] colunas não localizadas (seguindo sem elas): ",
          paste(faltando, collapse = ", "))
}

# =============================================================================
# 2. Filtrar Ciências Humanas + classificar foco em IA
# =============================================================================
col_ga <- cols$grande_area
if (is.na(col_ga)) stop("Não encontrei a coluna de grande área. Inspecione names(dados).")

humanas <- dados %>%
  filter(str_detect(.data[[col_ga]], regex("humanas", ignore_case = TRUE)))

message("    registros em Ciências Humanas: ", format(nrow(humanas), big.mark = "."))

# Texto de classificação = título (+ resumo + keywords quando existirem)
montar_texto <- function(df) {
  partes <- list()
  if (!is.na(cols$titulo))   partes[[length(partes)+1]] <- coalesce(as.character(df[[cols$titulo]]), "")
  if (!is.na(cols$resumo))   partes[[length(partes)+1]] <- coalesce(as.character(df[[cols$resumo]]), "")
  if (!is.na(cols$keywords)) partes[[length(partes)+1]] <- coalesce(as.character(df[[cols$keywords]]), "")
  if (length(partes) == 0) stop("Nenhuma coluna textual encontrada (título/resumo/keywords).")
  do.call(paste, c(partes, sep = " | "))
}

humanas <- humanas %>%
  mutate(.texto = montar_texto(.),
         FOCO_IA = classificar_foco(.texto))

ia_hum <- humanas %>% filter(FOCO_IA %in% c("Foco Central", "Correlato"))
message("    trabalhos IA em Humanas (Central+Correlato): ",
        format(nrow(ia_hum), big.mark = "."))

# Corpus auditável
out_csv <- file.path(DADOS_CAPES, "capes_capesR_ia_humanas.csv")
write_csv(ia_hum %>% select(-.texto), out_csv)
message("    corpus salvo -> ", out_csv)

if (nrow(ia_hum) == 0) {
  message("Nenhum trabalho IA-Humanas encontrado no recorte. Encerrando antes das figuras.")
  quit(save = "no")
}

# =============================================================================
# 3. Figuras
# =============================================================================
col_ano <- cols$ano

# --- r01: evolução anual do nº de teses/dissertações IA-Humanas ---------------
if (!is.na(col_ano)) {
  serie <- ia_hum %>%
    mutate(ano = as.integer(.data[[col_ano]])) %>%
    filter(!is.na(ano)) %>%
    count(ano, FOCO_IA)

  p1 <- ggplot(serie, aes(ano, n, fill = FOCO_IA)) +
    geom_col(width = 0.85) +
    scale_fill_manual(values = c("Foco Central" = COR_PRINCIPAL,
                                 "Correlato"    = COR_OUTRAS),
                      name = NULL) +
    labs(title = "IA na pós-graduação em Ciências Humanas (CAPES, 1987-2024)",
         subtitle = "Teses e dissertações por ano, via pacote capesR",
         x = NULL, y = "Nº de trabalhos") +
    scale_x_continuous(breaks = scales::pretty_breaks(10)) +
    tema_padrao
  salvar(p1, "capes_r01_temporal_ia_humanas.png")
}

# --- r02: % de IA dentro de Humanas por ano (intensidade do fenômeno) ---------
if (!is.na(col_ano)) {
  total_ano <- humanas %>%
    mutate(ano = as.integer(.data[[col_ano]])) %>%
    filter(!is.na(ano)) %>%
    count(ano, name = "total_humanas")
  ia_ano <- ia_hum %>%
    mutate(ano = as.integer(.data[[col_ano]])) %>%
    filter(!is.na(ano)) %>%
    count(ano, name = "ia_humanas")
  share <- total_ano %>%
    left_join(ia_ano, by = "ano") %>%
    mutate(ia_humanas = coalesce(ia_humanas, 0L),
           pct = 100 * ia_humanas / total_humanas)

  p2 <- ggplot(share, aes(ano, pct)) +
    geom_line(colour = COR_PRINCIPAL, linewidth = 0.8) +
    geom_point(colour = COR_PRINCIPAL, size = 1.6) +
    labs(title = "Intensidade da IA dentro das Ciências Humanas",
         subtitle = "% de trabalhos que mencionam IA/ML/DL sobre o total de Humanas, por ano",
         x = NULL, y = "% dos trabalhos de Humanas") +
    scale_x_continuous(breaks = scales::pretty_breaks(10)) +
    tema_padrao
  salvar(p2, "capes_r02_share_ia_humanas.png")
}

# --- r03: áreas de Humanas com mais IA (Antropologia em destaque) -------------
if (!is.na(cols$area)) {
  top_areas <- ia_hum %>%
    mutate(area = coalesce(as.character(.data[[cols$area]]), "(s/info)")) %>%
    count(area, sort = TRUE) %>%
    slice_head(n = 15) %>%
    mutate(destaque = ifelse(str_detect(tolower(area), "antropologia"),
                             "Antropologia", "Outras áreas"))

  p3 <- ggplot(top_areas, aes(reorder(area, n), n, fill = destaque)) +
    geom_col() +
    coord_flip() +
    scale_fill_manual(values = c("Antropologia" = COR_ANTROPOLOGIA,
                                 "Outras áreas" = COR_OUTRAS), name = NULL) +
    labs(title = "Áreas das Ciências Humanas com mais trabalhos sobre IA",
         subtitle = "Top 15 áreas de conhecimento no corpus IA-Humanas (CAPES)",
         x = NULL, y = "Nº de trabalhos") +
    tema_padrao
  salvar(p3, "capes_r03_top_areas_humanas.png", h = 7)
}

# --- r04: IES com mais teses IA-Humanas ---------------------------------------
if (!is.na(cols$ies)) {
  top_ies <- ia_hum %>%
    mutate(ies = coalesce(as.character(.data[[cols$ies]]), "(s/info)")) %>%
    count(ies, sort = TRUE) %>%
    slice_head(n = 15)

  p4 <- ggplot(top_ies, aes(reorder(ies, n), n)) +
    geom_col(fill = COR_PRINCIPAL) +
    coord_flip() +
    labs(title = "Instituições com mais trabalhos sobre IA em Ciências Humanas",
         subtitle = "Top 15 IES no corpus IA-Humanas (CAPES, 1987-2024)",
         x = NULL, y = "Nº de trabalhos") +
    tema_padrao
  salvar(p4, "capes_r04_top_ies_humanas.png", h = 7)
}

message("==> Concluído. Corpus em ", out_csv, " e figuras em ", FIGURAS_DIR)
