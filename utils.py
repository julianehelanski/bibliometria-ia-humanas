# -*- coding: utf-8 -*-
"""
Utilitários compartilhados entre os scripts de análise bibliométrica.

Centraliza:
- Estilo e paleta dos gráficos
- Regex de identificação de IA (com word boundaries)
- Lista de stopwords em português
- Detecção de diretórios de dados/saída em caminhos relativos
"""

import os
import re

import matplotlib.pyplot as plt
import seaborn as sns


# Caminhos relativos ao repositório
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_SCIELO_DIR = os.path.join(BASE_DIR, 'dados_scielo')
DADOS_CAPES_DIR = os.path.join(BASE_DIR, 'dados_capes')
FIGURAS_DIR = os.path.join(BASE_DIR, 'figuras')


def aplicar_estilo_padrao():
    """Estilo único compartilhado entre todos os gráficos."""
    plt.style.use('default')
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (14, 8)
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['savefig.facecolor'] = 'white'
    plt.rcParams['savefig.edgecolor'] = 'none'
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 13
    plt.rcParams['axes.labelsize'] = 11
    plt.rcParams['axes.titleweight'] = 'bold'


# Paleta usada por ambos os scripts
CORES_INTERMEDIARIAS = [
    '#E57373',  # 0: Muted Red
    '#FFB74D',  # 1: Muted Orange
    '#81C784',  # 2: Muted Green
    '#64B5F6',  # 3: Muted Blue
    '#BA68C8',  # 4: Muted Purple
    '#FFF176',  # 5: Muted Yellow
    '#F06292',  # 6: Muted Pink
    '#4DB6AC',  # 7: Muted Teal
    '#A1887F',  # 8: Muted Brown
    '#90A4AE',  # 9: Muted Blue-Gray
    '#B0BEC5',  # 10: Light Muted Gray
    '#E0E0E0',  # 11: Very Light Gray
]


# Regex de IA: \b garante limites de palavra, evitando capturar "ia" dentro de
# "via", "tecnologia", "história" etc. Sem \b, a string "ia " falharia em
# títulos onde "IA" aparece com pontuação ("...da IA.", "...da IA,").
RE_IA_FORTE = re.compile(
    r'\b('
    r'ia|'
    r'i\.a\.|'
    r'inteligência\s+artificial|inteligencia\s+artificial|'
    r'artificial\s+intelligence|'
    r'machine\s+learning|aprendizado\s+de\s+máquina|aprendizado\s+de\s+maquina|'
    r'deep\s+learning|aprendizado\s+profundo|'
    r'redes?\s+neurais|neural\s+networks?|'
    r'chatgpt|gpt|llm|llms|'
    r'algoritmo[s]?|algorithm[s]?'
    r')\b',
    flags=re.IGNORECASE
)

# "Foco relacionado" agora é mais estrito: removidos 'dados', 'internet',
# 'online', 'virtual', 'computacional' que produziam falsos positivos enormes
# (qualquer tese sobre redes sociais ou pesquisa quantitativa caía aqui).
RE_IA_RELACIONADA = re.compile(
    r'\b('
    r'transhumanismo|pós-humanismo|pos-humanismo|'
    r'robótica|robotica|robôs|robos|'
    r'automação|automacao|automation|'
    r'aprendizado\s+de\s+máquina|'
    r'mineração\s+de\s+dados|mineracao\s+de\s+dados|data\s+mining|'
    r'big\s+data|'
    r'visão\s+computacional|visao\s+computacional|computer\s+vision|'
    r'processamento\s+de\s+linguagem\s+natural|natural\s+language\s+processing|nlp'
    r')\b',
    flags=re.IGNORECASE
)


def classificar_foco_ia(texto):
    """Classifica um texto (título + resumo/keywords) em três categorias.

    Usa regex com word boundaries para reduzir falsos positivos. Retorna uma
    das strings: 'IA - Foco Central', 'IA - Foco Relacionado', 'Outros Temas'.
    """
    if not texto or (isinstance(texto, float)):
        return 'Outros Temas'
    s = str(texto)
    if RE_IA_FORTE.search(s):
        return 'IA - Foco Central'
    if RE_IA_RELACIONADA.search(s):
        return 'IA - Foco Relacionado'
    return 'Outros Temas'


# Stopwords em português, expandida. Cobre artigos, preposições, conjunções,
# pronomes, verbos auxiliares mais comuns e termos vazios típicos de títulos
# acadêmicos ("estudo", "análise", "uma", "sobre" etc.).
STOPWORDS_PT = {
    # Artigos e contrações
    'a', 'o', 'as', 'os', 'um', 'uma', 'uns', 'umas',
    'à', 'às', 'ao', 'aos', 'da', 'do', 'das', 'dos',
    'na', 'no', 'nas', 'nos', 'pela', 'pelo', 'pelas', 'pelos',
    'numa', 'num', 'numas', 'nuns', 'duma', 'dum', 'desta', 'deste',
    'desse', 'dessa', 'daquele', 'daquela', 'isto', 'isso', 'aquilo',
    # Preposições e conjunções
    'de', 'em', 'para', 'por', 'com', 'sem', 'sob', 'sobre',
    'entre', 'até', 'após', 'ante', 'desde', 'durante',
    'e', 'ou', 'mas', 'que', 'se', 'como', 'quando', 'onde',
    'porque', 'pois', 'então', 'assim', 'também', 'ainda',
    # Pronomes e demonstrativos
    'eu', 'tu', 'ele', 'ela', 'nós', 'vós', 'eles', 'elas',
    'este', 'esta', 'esse', 'essa', 'aquele', 'aquela',
    'seu', 'sua', 'seus', 'suas', 'meu', 'minha', 'nosso', 'nossa',
    # Verbos auxiliares e cópulas comuns
    'é', 'são', 'foi', 'foram', 'ser', 'sendo', 'sido',
    'estar', 'está', 'estão', 'estava', 'estavam',
    'ter', 'tem', 'têm', 'tinha', 'tinham', 'há', 'havia',
    # Vazios típicos de títulos acadêmicos
    'estudo', 'estudos', 'análise', 'analise',
    'pesquisa', 'pesquisas', 'trabalho', 'trabalhos',
    'sobre', 'através', 'partir', 'contexto', 'caso', 'casos',
    'uso', 'usos', 'utilização', 'utilizacao',
    'investigação', 'investigacao', 'abordagem', 'abordagens',
    'perspectiva', 'perspectivas', 'reflexão', 'reflexoes', 'reflexão',
}


def garantir_diretorio(caminho):
    """Cria o diretório se não existir. Retorna o caminho."""
    os.makedirs(caminho, exist_ok=True)
    return caminho


def buscar_arquivo(nomes, *diretorios):
    """Procura o primeiro arquivo existente nos diretórios dados.

    Args:
        nomes: lista de nomes possíveis (ex.: ['catalogo.xlsx', 'catalogo.csv']).
        diretorios: diretórios onde buscar, em ordem de prioridade.

    Retorna o caminho absoluto do primeiro arquivo encontrado, ou None.
    """
    for diretorio in diretorios:
        for nome in nomes:
            caminho = os.path.join(diretorio, nome)
            if os.path.isfile(caminho):
                return caminho
    return None
