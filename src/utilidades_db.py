#src/utilidades_db.py

"""
Módulo responsável por fornecer funções utilitárias para gerenciar a conexão com o banco de dados
"""

import sqlite3
import os

#Definição do caminho do banco de dados
CAMINHO_DIR_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_RAIZ = os.path.abspath(os.path.join(CAMINHO_DIR_ATUAL), os.pardir)
CAMINHO_BD = os.path.join(CAMINHO_RAIZ, 'data', 'bd_projeto.db')

def obter_conexao():
  """
  Retorna uma nova conexão com o banco de dados
  """
  try:
    #Estabelece a conexão com o banco de dados
    conexao = sqlite3.connect(CAMINHO_BD)

    #Permite que as linhas retornadas se comportem como dicionários
    conexao.row_factory = sqlite3.Row
    
    return conexao
  except sqlite3.Error as e:
    print(f"Erro ao conectar com banco de dados usando o caminho '{CAMINHO_BD}': {e}")
    raise