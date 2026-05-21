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
    """Estilo único compartilhado entre todos os gráficos.

    Segue o "padrão Python" enxuto: defaults do matplotlib + grade discreta,
    sem bordas grossas, sem títulos em negrito enfático, sem cores saturadas
    fora da paleta tab10. Pensado para reprodução em texto acadêmico.
    """
    plt.style.use('default')
    sns.set_style("whitegrid")
    # Paleta default do matplotlib (tab10) — sóbria e reconhecível.
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.tab10.colors)
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['savefig.facecolor'] = 'white'
    plt.rcParams['savefig.edgecolor'] = 'none'
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 300
    # Tipografia: tamanhos consistentes, sem bold gratuito.
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 11
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['axes.titleweight'] = 'normal'
    plt.rcParams['axes.labelweight'] = 'normal'
    plt.rcParams['legend.fontsize'] = 9
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
    # Spines: só esquerda e baixo, padrão de publicação.
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['grid.linewidth'] = 0.5


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


# =============================================================================
# Subcampos: reconhece que IA, ML, deep learning, LLMs e tecnologias correlatas
# têm genealogias e comunidades epistêmicas distintas. Cada subcampo é definido
# por seu próprio regex; um trabalho pode pertencer a mais de um subcampo
# simultaneamente. A coleção destes subcampos forma o que chamamos de
# "Tecnologias de IA, ML e aprendizado profundo" — rótulo descritivo, não
# afirmação de identidade entre os campos.
# =============================================================================

RE_SUBCAMPO_IA_STRICT = re.compile(
    r'\b('
    r'intelig[êe]ncia\s+artificial|artificial\s+intelligence'
    r')\b',
    flags=re.IGNORECASE,
)

RE_SUBCAMPO_ML = re.compile(
    r'\b('
    r'machine\s+learning|'
    r'aprendizado\s+de\s+m[áa]quina'
    r')\b',
    flags=re.IGNORECASE,
)

RE_SUBCAMPO_DL = re.compile(
    r'\b('
    r'deep\s+learning|aprendizado\s+profundo|'
    r'redes?\s+neurais|neural\s+networks?'
    r')\b',
    flags=re.IGNORECASE,
)

RE_SUBCAMPO_LLM = re.compile(
    r'\b('
    r'llms?|large\s+language\s+models?|'
    r'modelos?\s+de\s+linguagem|'
    r'transformer[s]?|'
    r'chatgpt|gpt-\d|'
    r'ia\s+generativa|generative\s+ai'
    r')\b',
    flags=re.IGNORECASE,
)

RE_SUBCAMPO_CORRELATOS = re.compile(
    r'\b('
    r'transhumanismo|p[óo]s-humanismo|'
    r'rob[óo]tica|rob[ôo]s|'
    r'automa[çc][ãa]o|automation|'
    r'minera[çc][ãa]o\s+de\s+dados|data\s+mining|'
    r'big\s+data|'
    r'vis[ãa]o\s+computacional|computer\s+vision|'
    r'processamento\s+de\s+linguagem\s+natural|natural\s+language\s+processing|nlp'
    r')\b',
    flags=re.IGNORECASE,
)

# Ordem é didática: do mais "alto nível" (IA conceito) até o mais "técnico"
# (correlatos). Os primeiros 4 são canonicamente IA/ML/DL/LLMs; o 5º agrupa
# tecnologias adjacentes que circulam no entorno mas não são equivalentes.
SUBCAMPOS = [
    ("IA em sentido estrito", RE_SUBCAMPO_IA_STRICT),
    ("Aprendizado de máquina (ML)", RE_SUBCAMPO_ML),
    ("Aprendizado profundo & redes neurais", RE_SUBCAMPO_DL),
    ("Modelos de linguagem & IA generativa", RE_SUBCAMPO_LLM),
    ("Tecnologias correlatas (robótica, NLP, big data…)", RE_SUBCAMPO_CORRELATOS),
]

