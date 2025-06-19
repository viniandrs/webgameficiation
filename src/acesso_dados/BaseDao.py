# src/acesso_dados/BaseDao.py

import sqlite3
from abc import ABC, abstractmethod
from ..utilidades_banco_dados import obter_conexao

class BaseDao(ABC):
  """
  Classe base abstrata para todas as operações com o banco de dados (CRUD)
  """

  def __init__(self):
    """
    Inicializa a classe BaseDao
    """
    super().__init__()
  
  #Métodos genéricos (protegidos) para interação com a base de dados

  def _executar_consulta(self, sql: str, parametros: tuple = None, retornar_lastrowid: bool = False):
    """
    Executa uma consulta na base de dados que não retorna resultados, como Insert, Update e Delete.

    Args:
      sql (str): String SQL a ser executada
      parametros (tuple): Tupla de parâmetros para a consulta, None como padrão
      retornar_lastrowid (bool): se True tenta retornar o último id geraldo.

    Raises:
      sqlite3.Error: Se ocorrer um erro durante a execução da consulta

    Returns:
      int ou None: O último id gerado, caso retornar_latrowid seja True, None caso contrário
    """
    try:
      with obter_conexao() as conexao:
        cursor = conexao.cursor()
        if parametros:
          cursor.execute(sql, parametros)
        else:
          cursor.execute(sql)

        if retornar_lastrowid:
          return cursor.lastrowid
        return None
    except sqlite3.Error as e:
      print(f"Erro ao executar consulta SQL: {sql}.\nErro: {e}")
      raise
  
  def _obter_um(self, sql: str, parametros: tuple = None):
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
        if parametros:
          cursor.execute(sql, parametros)
        else:
          cursor.execute(sql)
        return cursor.fetchone()
    except sqlite3.Error as e:
      print(f"Erro ao obter resultado SQL: {sql}\n. Erro: {e}")
      raise
  
  def _obter_todos(self, sql:str, parametros: tuple = None):
    """
    Executa uma consulta que tenta obter múltiplos registros da base de dados

    Args: 
      sql (str): String SQL a ser executada
      parametros (tuple): Tupla de parâmetros para a consulta, None como padrão

    Returns:
      lista de sqlite3.Row: Resultado da consulta como uma lista de objetos sqlite3.Row ou uma lista vazia caso não tenha resultado

    Raises:
      sqlite3.Error: Se ocorrer algum erro durante a execução da consulta
    """
    try:
      with obter_conexao() as conexao:
        cursor = conexao.cursor()
        if parametros:
          cursor.execute(sql, parametros)
        else:
          cursor.execute(sql)
        return cursor.fetchall()
    except sqlite3.Error as e:
      print(f"Erro ao obter resultado SQL: {sql}\n. Erro: {e}")
      raise

  # Métodos abstratos
  @abstractmethod
  def _obter_nome_tabela(self) -> str:
    """
    Retorna o nome da tabela do banco de dados

    Returns:
      (str): O nome da tabela
    """
    pass
  
  @abstractmethod
  def _converter_resultado_para_entidade(self, linha_resultado):
    """
    Converte uma linha de resultado do banco de dados (sqlite3.Row)
    em uma instância da entidade de modelo correspondente

    Args: 
      linha_resultado (sqlite3.Row): Linha do resultado obtido no banco de dados

    Return:
      objeto: Instância da classe de modelo correspondente 
    """
    pass

  @abstractmethod
  def _converter_entidade_para_parametros_insercao(self, entidade):
    """
    Converte uma instância da entidade em uma tupla com os valores dos atributos na ordem correta
    para a inserção no banco de dados

    Args:
      entidade: Instância da classe de modelo
    
    Returns:
      tuple: Tupla com os valores dos atributos em ordem para a inserção
    """
    pass

  @abstractmethod
  def _converter_entidade_para_parametros_atualizacao(self, entidade):
    """
    Converte uma instância da entidade em uma tupla com os valores dos atributos na ordem correta
    para a atualização no banco de dados

    Args:
      entidade: Instância da classe de modelo
    
    Returns:
      tuple: Tupla com os valores dos atributos em ordem para a atualização
    """
    pass

  #Métodos genéricos (públicos) para interação com o banco de dados

  def buscar_por_id(self, id_entidade):
    """
    Busca uma entidade no banco de dados pelo id

    Args:
      id_entidade: o identificador da entidade a ser buscada
    
    Returns:
      objeto ou None: Objeto da entidade correspondente ou None caso não seja encontrado
    
    Raises:
      sqlite3.Error: Se ocorrer algum erro durante a execução da consulta
    """
    sql = f"SELECT * FROM {self._obter_nome_tabela()} WHERE id = ?"
    resultado_consulta = self._obter_um(sql, (id_entidade,))
    if resultado_consulta:
      return self._converter_resultado_para_entidade(resultado_consulta)
    return None
  
  def remover(self, id_entidade):
    """
    Remove uma entidade do banco de dados pelo id

    Args:
      id_entidade: o identificador da entidade a ser removida
    
    Raises:
      sqlite3.Error: Se ocorrer algum erro durante a execução da consulta
    """
    sql = f"DELETE FROM {self._obter_nome_tabela()} WHERE id = ?"
    self._executar_consulta(sql, (id_entidade, ))