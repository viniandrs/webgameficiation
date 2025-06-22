# src/utilidades_banco_dados.py

"""
Módulo responsável por fornecer funções utilitárias para gerenciar a conexão com o banco de dados
"""

import sqlite3
import os

# Definição do caminho do banco de dados
CAMINHO_DIR_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_RAIZ = os.path.abspath(os.path.join(CAMINHO_DIR_ATUAL, os.pardir))
CAMINHO_BD = os.path.join(CAMINHO_RAIZ, "dados", "bd_projeto.db")


def obter_conexao():
    """
    Retorna uma nova conexão com o banco de dados

    Returns:
      sqlite3.Connection: Um objeto de conexão com o banco de dados

    Raises:
      sqlite3.Error: Se ocorrer um erro específico do SQLite ao tentar estabelecer a conexão com o banco de dados
    """
    try:
        # Estabelece a conexão com o banco de dados
        conexao = sqlite3.connect(CAMINHO_BD)

        # Permite que as linhas retornadas se comportem como dicionários
        conexao.row_factory = sqlite3.Row

        return conexao
    except sqlite3.Error as e:
        print(
            f"Erro ao conectar com banco de dados usando o caminho '{CAMINHO_BD}': {e}"
        )
        raise


def obter_conexao_teste():
    """
    Retorna uma conexão com um banco de dados SQLite em memória (não persistente).
    """
    conexao = sqlite3.connect(":memory:")
    conexao.row_factory = sqlite3.Row
    return conexao


# Teste de sanidade para a conexão com banco de dados
if __name__ == "__main__":
    print(f"Tentando conectar ao banco de dados em: {CAMINHO_BD}")
    try:
        conn = obter_conexao()
        print("Conexão com o banco de dados estabelecida com sucesso!")
        # Cria um cursor para garantir que a conexão está ativa
        cursor = conn.cursor()
        cursor.close()
        conn.close()
        print("Conexão fechada.")
    except sqlite3.Error as e:
        print(f"Falha ao conectar ao banco de dados: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
