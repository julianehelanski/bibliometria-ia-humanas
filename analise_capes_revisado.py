# -*- coding: utf-8 -*-
"""
ANÁLISE CAPES (VERSÃO OTIMIZADA)
Melhorias: Tratamento de Erros, Regex para IA e Caminhos Relativos.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re

# Configuração de Ambiente
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
GRAFICOS_DIR = os.path.join(BASE_DIR, 'graficos')
if not os.path.exists(GRAFICOS_DIR):
    os.makedirs(GRAFICOS_DIR)

def limpar_e_analisar_capes(caminho_csv):
    try:
        # Load com encoding flexível
        df = pd.read_csv(caminho_csv, encoding='utf-8', sep=None, engine='python')
    except Exception as e:
        print(f"Erro ao ler CSV: {e}")
        return

    # Normalização de Colunas
    df.columns = [c.lower().strip() for c in df.columns]
    
    # Regex robusto para IA
    re_ia = re.compile(r'\b(ia|inteligência artificial|machine learning|aprendizado de máquina)\b', re.IGNORECASE)
    
    def identificar_ia(row):
        texto = str(row.get('titulo', '')) + " " + str(row.get('resumo', ''))
        return 'Sim' if re_ia.search(texto) else 'Não'

    df['foco_ia'] = df.apply(identificar_ia, axis=1)

    # Gráfico de Foco IA
    plt.figure(figsize=(8, 8))
    counts = df['foco_ia'].value_counts()
    plt.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=['#ecf0f1', '#e74c3c'], startangle=140)
    plt.title('Proporção de Teses com Foco em IA (CAPES)')
    plt.savefig(os.path.join(GRAFICOS_DIR, '01_proporcao_ia_capes.png'))
    plt.close()

    print(f"Análise CAPES concluída. Gráficos salvos em: {GRAFICOS_DIR}")

if __name__ == "__main__":
    # Exemplo de chamada (ajuste o nome do seu arquivo CSV da CAPES aqui)
    arquivo_alvo = os.path.join(BASE_DIR, 'dados_capes.csv') 
    if os.path.exists(arquivo_alvo):
        limpar_e_analisar_capes(arquivo_alvo)
    else:
        print("Aguardando arquivo 'dados_capes.csv' na pasta do script.")
