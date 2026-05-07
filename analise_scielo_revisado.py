# -*- coding: utf-8 -*-
"""
ANÁLISE BIBLIOMÉTRICA: ARTIGOS SCIELO (VERSÃO OTIMIZADA)
Melhorias: Uso de Pandas, Caminhos Relativos, Regex Compilado e Robustez.
"""

import re
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Configurações de Estilo
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 10

# Caminhos Relativos (Melhor para VS Code/GitHub)
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
OUTPUT_DIR = os.path.join(BASE_DIR, 'resultados_analise')
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Expressões Regulares Compiladas (Performance)
RE_YEAR = re.compile(r'^PY  - (\d{4})', re.MULTILINE)
RE_LANG = re.compile(r'^LA  - (\w+)', re.MULTILINE)
RE_JOURNAL = re.compile(r'^T2  - (.*)', re.MULTILINE)

def verificar_foco_ia(texto):
    if not texto: return False
    texto = texto.lower()
    keywords = ['inteligência artificial', 'artificial intelligence', 'machine learning', 
                'aprendizado de máquina', 'deep learning', 'neural networks', 'redes neurais',
                'llm', 'chatgpt', 'nlp', 'processamento de linguagem natural']
    return any(kw in texto for kw in keywords)

def processar_scielo():
    ris_path = os.path.join(BASE_DIR, 'export_scielo.ris')
    if not os.path.exists(ris_path):
        print(f"Erro: Arquivo {ris_path} não encontrado.")
        return

    with open(ris_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    records = content.split('ER  -')
    data = []

    for record in records:
        if not record.strip(): continue
        
        year_match = RE_YEAR.search(record)
        lang_match = RE_LANG.search(record)
        jrnl_match = RE_JOURNAL.search(record)
        
        year = year_match.group(1) if year_match else "N/A"
        lang = lang_match.group(1) if lang_match else "Outro"
        journal = jrnl_match.group(1).strip() if jrnl_match else "Desconhecido"
        
        is_ia = verificar_foco_ia(record)
        
        data.append({
            'ano': year,
            'idioma': lang,
            'journal': journal,
            'foco_ia': 'Sim' if is_ia else 'Não'
        })

    df = pd.DataFrame(data)
    
    # Gerar Gráfico de Evolução Temporal
    plt.figure(figsize=(10, 6))
    df_plot = df[df['ano'] != "N/A"].groupby(['ano', 'foco_ia']).size().unstack(fill_value=0)
    df_plot.plot(kind='bar', stacked=True, color=['#bdc3c7', '#3498db'])
    plt.title('Evolução de Artigos: Geral vs Foco IA (SciELO)')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '01_evolucao_ia_scielo.png'))
    plt.close()

    print(f"Análise SciELO concluída. Resultados em: {OUTPUT_DIR}")

if __name__ == "__main__":
    processar_scielo()
