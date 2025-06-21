#src/acesso_dados/TarefaDao.py

from .BaseDao import BaseDao
from ..modelos.Tarefa import Tarefa
from ..modelos.ItemDeTrabalho import StatusItem
from datetime import date

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

    #Converte o status (string) obtido no bd para um membro da Enum StatusItem
    status = StatusItem[linha_resultado['status']]
    
    #Converte string de data no bd para um objeto date
    prazo = None
    if linha_resultado['prazo']:
      prazo = date.fromisoformat(linha_resultado['prazo'])

    return Tarefa(
      linha_resultado['id'],
      linha_resultado['projeto_id'],
      linha_resultado['titulo'],
      linha_resultado['descricao'],
      linha_resultado['xp_valor'],
      status,
      linha_resultado['participacao_responsavel_id'],
      prazo,
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

    #Converte o status de um membro da Enum StatusItem para uma string
    status = tarefa.get_status().name

    #Converte o prazo de um objeto date para uma string no formato ISO
    prazo = None
    if tarefa.get_prazo():
      prazo = tarefa.get_prazo().isoformat()

    return (
      tarefa.get_projeto_id(),
      tarefa.get_nome(),
      tarefa.get_descricao(),
      tarefa.get_xp_valor(),
      status,
      tarefa.get_participacao_responsavel_id(),
      prazo,
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

    #Converte o status de um membro da Enum StatusItem para uma string
    status = tarefa.get_status().name

    #Converte o prazo de um objeto date para uma string no formato ISO
    prazo = None
    if tarefa.get_prazo():
      prazo = tarefa.get_prazo().isoformat()
    
    return (
      tarefa.get_nome(),
      tarefa.get_descricao(),
      tarefa.get_xp_valor(),
      status,
      tarefa.get_participacao_responsavel_id(),
      prazo,
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
  
  def atualizar_status_tarefa(self, tarefa_id: int, novo_status: StatusItem):
    """
    Atualiza o status de uma tarefa no banco de dados

    Args:
      tarefa_id (int): Identificador da tarefa a ser atualizada
      novo_status (StatusItem): Novo status da tarefa
    """
    sql = f"""
    UPDATE {self._obter_nome_tabela()}
    SET status = ?
    WHERE id = ?
    """

    status_str = novo_status.name
    self._executar_consulta(sql, (status_str, tarefa_id))
  
  def buscar_tarefas_projeto(self, projeto_id):
    """
    Busca todas as tarefas associadas a um projeto

    Args: 
      projeto_id (int): Identificador do projeto usado na busca

    Returns:
      lista de Tarefas: Lista contendo todas as tarefas associadas ao projeto 
    """
    sql = """
    SELECT 
    id, projeto_id, titulo, descricao, xp_valor, status, 
    participacao_responsavel_id, prazo, sprint_meta_id
    FROM tarefas
    WHERE projeto_id = ?
    """
    resultados = self._obter_todos(sql, (projeto_id,))
    return [self._converter_resultado_para_entidade(linha) for linha in resultados]
  
  def buscar_tarefas_sprint(self, sprint_id):
    """
    Busca todas as tarefas associadas a uma sprint

    Args: 
      sprint_id (int): Identificador da sprint usado na busca

    Returns:
      lista de Tarefas: Lista contendo todas as tarefas associadas a sprint
    """
    sql = """
    SELECT 
    id, projeto_id, titulo, descricao, xp_valor, status, 
    participacao_responsavel_id, prazo, sprint_meta_id
    FROM tarefas
    WHERE sprint_meta_id = ?
    """
    resultados = self._obter_todos(sql, (sprint_id,))
    return [self._converter_resultado_para_entidade(linha) for linha in resultados]