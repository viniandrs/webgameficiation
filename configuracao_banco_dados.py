# src/configuracao_banco_dados.py

"""
Módulo responsável pela configuração inicial do banco de dados, incluindo a criação de tabelas
"""

import sqlite3
from models.utils import obter_conexao

# Tabela com as strings SQL para a criação das tabelas
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
    xp_acumulado INT NOT NULL DEFAULT 0,
    xp_meta INT NOT NULL DEFAULT 0
  );
  """,
    """
  CREATE TABLE IF NOT EXISTS participacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    projeto_id INTEGER NOT NULL,
    xp_participacao INT NOT NULL DEFAULT 0,
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
    xp_valor INT NOT NULL,
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
    xp_bonus INT NOT NULL DEFAULT 0.0,
    status TEXT NOT NULL,
    data_alvo TEXT, -- Formato ISO 8601 YYYY-MM-DD HH:MM:SS
    FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE ON UPDATE CASCADE
  );
  """,
]


def criar_tabelas():
    """
    Cria as tabelas necessárias no banco de dados SQLite
    """
    try:
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            for sql in sql_tabelas:
                cursor.execute(sql)
            print("Tabelas criadas com sucesso")
    except sqlite3.Error as e:
        print(f"Erro ao criar tabelas: {e}")


def criar_tabelas_em_conexao(conexao):
    cursor = conexao.cursor()
    for sql in sql_tabelas:
        cursor.execute(sql)


def apagar_tabelas_em_conexao(conexao):
    cursor = conexao.cursor()
    # Ordem reversa para evitar problemas de chave estrangeira
    sql_drop_tabelas = [
        "DROP TABLE IF EXISTS sprint_metas;",
        "DROP TABLE IF EXISTS tarefas;",
        "DROP TABLE IF EXISTS participacoes;",
        "DROP TABLE IF EXISTS projetos;",
        "DROP TABLE IF EXISTS usuarios;",
    ]
    for sql in sql_drop_tabelas:
        cursor.execute(sql)


# Teste de sanidade para a criação de tabelas
if __name__ == "__main__":
    print("Executando teste de criação de tabelas")
    try:
        criar_tabelas()
        print("Teste de criação de tabelas concluído.")
    except sqlite3.Error as e:
        print(f"Erro no teste de criação de tabelas: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante a criação das tabelas: {e}")
