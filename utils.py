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


# Núcleo de termos de IA com alta precisão. Sem 'IA' isolado (tratado por
# co-ocorrência), sem 'algoritmo' (falso positivo enorme fora das humanas).
# Estes termos definem o vocabulário canônico do campo: presença de qualquer
# um deles num título/resumo basta para classificar como foco em IA.
RE_IA_NUCLEO = re.compile(
    r'\b('
    r'inteligência\s+artificial|inteligencia\s+artificial|'
    r'artificial\s+intelligence|'
    r'machine\s+learning|aprendizado\s+de\s+máquina|aprendizado\s+de\s+maquina|'
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

# 'IA' como sigla. Só conta como IA central se também houver um termo do
# núcleo ou da lista relacionada no mesmo texto — caso contrário, gera muitos
# falsos positivos (Iniciação Científica, Imposto Adicional, Inteligência de
# Mercado, nomes próprios, etc).
RE_IA_SIGLA = re.compile(r'\b(ia|i\.a\.)\b', flags=re.IGNORECASE)

# "Foco relacionado": termos vizinhos do campo que sozinhos não bastam para
# afirmar que a tese é "sobre IA", mas que indicam adjacência conceitual.
# Mantido conservador, sem 'dados', 'internet', 'online', 'virtual',
# 'computacional' (falsos positivos enormes em humanas).
RE_IA_RELACIONADA = re.compile(
    r'\b('
    r'transhumanismo|pós-humanismo|pos-humanismo|'
    r'robótica|robotica|robôs|robos|'
    r'automação|automacao|automation|'
    r'mineração\s+de\s+dados|mineracao\s+de\s+dados|data\s+mining|'
    r'big\s+data|'
    r'visão\s+computacional|visao\s+computacional|computer\s+vision|'
    r'processamento\s+de\s+linguagem\s+natural|natural\s+language\s+processing|nlp'
    r')\b',
    flags=re.IGNORECASE,
)

# Alias retrocompatível: scripts antigos usam RE_IA_FORTE.
RE_IA_FORTE = RE_IA_NUCLEO


def classificar_foco_ia(texto):
    """Classifica um texto em três categorias quanto ao foco em IA.

    A categoria 'IA - Foco Central' é atribuída se há termo do núcleo OU se
    a sigla 'IA' aparece em co-ocorrência com termo do núcleo/relacionado no
    mesmo texto. A regra de co-ocorrência reduz drasticamente falsos positivos
    em grandes áreas onde 'IA' tem outros significados.

    Retorna uma das strings: 'IA - Foco Central', 'IA - Foco Relacionado',
    'Outros Temas'.
    """
    if not texto or isinstance(texto, float):
        return 'Outros Temas'
    s = str(texto)
    if RE_IA_NUCLEO.search(s):
        return 'IA - Foco Central'
    if RE_IA_RELACIONADA.search(s):
        # Sigla 'IA' + termo relacionado = foco central (ex.: "IA e robótica").
        if RE_IA_SIGLA.search(s):
            return 'IA - Foco Central'
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
