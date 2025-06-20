#src/acesso_dados/TarefaDao.py

from .BaseDao import BaseDao
from ..modelos.Tarefa import Tarefa

class TarefaDao(BaseDao):
  """
  Classe para gerenciar as interações com o banco de dados referentes a entidade Tarefa
  """
  
  def __init__(self):
    """
    Inicializa a classe TarefaDao
    """
    super().__init__()

  # Implementação dos métodos abstratos da classe BaseDao

  def _obter_nome_tabela(self) -> str:
    """
    Retorna o nome da tabela correspondente à Tarefa no bd
    
    Returns:
      str: O nome da tabela (tarefas)
    """
    return "tarefas"
  
  def _converter_resultado_para_entidade(self, linha_resultado) -> Tarefa:
    """
    Converte uma linha de resultado do banco de dados (sqlite3.Row)
    em uma instância da classe Tarefa

    Args: 
      linha_resultado (sqlite3.Row): Linha do resultado obtido no banco de dados

    Return:
      Tarefa: Instância da classe Tarefa preenchida com os dados da consulta 
    """

    return Tarefa(
      linha_resultado['id'],
      linha_resultado['projeto_id'],
      linha_resultado['titulo'],
      linha_resultado['descricao'],
      linha_resultado['xp_valor'],
      linha_resultado['status'],
      linha_resultado['participacao_responsavel_id'],
      linha_resultado['prazo'],
      linha_resultado['sprint_meta_id']
    )
  
  def _converter_entidade_para_parametros_insercao(self, tarefa: Tarefa) -> tuple:
    """
    Converte uma instância de Tarefa em uma tupla com os valores dos atributos na ordem correta
    para a inserção no banco de dados (projeto_id, titulo, descricao, xp_valor, status, 
    participacao_responsavel_id, prazo, sprint_meta_id)

    Args:
      tarefa (Tarefa): Instância da classe de modelo
    
    Returns:
      tuple: Tupla com os valores dos atributos em ordem para a inserção
    """

    return (
      tarefa.get_projeto_id(),
      tarefa.get_nome(),
      tarefa.get_descricao(),
      tarefa.get_xp_valor(),
      tarefa.get_status(),
      tarefa.get_participacao_responsavel_id(),
      tarefa.get_prazo(),
      tarefa.get_sprint_meta_id(),
    )
  
  def _converter_entidade_para_parametros_atualizacao(self, tarefa: Tarefa) -> tuple:
    """
    Converte uma instância de Tarefa em uma tupla com os valores dos atributos na ordem correta
    para a atualização no banco de dados (titulo, descricao, xp_valor, status, 
    participacao_responsavel_id, prazo, sprint_meta_id)
    
    Args:
      tarefa (Tarefa): Instância da classe de modelo
    
    Returns:
      tuple: Tupla com os valores dos atributos em ordem para a atualização
    """
    return (
      tarefa.get_nome(),
      tarefa.get_descricao(),
      tarefa.get_xp_valor(),
      tarefa.get_status(),
      tarefa.get_participacao_responsavel_id(),
      tarefa.get_prazo(),
      tarefa.get_sprint_meta_id(),
      tarefa.get_id()
    )
  
  #Métodos públicos
  
  def inserir(self, tarefa: Tarefa) -> Tarefa:
    """
    Insere uma nova tarefa no banco de dados

    Args:
      tarefa (Tarefa): Instância da classe Tarefa a ser inserida
    
    Raises:
      sqlite3.Error: Se ocorrer algum erro durante a inserção
    
    Returns:
      Tarefa: A mesma instância de Tarefa passada, agora com id preenchido (no caso de sucesso na inserção)
    """
    sql = f"""
    INSERT INTO {self._obter_nome_tabela()} 
    (projeto_id, titulo, descricao, xp_valor, status, participacao_responsavel_id, prazo, sprint_meta_id)
    Values (?, ?, ?, ?, ?, ?, ?, ?);
    """
    return self._realizar_insercao_e_atribuir_id(tarefa, sql)
  
  def atualizar(self, tarefa: Tarefa):
    """
    Atualiza todos os atributos editáveis de uma tarefa no bd

    Args:
      tarefa (Tarefa): instância da classe Tarefa a ser atualizado
    """
    sql = f"""
    UPDATE {self._obter_nome_tabela()}
    SET titulo = ?, descricao = ?, xp_valor = ?, status = ?, participacao_responsavel_id = ?, prazo = ?, sprint_meta_id = ?
    WHERE id = ?
    """
    self._realizar_atualizacao(tarefa, sql)
  