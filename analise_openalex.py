# -*- coding: utf-8 -*-
"""Coleta OpenAlex — IA nas Humanidades por país e ano.

Terceira fonte do projeto, ao lado de CAPES (teses/dissertações) e SciELO
(periódicos). O OpenAlex é um catálogo aberto e global (~250M de obras), o
que permite duas coisas que CAPES e SciELO não dão:

  1. **Recorte internacional** — produção de IA por país/ano, no estilo do
     gráfico OWID/CSET "Annual scholarly publications on AI", mas com o
     filtro de **área do conhecimento** (Humanidades) que aquela base NÃO
     tinha (lá "Field" = subcampo técnico da IA, não disciplina).
  2. **Interseção IA × Humanidades** de verdade, usando a classificação
     por *topic/field* do OpenAlex (Scopus-like) cruzada com o conceito
     "Artificial intelligence".

Coerência com o resto do projeto: aplica o MESMO `classificar_subcampos`
do CAPES/SciELO (utils.py) sobre título+abstract, para que os subcampos
(IA stricto, ML, DL, LLMs, correlatos) sejam comparáveis entre as três
bases.

------------------------------------------------------------------------
DOIS MODOS
------------------------------------------------------------------------

`--modo agregado` (default, rápido, minutos):
    Usa o `group_by` da API. NÃO baixa obra por obra. Devolve contagens
    de IA∩Humanidades por país e por ano, MAIS o universo de Humanidades
    (denominador) para calcular a **taxa interna** — a mesma métrica
    canônica usada nos blocos CAPES/SciELO de `decisoes_metodologicas.md`.

`--modo corpus` (lento, baixa obra por obra, horas em recortes grandes):
    Baixa título + abstract (reconstruído do inverted index) + país + ano
    + topic de cada obra de IA∩Humanidades, aplica `classificar_subcampos`
    e salva CSV + XLSX de auditoria, no mesmo formato dos outros scripts.
    Recomenda-se restringir a janela/país (ver --pais) antes de usar.

------------------------------------------------------------------------
USO
------------------------------------------------------------------------

    # 0) PRIMEIRO confirme os IDs de campo da API no seu ambiente:
    python analise_openalex.py --listar-campos --mailto voce@exemplo.com

    # 1) Panorama internacional IA×Humanidades por país/ano (rápido):
    python analise_openalex.py --modo agregado --mailto voce@exemplo.com

    # 2) Corpus detalhado do Brasil, com subcampos (lento):
    python analise_openalex.py --modo corpus --pais BR --mailto voce@exemplo.com

Pré-requisitos:
    pip install requests pandas openpyxl

Boa cidadania de API (OpenAlex "polite pool"):
    Passe SEMPRE --mailto com um e-mail real. Sem ele a API ainda
    responde, mas com prioridade menor e mais sujeita a throttling.
    Docs: https://docs.openalex.org/how-to-use-the-api/api-overview
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Iterator

import pandas as pd
import requests

from utils import (
    BASE_DIR,
    classificar_foco_ia,
    classificar_subcampos,
    garantir_diretorio,
)

API = "https://api.openalex.org"
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "analise-bibliometrica-ia-humanas/2026"})
TIMEOUT = 60
RATE_LIMIT_SECONDS = 0.12  # ~10 req/s; OpenAlex tolera, mas seja gentil
PER_PAGE = 200             # máximo permitido pela API

# Diretório de saída/cache, no mesmo padrão de dados_capes/ e dados_scielo/.
DADOS_OPENALEX_DIR = os.path.join(BASE_DIR, "dados_openalex")
CACHE_DIR = os.path.join(DADOS_OPENALEX_DIR, "cache_openalex")
garantir_diretorio(DADOS_OPENALEX_DIR)
garantir_diretorio(CACHE_DIR)

# =============================================================================
# FILTROS — IDs da OpenAlex
# =============================================================================
# IA: conceito "Artificial intelligence" (nível 1). ID estável e amplamente
# usado. O OpenAlex está migrando de `concepts` para `topics`, mas o conceito
# de IA continua disponível e é o recorte mais comparável ao OWID/CSET.
IA_FILTRO = "concepts.id:C154945302"

# HUMANIDADES: classificação por *field* (taxonomia Scopus/ASJC do OpenAlex).
# Recorte AMPLO (default), para aproximar o "Ciências Humanas" da CAPES — que é
# mais largo que só "Artes e Humanidades": inclui Sociologia, Ciência Política,
# Geografia, Antropologia, Educação etc. (Ciências Sociais), além de Filosofia,
# História e Religião (Artes e Humanidades). Por isso combinamos dois fields
# com a sintaxe OR ("|") do OpenAlex:
#   12 = Arts and Humanities
#   33 = Social Sciences
#
# >>> Os IDs PRECISAM ser confirmados no seu ambiente com `--listar-campos`,
#     porque a taxonomia do OpenAlex evolui. NÃO confie cegamente nestes valores.
#
# Observação: a CAPES classifica **Psicologia** dentro de "Ciências Humanas"
# (14% do corpus IA-Humanas), mas no OpenAlex Psicologia é o field SEPARADO 32.
# Para espelhar a CAPES com fidelidade total, inclua-o:
#   --humanidades-filtro "primary_topic.field.id:12|32|33"
# Para o recorte estrito "só Artes e Humanidades", use:
#   --humanidades-filtro "primary_topic.field.id:12"
HUMANIDADES_FILTRO = "primary_topic.field.id:12|33"  # Artes/Humanidades + Ciências Sociais (VERIFICAR)

# Recorte temporal default — alinhado ao OWID/CSET (2016–2024) para comparação.
ANO_INICIAL_DEFAULT = 2016
ANO_FINAL_DEFAULT = 2024


def _get(path_ou_url: str, params: dict | None = None) -> dict:
    """GET com retry exponencial e rate limiting. Aceita path ('/works') ou URL."""
    url = path_ou_url if path_ou_url.startswith("http") else f"{API}{path_ou_url}"
    for tentativa in range(5):
        try:
            r = SESSION.get(url, params=params, timeout=TIMEOUT)
            r.raise_for_status()
            time.sleep(RATE_LIMIT_SECONDS)
            return r.json()
        except (requests.RequestException, ValueError) as e:
            espera = 2 ** tentativa
            sys.stderr.write(
                f"[retry {tentativa+1}/5] {url}: {e} (aguardando {espera}s)\n"
            )
            time.sleep(espera)
    raise RuntimeError(f"falha após 5 tentativas em {url}")


def _params_base(mailto: str | None) -> dict:
    """Parâmetros comuns: polite pool via mailto, quando fornecido."""
    p: dict = {}
    if mailto:
        p["mailto"] = mailto
    return p


def montar_filtro(ano_ini: int, ano_fim: int, ia: str, humanidades: str,
                  pais: str | None) -> str:
    """Concatena os pedaços de filtro do OpenAlex (vírgula = AND)."""
    partes = [
        ia,
        humanidades,
        f"publication_year:{ano_ini}-{ano_fim}",
    ]
    if pais:
        # país do vínculo institucional de qualquer autor (mesma regra do OWID:
        # um trabalho conta para cada país de afiliação presente).
        partes.append(f"authorships.countries:{pais.upper()}")
    return ",".join(partes)


# =============================================================================
# DESCOBERTA — confirmar IDs de campo no ambiente do usuário
# =============================================================================

def listar_campos(mailto: str | None) -> None:
    """Imprime os `field` da taxonomia do OpenAlex com contagem de obras.

    Use isto ANTES de confiar em HUMANIDADES_FILTRO: a saída mostra o ID
    exato de "Arts and Humanities", "Social Sciences" etc. no estado atual
    da API.
    """
    print("Campos (primary_topic.field) no OpenAlex — confirme o ID de Humanidades:\n")
    params = _params_base(mailto)
    params["group_by"] = "primary_topic.field.id"
    data = _get("/works", params)
    grupos = data.get("group_by", [])
    grupos.sort(key=lambda g: -g.get("count", 0))
    for g in grupos:
        # key vem como URL (.../fields/12); o ID curto é o sufixo.
        chave = str(g.get("key", ""))
        id_curto = chave.rsplit("/", 1)[-1]
        nome = g.get("key_display_name", "")
        print(f"  id={id_curto:>4}  {nome:<32} obras={g.get('count', 0):,}")
    print(
        "\nDica: para Humanidades use, p.ex., "
        '--humanidades-filtro "primary_topic.field.id:<ID>"'
        "\n(ou combine com '|' para incluir Ciências Sociais).")


# =============================================================================
# MODO AGREGADO — group_by, sem baixar obras
# =============================================================================

def contar_group_by(filtro: str, group_by: str, mailto: str | None) -> pd.DataFrame:
    """Retorna DataFrame [key, nome, count] para um group_by da API."""
    params = _params_base(mailto)
    params["filter"] = filtro
    params["group_by"] = group_by
    params["per-page"] = PER_PAGE
    data = _get("/works", params)
    linhas = []
    for g in data.get("group_by", []):
        chave = str(g.get("key", ""))
        linhas.append({
            "key": chave.rsplit("/", 1)[-1],
            "nome": g.get("key_display_name", ""),
            "count": g.get("count", 0),
        })
    return pd.DataFrame(linhas)


def modo_agregado(args) -> None:
    """Contagens IA∩Humanidades por país e ano + universo de Humanidades."""
    mailto = args.mailto
    ia, hum = args.ia_filtro, args.humanidades_filtro

    filtro_ia_hum = montar_filtro(args.ano_inicial, args.ano_final, ia, hum, args.pais)
    # Denominador: universo de Humanidades (sem o filtro de IA), mesma janela/país.
    filtro_universo_hum = ",".join(
        p for p in [hum, f"publication_year:{args.ano_inicial}-{args.ano_final}"]
        + ([f"authorships.countries:{args.pais.upper()}"] if args.pais else [])
    )

    print("=== OpenAlex — modo agregado (IA × Humanidades) ===")
    print(f"Janela: {args.ano_inicial}–{args.ano_final}"
          + (f" | país: {args.pais.upper()}" if args.pais else " | global"))
    print(f"Filtro IA∩Humanidades: {filtro_ia_hum}")
    print(f"Filtro universo Humanidades: {filtro_universo_hum}\n")

    # Por ano
    ia_ano = contar_group_by(filtro_ia_hum, "publication_year", mailto)
    uni_ano = contar_group_by(filtro_universo_hum, "publication_year", mailto)
    por_ano = ia_ano.merge(uni_ano, on=["key", "nome"], how="outer",
                           suffixes=("_ia_hum", "_universo_hum"))
    por_ano = por_ano.rename(columns={"key": "ano"}).drop(columns=["nome"])
    por_ano["ano"] = pd.to_numeric(por_ano["ano"], errors="coerce")
    por_ano = por_ano.sort_values("ano").fillna(0)
    por_ano["taxa_interna_%"] = (
        100 * por_ano["count_ia_hum"] / por_ano["count_universo_hum"].replace(0, pd.NA)
    ).round(3)

    # Por país (só faz sentido no recorte global)
    if not args.pais:
        ia_pais = contar_group_by(filtro_ia_hum, "authorships.countries", mailto)
        uni_pais = contar_group_by(filtro_universo_hum, "authorships.countries", mailto)
        por_pais = ia_pais.merge(uni_pais, on=["key", "nome"], how="outer",
                                 suffixes=("_ia_hum", "_universo_hum"))
        por_pais = por_pais.rename(columns={"key": "pais_codigo", "nome": "pais"})
        por_pais = por_pais.fillna(0).sort_values("count_ia_hum", ascending=False)
        por_pais["taxa_interna_%"] = (
            100 * por_pais["count_ia_hum"]
            / por_pais["count_universo_hum"].replace(0, pd.NA)
        ).round(3)
    else:
        por_pais = None

    # Saída
    suf = f"_{args.pais.upper()}" if args.pais else "_global"
    out_ano = os.path.join(DADOS_OPENALEX_DIR, f"openalex_ia_humanas_por_ano{suf}.csv")
    por_ano.to_csv(out_ano, index=False)
    print("IA∩Humanidades por ano (com taxa interna sobre o universo de Humanidades):")
    print(por_ano.to_string(index=False))
    print(f"\n-> {out_ano}")

    if por_pais is not None:
        out_pais = os.path.join(DADOS_OPENALEX_DIR, "openalex_ia_humanas_por_pais_global.csv")
        por_pais.to_csv(out_pais, index=False)
        print("\nTop 20 países (IA∩Humanidades):")
        print(por_pais.head(20).to_string(index=False))
        print(f"\n-> {out_pais}")


# =============================================================================
# MODO CORPUS — baixa obras e aplica a taxonomia de subcampos do projeto
# =============================================================================

def reconstruir_abstract(inv_index: dict | None) -> str:
    """Reconstrói o abstract a partir do abstract_inverted_index do OpenAlex."""
    if not inv_index:
        return ""
    posicoes: list[tuple[int, str]] = []
    for palavra, idxs in inv_index.items():
        for i in idxs:
            posicoes.append((i, palavra))
    posicoes.sort(key=lambda t: t[0])
    return " ".join(palavra for _, palavra in posicoes)


def iter_works(filtro: str, mailto: str | None) -> Iterator[dict]:
    """Itera todas as obras de um filtro via paginação por cursor."""
    cursor = "*"
    select = ",".join([
        "id", "title", "publication_year", "language",
        "abstract_inverted_index", "authorships", "primary_topic",
    ])
    baixados = 0
    while cursor:
        params = _params_base(mailto)
        params.update({
            "filter": filtro,
            "per-page": PER_PAGE,
            "cursor": cursor,
            "select": select,
        })
        data = _get("/works", params)
        resultados = data.get("results", [])
        for obra in resultados:
            yield obra
        baixados += len(resultados)
        total = data.get("meta", {}).get("count", 0)
        cursor = data.get("meta", {}).get("next_cursor")
        sys.stderr.write(f"\r  baixadas {baixados:,}/{total:,} obras")
        sys.stderr.flush()
        if not resultados:
            break
    sys.stderr.write("\n")


def extrair_campos_obra(obra: dict) -> list[dict]:
    """Achata uma obra do OpenAlex em UMA linha por país de afiliação.

    Espelha a regra do OWID/CSET: um trabalho conta uma vez para CADA país
    presente entre as afiliações dos autores. Quem quiser a contagem única
    (1 linha por obra) pode deduplicar por 'openalex_id' depois.
    """
    titulo = obra.get("title") or ""
    abstract = reconstruir_abstract(obra.get("abstract_inverted_index"))
    ano = obra.get("publication_year")
    idioma = obra.get("language") or ""
    topic = obra.get("primary_topic") or {}
    field = ((topic.get("field") or {}).get("display_name")) if topic else ""
    domain = ((topic.get("domain") or {}).get("display_name")) if topic else ""

    # Países distintos entre todas as afiliações.
    paises: set[str] = set()
    for a in obra.get("authorships") or []:
        for c in a.get("countries") or []:
            if c:
                paises.add(c)
        # fallback: country_code das instituições
        for inst in a.get("institutions") or []:
            cc = inst.get("country_code")
            if cc:
                paises.add(cc)
    if not paises:
        paises = {""}  # mantém a obra mesmo sem país identificado

    texto = " | ".join([t for t in [titulo, abstract] if t])
    base = {
        "openalex_id": obra.get("id", "").rsplit("/", 1)[-1],
        "titulo": titulo,
        "ano": ano,
        "idioma": idioma,
        "field": field,
        "domain": domain,
        "_texto_classif": texto,
    }
    return [dict(base, pais=p) for p in sorted(paises)]


def modo_corpus(args) -> None:
    """Baixa obras IA∩Humanidades e aplica a taxonomia de subcampos."""
    filtro = montar_filtro(args.ano_inicial, args.ano_final,
                           args.ia_filtro, args.humanidades_filtro, args.pais)
    print("=== OpenAlex — modo corpus (baixa obra por obra) ===")
    print(f"Janela: {args.ano_inicial}–{args.ano_final}"
          + (f" | país: {args.pais.upper()}" if args.pais else " | GLOBAL (pode ser MUITO grande)"))
    print(f"Filtro: {filtro}\n")
    if not args.pais:
        print("AVISO: sem --pais o corpus global de IA×Humanidades pode ter "
              "centenas de milhares de obras. Considere restringir.\n")

    registros: list[dict] = []
    for obra in iter_works(filtro, args.mailto):
        registros.extend(extrair_campos_obra(obra))

    df = pd.DataFrame(registros)
    if df.empty:
        print("Nenhuma obra retornada. Verifique os filtros (--listar-campos).")
        return
    print(f"\nTotal de linhas (obra × país): {len(df):,} "
          f"| obras únicas: {df['openalex_id'].nunique():,}")

    # Aplica a MESMA taxonomia dos outros scripts.
    df["FOCO_IA"] = df["_texto_classif"].map(classificar_foco_ia)
    subcs = df["_texto_classif"].map(classificar_subcampos)
    mapa_col = {
        "IA em sentido estrito": "SUBCAMPO_IA_STRICTO",
        "Aprendizado de máquina (ML)": "SUBCAMPO_ML",
        "Aprendizado profundo & redes neurais": "SUBCAMPO_DL",
        "Modelos de linguagem & IA generativa": "SUBCAMPO_LLM",
        "Tecnologias correlatas (robótica, NLP, big data…)": "SUBCAMPO_CORRELATOS",
    }
    for nome, col in mapa_col.items():
        df[col] = subcs.map(lambda s, n=nome: n in s)
    df["SUBCAMPOS"] = subcs.map(lambda s: "; ".join(sorted(s)) if s else "")
    df = df.drop(columns=["_texto_classif"])

    suf = f"_{args.pais.upper()}" if args.pais else "_global"
    out_csv = os.path.join(DADOS_OPENALEX_DIR, f"openalex_ia_humanas_corpus{suf}.csv")
    df.to_csv(out_csv, index=False)
    print(f"\nCorpus salvo em {out_csv}")
    print("Distribuição FOCO_IA (linhas obra × país):")
    print(df["FOCO_IA"].value_counts().to_string())

    # XLSX de auditoria (só obras únicas, para inspeção manual).
    unicas = df.drop_duplicates(subset=["openalex_id"]).copy()
    out_xlsx = os.path.join(DADOS_OPENALEX_DIR, f"openalex_ia_humanas_auditoria{suf}.xlsx")
    unicas.to_excel(out_xlsx, index=False, engine="openpyxl")
    print(f"XLSX para auditoria (obras únicas, {len(unicas):,}): {out_xlsx}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--modo", choices=["agregado", "corpus"], default="agregado",
                        help="agregado=group_by rápido (default); corpus=baixa obras")
    parser.add_argument("--listar-campos", action="store_true",
                        help="Lista os IDs de field da API e sai (confirme Humanidades)")
    parser.add_argument("--mailto", default=None,
                        help="E-mail para o polite pool da OpenAlex (recomendado)")
    parser.add_argument("--pais", default=None,
                        help="Código ISO-2 (ex.: BR, US). Sem isto = global.")
    parser.add_argument("--ano-inicial", type=int, default=ANO_INICIAL_DEFAULT)
    parser.add_argument("--ano-final", type=int, default=ANO_FINAL_DEFAULT)
    parser.add_argument("--ia-filtro", default=IA_FILTRO,
                        help=f"Filtro de IA da API (default: {IA_FILTRO})")
    parser.add_argument("--humanidades-filtro", default=HUMANIDADES_FILTRO,
                        help=f"Filtro de Humanidades (default: {HUMANIDADES_FILTRO}; "
                             "VERIFIQUE com --listar-campos)")
    args = parser.parse_args()

    if args.listar_campos:
        listar_campos(args.mailto)
        return

    if not args.mailto:
        sys.stderr.write(
            "AVISO: rodando sem --mailto. A OpenAlex recomenda informar um "
            "e-mail (polite pool) para evitar throttling.\n\n")

    if args.modo == "agregado":
        modo_agregado(args)
    else:
        modo_corpus(args)


if __name__ == "__main__":
    main()
