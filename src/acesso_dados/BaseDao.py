# src/acesso_dados/BaseDao.py

import sqlite3
from abc import ABC, abstractmethod
from ..utilidades_banco_dados import obter_conexao

class BaseDao:
  """
  Classe base abstrata para todas as operações com o banco de dados (CRUD)
  """

  def __init__(self):
    """
    Inicializa a classe BaseDao
    """
    pass
  
  #Métodos genéricos para interação com a base de dados

  def _executar_consulta(self, sql: str, parametros = None):
    """
    Executa uma consulta na base de dados que não retorna resultados, como Insert, Update e Delete.

    Args:
      sql (str): String SQL a ser executada
      parametros (tuple): Tupla de parâmetros para a consulta, None como padrão

    Raises:
      sqlite3.Error: Se ocorrer um erro durante a execução da consulta
    """

    try:
      with obter_conexao() as conexao:
        cursor = conexao.cursor()
        if(parametros):
          cursor.execute(sql, parametros)
        else:
          cursor.execute(sql)
    except sqlite3.Error as e:
      print(f"Erro ao executar consulta SQL: {sql}.\nErro: {e}")
      raise
  
  def _obter_um(self, sql: str, parametros = None):
    """
    Executa uma consulta que tenta obter um registro da base de dados
    
    Args: 
      sql (str): String SQL a ser executada
      parametros (tuple): Tupla de parâmetros para a consulta, None como padrão

    Returns:
      sqlite3.Row ou None: Resultado da consulta como um objeto sqlite3.Row ou None, caso não tenha resultado

    Raises:
      sqlite3.Error: Se ocorrer algum erro durante a execução da consulta
    """
    
    try:
      with obter_conexao() as conexao:
        cursor = conexao.cursor()
        if(parametros):
          cursor.execute(sql, parametros)
        else:
          cursor.execute(sql)
        return cursor.fetchone()
    except sqlite3.Error as e:
      print(f"Erro ao obter resultado SQL: {sql}\n. Erro: {e}")
      raise
  
  def _obter_todos(self, sql:str, parametros = None):
    """
    Executa uma consulta que tenta obter múltiplos registros da base de dados

    Args: 
      sql (str): String SQL a ser executada
      parametros (tuple): Tupla de parâmetros para a consulta, None como padrão

    Returns:
      lista de sqlite3.Row ou None: Resultado da consulta como uma lista de objetos sqlite3.Row ou None, caso não tenha resultado

    Raises:
      sqlite3.Error: Se ocorrer algum erro durante a execução da consulta
    """
    
    try:
      with obter_conexao() as conexao:
        cursor = conexao.cursor()
        if(parametros):
          cursor.execute(sql, parametros)
        else:
          cursor.execute(sql)
        return cursor.fetchall()
    except sqlite3.Error as e:
      print(f"Erro ao obter resultado SQL: {sql}\n. Erro: {e}")
      raise