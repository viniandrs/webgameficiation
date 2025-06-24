# src/acesso_dados/SprintMetaDao.py

from .BaseDao import BaseDao
from ..modelos.SprintMeta import SprintMeta
from ..modelos.ItemDeTrabalho import StatusItem
from .SingletonMeta import SingletonMeta
from datetime import date, datetime

class SprintMetaDao(BaseDao, metaclass = SingletonMeta):
  """
  Classe para gerenciar as interações com o banco de dados referentes à entidade SprintMeta
  """

  def __init__(self):
    """
    Inicializa a classe SprintMetaDao
    """
    super().__init__()

  # Implementação dos métodos abstratos da classe BaseDao

  def _obter_nome_tabela(self) -> str:
    """
    Retorna o nome da tabela correspondente à SprintMeta no bd
    
    Returns:
      str: O nome da tabela (sprint_metas)
    """
    return "sprint_metas"
  
  def _converter_resultado_para_entidade(self, linha_resultado) -> SprintMeta:
    """
    Converte uma linha de resultado do banco de dados (sqlite3.Row)
    em uma instância da classe SprintMeta

    Args: 
      linha_resultado (sqlite3.Row): Linha do resultado obtido no banco de dados

    Return:
      SprintMeta: Instância da classe SprintMeta preenchida com os dados da consulta 
    """

    #Converte o status (string) obtido no bd para um membro da Enum StatusItem
    status = StatusItem[linha_resultado['status']]
    
    #Converte string de data no bd para um objeto date
    prazo = None
    if linha_resultado['data_alvo']:
      prazo = datetime.strptime(linha_resultado['data_alvo'], '%Y-%m-%dT%H:%M:%S').date()

    return SprintMeta(
      linha_resultado['id'],
      linha_resultado['projeto_id'],
      linha_resultado['nome'],
      linha_resultado['descricao'],
      linha_resultado['xp_bonus'],
      status,
      prazo
    )
  
  def _converter_entidade_para_parametros_insercao(self, sprint: SprintMeta) -> tuple:
    """
    Converte uma instância de SprintMeta em uma tupla com os valores dos atributos na ordem correta
    para a inserção no banco de dados (projeto_id, nome, descricao, xp_bonus, status, data_alvo)

    Args:
      sprint (SprintMeta): Instância da classe de modelo
    
    Returns:
      tuple: Tupla com os valores dos atributos em ordem para a inserção
    """

    #Converte o status de um membro da Enum StatusItem para uma string
    status = sprint.get_status().name
    #Converte o prazo de um objeto date para uma string no formato ISO
    prazo = None
    if sprint.get_data_alvo():
      prazo = datetime.fromisoformat(sprint.get_data_alvo()).isoformat()

    
    return (
      sprint.get_projeto_id(),
      sprint.get_nome(),
      sprint.get_descricao(),
      sprint.get_xp_valor(),
      status,
      prazo,
    )
  
  def _converter_entidade_para_parametros_atualizacao(self, sprint: SprintMeta) -> tuple:
    """
    Converte uma instância de SprintMeta em uma tupla com os valores dos atributos na ordem correta
    para a atualização no banco de dados (projeto_id, nome, descricao, xp_bonus, status, data_alvo)
    
    Args:
      sprint (SprintMeta): Instância da classe de modelo
    
    Returns:
      tuple: Tupla com os valores dos atributos em ordem para a atualização
    """

    #Converte o status de um membro da Enum StatusItem para uma string
    status = sprint.get_status().name

    #Converte o prazo de um objeto date para uma string no formato ISO
    prazo = None
    if sprint.get_data_alvo():
      prazo = datetime.fromisoformat(sprint.get_data_alvo()).isoformat()
    
    return (
      sprint.get_nome(),
      sprint.get_descricao(),
      sprint.get_xp_valor(),
      status,
      prazo,
      sprint.get_id()
    )
  
  #Métodos públicos
  
  def inserir(self, sprint: SprintMeta) -> SprintMeta:
    """
    Insere uma nova SprintMeta no banco de dados

    Args:
      sprint (SprintMeta): Instância da classe Tarefa a ser inserida
    
    Raises:
      sqlite3.Error: Se ocorrer algum erro durante a inserção
    
    Returns:
      Tarefa: A mesma instância de Tarefa passada, agora com id preenchido (no caso de sucesso na inserção)
    """
    sql = f"""
    INSERT INTO {self._obter_nome_tabela()} 
    (projeto_id, nome, descricao, xp_bonus, status, data_alvo)
    Values (?, ?, ?, ?, ?, ?);
    """
    return self._realizar_insercao_e_atribuir_id(sprint, sql)
  
  def atualizar(self, sprint: SprintMeta):
    """
    Atualiza todos os atributos editáveis de uma sprint no bd

    Args:
      sprint (SprintMeta): instância da classe SprintMeta a ser atualizado
    """
    sql = f"""
    UPDATE {self._obter_nome_tabela()}
    SET nome = ?, descricao = ?, xp_bonus = ?, status = ?, data_alvo = ?
    WHERE id = ?
    """
    self._realizar_atualizacao(sprint, sql)
  
  def atualizar_status_sprint(self, sprint_id: int, novo_status: StatusItem):
    """
    Atualiza o status de uma sprint no banco de dados

    Args:
      sprint_id (int): Identificador da sprint a ser atualizada
      novo_status (StatusItem): Novo status da sprint
    """
    sql = f"""
    UPDATE {self._obter_nome_tabela()}
    SET status = ?
    WHERE id = ?
    """

    status_str = novo_status.name
    self._executar_consulta(sql, (status_str, sprint_id))
  
  def buscar_sprint_metas_projeto(self, projeto_id: int):
    """
    Busca as SprintMetas associadas a um projeto

    Args:
      projeto_id (int): Identificador do projeto usado na busca
    
    Returns:
      lista de SprintMeta: Lista contendo todos as SprintMeta associadas a um projeto
    """
    sql = """
    SELECT id, projeto_id, nome, descricao, xp_bonus, status, data_alvo
    FROM sprint_metas
    WHERE projeto_id = ?;
    """
    resultados = self._obter_todos(sql, (projeto_id,))
    return [self._converter_resultado_para_entidade(linha) for linha in resultados]