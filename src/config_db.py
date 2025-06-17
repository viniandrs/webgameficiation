#src/config_db.py

"""
Módulo responsável pela configuração inicial do banco de dados, incluindo a criação de tabelas
"""

import sqlite3
from .utilidades_db import obter_conexao

def criar_tabelas(caminho: str):
  """
  Cria as tabelas necessárias no banco de dados SQLite
  
  Args:
  - caminho (str): caminho completo para o banco de dados, caso não existam.
  """
  
  #Tabela com as strings SQL para a criação das tabelas
  sql_tabelas = [
    """
    CREATE TABLE IF NOT EXISTS usuarios (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nome TEXT NOT NULL,
      email TEXT UNIQUE NOT NULL,
      senha TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS projetos (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nome TEXT NOT NULL,
      descricao TEXT,
      xp_acumulado REAL NOT NULL DEFAULT 0.0,
      xp_meta REAL NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS participacoes (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      usuario_id INTEGER NOT NULL,
      projeto_id INTEGER NOT NULL,
      xp_participacao REAL NOT NULL DEFAULT 0.0,
      participacao_habilitada BOOLEAN NOT NULL,
      classificacao TEXT NOT NULL,
      UNIQUE(usuario_id, projeto_id),
      FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE ON UPDATE CASCADE,
      FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE ON UPDATE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS tarefas (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      projeto_id INTEGER NOT NULL,
      titulo TEXT NOT NULL,
      descricao TEXT,
      xp_valor REAL NOT NULL,
      status TEXT NOT NULL,
      participacao_responsavel_id INTEGER,
      prazo TEXT, -- Formato ISO 8601 YYYY-MM-DD HH:MM:SS
      sprint_meta_id INTEGER,
      FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE ON UPDATE CASCADE,
      FOREIGN KEY (participacao_responsavel_id) REFERENCES participacoes(id) ON DELETE SET NULL ON UPDATE CASCADE,
      FOREIGN KEY (sprint_meta_id) REFERENCES sprint_metas(id) ON DELETE SET NULL ON UPDATE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS sprint_metas (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      projeto_id INTEGER NOT NULL,
      nome TEXT NOT NULL,
      descricao TEXT,
      xp_bonus REAL NOT NULL DEFAULT 0.0,
      status TEXT NOT NULL,
      data_alvo TEXT, -- Formato ISO 8601 YYYY-MM-DD HH:MM:SS
      FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE ON UPDATE CASCADE
    );
    """
  ]

  try:
    with obter_conexao() as conexao:
      cursor = conexao.cursor()
      for sql in sql_tabelas:
        cursor.execute(sql)
      print("Tabelas criadas com sucesso")
  except sqlite3.Error as e:
    print(f"Erro ao criar tabelas: {e}")