# Subcampos "centrais" (1-4) vs "correlato" (5). Útil para preservar a
# distinção Central / Correlato sem aglutinar IA com ML/DL/LLMs.
SUBCAMPOS_CENTRAIS = [s for s, _ in SUBCAMPOS[:4]]
SUBCAMPO_CORRELATOS = SUBCAMPOS[4][0]


def classificar_subcampos(texto):
    """Retorna o conjunto de subcampos que aparecem no texto.

    Um trabalho pode estar em zero, um ou vários subcampos. A presença
    do conjunto vazio indica que o trabalho não toca o campo coberto
    pelo regex e fica em 'Outros Temas'.
    """
    if not texto or isinstance(texto, float):
        return set()
    s = str(texto)
    return {label for label, padrao in SUBCAMPOS if padrao.search(s)}


# Núcleo (mantido para retrocompatibilidade): união dos 4 subcampos centrais.
# Estes termos definem o vocabulário canônico das tecnologias de IA/ML/DL/LLMs.
RE_IA_NUCLEO = re.compile(
    r'\b('
    r'intelig[êe]ncia\s+artificial|artificial\s+intelligence|'
    r'machine\s+learning|aprendizado\s+de\s+m[áa]quina|'
    r'deep\s+learning|aprendizado\s+profundo|'
    r'redes?\s+neurais|neural\s+networks?|'
    r'modelos?\s+de\s+linguagem|'
    r'large\s+language\s+models?|llms?|'
    r'transformer[s]?|'
    r'chatgpt|gpt-\d|'
    r'ia\s+generativa|generative\s+ai'
    r')\b',
    flags=re.IGNORECASE,
)

# 'IA' como sigla. Só conta como central se coocorrer com termo do núcleo
# ou correlatos no mesmo texto (regra de co-ocorrência).
RE_IA_SIGLA = re.compile(r'\b(ia|i\.a\.)\b', flags=re.IGNORECASE)

# Alias retrocompatível: scripts antigos usam RE_IA_FORTE / RE_IA_RELACIONADA.
RE_IA_FORTE = RE_IA_NUCLEO
RE_IA_RELACIONADA = RE_SUBCAMPO_CORRELATOS


def classificar_foco_ia(texto):
    """Classifica um texto em três categorias quanto ao foco no campo.

    Importante: o rótulo guarda-chuva NÃO afirma que IA, ML, DL, LLMs e
    correlatos são a mesma coisa. Ele apenas agrupa, para fins de
    contagem total, trabalhos que mencionam qualquer uma dessas
    tecnologias. A subcategorização real fica em classificar_subcampos.

    Retorna uma das strings:
      - 'Tecnologias IA/ML/DL - Foco Central'
        (mencionou IA, ML, DL ou LLMs — i.e., algum subcampo central)
      - 'Tecnologias IA/ML/DL - Correlato'
        (mencionou só tecnologias correlatas, ou só a sigla 'IA' sem
        co-ocorrência)
      - 'Outros Temas'
    """
    if not texto or isinstance(texto, float):
        return 'Outros Temas'
    s = str(texto)
    if RE_IA_NUCLEO.search(s):
        return 'Tecnologias IA/ML/DL - Foco Central'
    if RE_SUBCAMPO_CORRELATOS.search(s):
        # Sigla 'IA' + correlato = central (ex.: "IA e robótica").
        if RE_IA_SIGLA.search(s):
            return 'Tecnologias IA/ML/DL - Foco Central'
        return 'Tecnologias IA/ML/DL - Correlato'
    return 'Outros Temas'


# Rótulo guarda-chuva descritivo, sem afirmar identidade entre os campos.
LABEL_GUARDA_CHUVA = "Tecnologias de IA, ML e aprendizado profundo"
LABEL_GUARDA_CHUVA_CURTO = "Tecnologias IA/ML/DL"


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
