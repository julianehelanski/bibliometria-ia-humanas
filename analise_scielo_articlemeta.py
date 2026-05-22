# -*- coding: utf-8 -*-
"""Re-análise SciELO via API ArticleMeta — sem export manual RIS.

Substitui o workflow antigo (export manual da interface web → arquivo
RIS → parsing custom) por queries programáticas à API oficial. Aplica
o mesmo `classificar_subcampos` do CAPES, garantindo coerência entre
as duas bases.

Estratégia (eficiente):
  1. Lista todos os periódicos da coleção 'scl' (Brasil).
  2. Para cada periódico, identifica subject_areas. Mantém só os que
     incluem "Human Sciences", "Applied Social Sciences" ou
     "Linguistics, Letters and Arts" (o equivalente SciELO da grande
     área "Ciências Humanas" e adjacências).
  3. Para cada periódico relevante, lista PIDs de artigos via
     /article/identifiers/?issn=...&from=...&until=...
  4. Para cada PID, fetch /article/?format=xylose; extrai título,
     resumo, palavras-chave, autores, idioma, ano, periódico.
  5. Aplica classificar_subcampos no texto agregado.
  6. Salva subset IA em dados_scielo/scielo_ia_subcampos.csv +
     XLSX slim em scielo_ia_subcampos_auditoria.xlsx.

Cache: respostas da API ficam em dados_scielo/cache_articlemeta/. Re-
rodadas reutilizam o cache, então iterar regex/filtros fica barato.

Uso:
    python analise_scielo_articlemeta.py [--from 2021-01-01] [--until 2024-12-31]
    python analise_scielo_articlemeta.py --periodo-completo   # 1983-presente

Pré-requisitos:
    pip install requests pandas openpyxl
    (NÃO precisa de articlemetaapi nem xylose — usa requests puro.)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Iterator

import pandas as pd
import requests

from utils import (
    DADOS_SCIELO_DIR,
    classificar_foco_ia,
    classificar_subcampos,
    garantir_diretorio,
)

API = "https://articlemeta.scielo.org/api/v1"
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "analise-bibliometrica-ia-humanas/2026"})
TIMEOUT = 60
RATE_LIMIT_SECONDS = 0.25

CACHE_DIR = os.path.join(DADOS_SCIELO_DIR, "cache_articlemeta")
garantir_diretorio(CACHE_DIR)
garantir_diretorio(os.path.join(CACHE_DIR, "articles"))
garantir_diretorio(os.path.join(CACHE_DIR, "journals"))

# Áreas-alvo no vocabulário SciELO. Para a janela "Ciências Humanas" da CAPES,
# o equivalente SciELO inclui as três grandes categorias abaixo. Filtragem
# client-side via journal.subject_areas.
SUBJECT_AREAS_ALVO = {
    "Human Sciences",
    "Applied Social Sciences",
    "Linguistics, Letters and Arts",
}


def _get(path: str, params: dict | None = None) -> dict:
    """GET com retry e rate limiting."""
    for tentativa in range(5):
        try:
            r = SESSION.get(f"{API}{path}", params=params, timeout=TIMEOUT)
            r.raise_for_status()
            time.sleep(RATE_LIMIT_SECONDS)
            return r.json()
        except (requests.RequestException, ValueError) as e:
            espera = 2 ** tentativa
            sys.stderr.write(f"[retry {tentativa+1}/5] {path}: {e} (aguardando {espera}s)\n")
            time.sleep(espera)
    raise RuntimeError(f"falha após 5 tentativas em {path}")


def listar_periodicos(collection: str = "scl") -> list[dict]:
    """Lista todos os periódicos da coleção Brasil. Cache em journals/list.json."""
    cache_path = os.path.join(CACHE_DIR, "journals", "list.json")
    if os.path.isfile(cache_path):
        with open(cache_path) as f:
            return json.load(f)
    print("Listando periódicos da coleção Brasil ...")
    out: list[dict] = []
    offset = 0
    while True:
        page = _get("/journal/identifiers/", {
            "collection": collection, "limit": 1000, "offset": offset
        })
        out.extend(page.get("objects", []))
        total = page.get("meta", {}).get("total", 0)
        offset += 1000
        if offset >= total:
            break
    with open(cache_path, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"  {len(out)} periódicos catalogados")
    return out


def carregar_periodico(issn: str, collection: str = "scl") -> dict | None:
    """Fetch metadata de um periódico (subject_areas etc.). Cache por ISSN.

    Se o JSON em cache estiver corrompido (truncamento por queda de rede,
    interrupção do processo etc.), apaga e refaz.
    """
    cache_path = os.path.join(CACHE_DIR, "journals", f"{issn}.json")
    if os.path.isfile(cache_path):
        try:
            with open(cache_path) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            sys.stderr.write(f"[cache corrompido journal {issn}, refazendo] {e}\n")
            try:
                os.remove(cache_path)
            except OSError:
                pass
    try:
        data = _get("/journal/", {"collection": collection, "issn": issn})
        with open(cache_path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return data
    except Exception as e:
        sys.stderr.write(f"[skip journal {issn}] {e}\n")
        return None


def filtrar_periodicos_humanas(periodicos: list[dict], todas_as_areas: bool = False) -> list[dict]:
    """Mantém só periódicos cujas subject_areas tocam Humanas/Sociais Aplicadas/Letras.

    Se todas_as_areas=True, NÃO filtra por área — devolve todos os periódicos
    com suas subject_areas anotadas. Útil para análises panorâmicas do
    universo SciELO Brasil.
    """
    if todas_as_areas:
        print(f"Modo todas-as-áreas: coletando metadados de TODOS os periódicos...")
    else:
        print(f"Identificando periódicos em áreas-alvo (Humanas + Sociais Aplicadas + Letras)...")
    relevantes = []
    for p in periodicos:
        issn = p.get("code")
        if not issn:
            continue
        meta = carregar_periodico(issn)
        if not meta:
            continue
        # xylose espera lista; mas a API às vezes retorna dict direto
        if isinstance(meta, list):
            meta = meta[0] if meta else {}
        title_obj = meta.get("title") or {}
        # subject_areas costuma vir em v441
        areas = []
        for key in ("v441", "subject_areas"):
            v = title_obj.get(key) or meta.get(key)
            if isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        areas.append(item.get("_") or item.get("value") or "")
                    else:
                        areas.append(str(item))
        areas = [a.strip() for a in areas if a.strip()]
        if todas_as_areas or (set(areas) & SUBJECT_AREAS_ALVO):
            relevantes.append({
                "issn": issn,
                "subject_areas": areas,
                "raw": meta,
            })
    if todas_as_areas:
        print(f"  {len(relevantes)} periódicos no total (todas as áreas)")
    else:
        print(f"  {len(relevantes)} periódicos em áreas-alvo")
    return relevantes


def listar_pids_periodico(issn: str, date_from: str, date_until: str,
                          collection: str = "scl") -> Iterator[str]:
    """Itera PIDs de um periódico no período. Use date_from='' para tudo."""
    offset = 0
    while True:
        params = {"collection": collection, "issn": issn,
                  "limit": 1000, "offset": offset}
        if date_from:
            params["from"] = date_from
        if date_until:
            params["until"] = date_until
        page = _get("/article/identifiers/", params)
        for obj in page.get("objects", []):
            yield obj["code"]
        total = page.get("meta", {}).get("total", 0)
        offset += 1000
        if offset >= total:
            break


def carregar_artigo(pid: str, collection: str = "scl") -> dict | None:
    """Fetch full article metadata. Cache por PID.

    Se o JSON em cache estiver corrompido (truncamento por queda de rede,
    interrupção do processo etc.), apaga e refaz.
    """
    cache_path = os.path.join(CACHE_DIR, "articles", f"{pid}.json")
    if os.path.isfile(cache_path):
        try:
            with open(cache_path) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            sys.stderr.write(f"[cache corrompido article {pid}, refazendo] {e}\n")
            try:
                os.remove(cache_path)
            except OSError:
                pass
    try:
        data = _get("/article/", {"code": pid, "collection": collection, "format": "xylose"})
        with open(cache_path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return data
    except Exception as e:
        sys.stderr.write(f"[skip article {pid}] {e}\n")
        return None


# Os artigos vêm em formato ISIS2JSON. Os campos relevantes:
# v12 = título original / traduções
# v83 = resumo
# v85 = palavras-chave
# v40 = idioma original
# v65 = data publicação (YYYYMM)
# v100 / v480 = ISSN / journal title
# title.v100 = título do journal
# title.v441 = subject_areas

def extrair_campos_artigo(art: dict) -> dict:
    """Pega título + resumo + keywords + metadados de um artigo SciELO."""
    art_obj = art.get("article") or art  # depende da forma do retorno

    def _flat_list(val):
        if val is None: return []
        if isinstance(val, list):
            out = []
            for item in val:
                if isinstance(item, dict):
                    out.append(item.get("_") or item.get("text") or "")
                else:
                    out.append(str(item))
            return [x for x in out if x]
        return [str(val)]

    titulos = _flat_list(art_obj.get("v12") or [])
    resumos = _flat_list(art_obj.get("v83") or [])
    keywords = _flat_list(art_obj.get("v85") or [])
    idioma = (_flat_list(art_obj.get("v40")) or ["?"])[0]
    pubdate = (_flat_list(art_obj.get("v65")) or [""])[0]
    ano = pubdate[:4] if pubdate else ""
    pid = (_flat_list(art_obj.get("v880")) or _flat_list(art_obj.get("v881")) or [""])[0]
    if not pid:
        # algumas respostas trazem "code" no nível raiz
        pid = art.get("code", "")

    title_obj = art.get("title") or {}
    journal_titulo = (_flat_list(title_obj.get("v100"))
                      or _flat_list(art_obj.get("v100"))
                      or [""])[0]
    journal_issn = (_flat_list(title_obj.get("v400"))
                    or _flat_list(art_obj.get("v400"))
                    or [""])[0]
    subject_areas_raw = title_obj.get("v441") or []
    subject_areas = "; ".join(_flat_list(subject_areas_raw))

    return {
        "pid": pid,
        "titulo": " | ".join(titulos),
        "resumo": " | ".join(resumos),
        "keywords": " | ".join(keywords),
        "ano": ano,
        "idioma": idioma,
        "periodico": journal_titulo,
        "issn": journal_issn,
        "subject_areas": subject_areas,
        # texto para classificação
        "_texto_classif": " | ".join(titulos + resumos + keywords),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from", dest="date_from", default="2021-01-01",
                        help="Data inicial (default 2021-01-01)")
    parser.add_argument("--until", dest="date_until", default="2024-12-31",
                        help="Data final (default 2024-12-31)")
    parser.add_argument("--periodo-completo", action="store_true",
                        help="Sem janela de datas; coleta tudo na fonte")
    parser.add_argument("--todas-as-areas", action="store_true",
                        help=("Coleta o universo SciELO Brasil completo (todas as "
                              "subject_areas), não só Humanas+Sociais Aplicadas+Letras. "
                              "Atenção: muito mais lento (várias horas) e ocupa muito "
                              "mais espaço em cache."))
    args = parser.parse_args()
    if args.periodo_completo:
        args.date_from = ""
        args.date_until = ""

    print(f"=== ArticleMeta — coleção 'scl' (Brasil) ===")
    if args.date_from or args.date_until:
        print(f"Janela: {args.date_from or 'início'} → {args.date_until or 'fim'}")
    else:
        print("Janela: histórico completo")
    if args.todas_as_areas:
        print("Modo: TODAS as subject_areas (universo completo do SciELO Brasil)")
    else:
        print("Modo: áreas-alvo (Human Sciences + Applied Social Sciences + Linguistics, Letters and Arts)")

    # 1) Periódicos da coleção
    periodicos = listar_periodicos()

    # 2) Filtra (ou não) por áreas
    relevantes = filtrar_periodicos_humanas(periodicos, todas_as_areas=args.todas_as_areas)

    # 3) Itera artigos
    registros = []
    for i, p in enumerate(relevantes, 1):
        issn = p["issn"]
        print(f"  [{i}/{len(relevantes)}] {issn} ({', '.join(p['subject_areas'])})")
        pids = list(listar_pids_periodico(issn, args.date_from, args.date_until))
        print(f"    {len(pids)} artigos no período")
        for pid in pids:
            art = carregar_artigo(pid)
            if not art:
                continue
            campos = extrair_campos_artigo(art)
            # Anexa subject_areas do periódico (mais confiável)
            campos["subject_areas_periodico"] = "; ".join(p["subject_areas"])
            registros.append(campos)

    df = pd.DataFrame(registros)
    print(f"\nTotal coletado: {len(df):,} artigos")

    # 4) Classifica
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

    # 5) Salva universo + subset IA. Nome de saída depende do modo.
    df = df.drop(columns=["_texto_classif"])
    if args.todas_as_areas:
        out_universo = os.path.join(DADOS_SCIELO_DIR, "scielo_brasil_universo.csv")
        out_ia = os.path.join(DADOS_SCIELO_DIR, "scielo_brasil_ia_subcampos.csv")
        out_xlsx = os.path.join(DADOS_SCIELO_DIR, "scielo_brasil_ia_subcampos_auditoria.xlsx")
        rotulo = "Brasil SciELO completo"
    else:
        out_universo = os.path.join(DADOS_SCIELO_DIR, "scielo_humanas_universo.csv")
        out_ia = os.path.join(DADOS_SCIELO_DIR, "scielo_ia_subcampos.csv")
        out_xlsx = os.path.join(DADOS_SCIELO_DIR, "scielo_ia_subcampos_auditoria.xlsx")
        rotulo = "Humanas + Sociais Aplicadas + Letras"

    df.to_csv(out_universo, index=False)
    print(f"Universo ({rotulo}) salvo em {out_universo}")
    print(f"Distribuição FOCO_IA:")
    print(df["FOCO_IA"].value_counts().to_string())

    ia = df[df["FOCO_IA"] != "Outros Temas"].copy()
    ia.to_csv(out_ia, index=False)
    print(f"\nSubset IA salvo em {out_ia} ({len(ia)} artigos)")

    if len(ia):
        ia.to_excel(out_xlsx, index=False, engine="openpyxl")
        print(f"XLSX para auditoria: {out_xlsx}")


if __name__ == "__main__":
    main()
