# src/acesso_dados/ParticipacaoDao.py

from .BaseDao import BaseDao
from ..modelos.Participacao import Participacao
from ..modelos.Dono import Dono
from ..modelos.Participante import Participante

class ParticipacaoDao(BaseDao):
  """
  Classe para gerenciar as interações com o banco de dados referentes a entidade Participacao
  """

  def __init__(self):
    """
    Inicializa a classe ProjetoDao
    """
    super().__init__()
  
  # Implementação dos métodos abstratos da classe BaseDao

  def _obter_nome_tabela(self) -> str:
    """
    Retorna o nome da tabela correspondente à Projeto no bd
    
    Returns:
      str: O nome da tabela (participacoes)
    """
    return "participacoes"
  
  def _converter_resultado_para_entidade(self, linha_resultado) -> Participacao:
    """
    Converte uma linha de resultado do banco de dados (sqlite3.Row)
    em uma instância da classe Participacao

    Args: 
      linha_resultado (sqlite3.Row): Linha do resultado obtido no banco de dados

    Return:
      Participacao: Instância da classe Participacao (Dono ou Participante) preenchida com os dados da consulta 
    
    Raises:
      ValueError: Se a classificação lida do banco de dados for desconhecida.
    """
    usuario_id = linha_resultado['usuario_id']
    projeto_id = linha_resultado['projeto_id']
    participacao_id = linha_resultado['id']
    classificacao = linha_resultado['classificacao']
    xp_participacao = linha_resultado['xp_participacao']
    ativa = True if linha_resultado['participacao_habilitada'] == 1 else False

    if classificacao == "DONO":
      return Dono(usuario_id, projeto_id, participacao_id, xp_participacao, ativa)
    elif classificacao == "PARTICIPANTE":
      return Participante(usuario_id, projeto_id, participacao_id, xp_participacao, ativa)
    else:
      raise ValueError(f"Classificação {classificacao} desconhecida")

  def _converter_entidade_para_parametros_insercao(self, participacao: Participacao) -> tuple:
    """
    Converte uma instância de Participacao em uma tupla com os valores dos atributos na ordem correta
    para a inserção no banco de dados (usuario_id, projeto_id, xp_participacao, participacao_habilitada, classificacao)

    Args:
      participacao (Participacao): Instância da classe de modelo
    
    Returns:
      tuple: Tupla com os valores dos atributos em ordem para a inserção
    """

    return (
      participacao.get_usuario_id(),
      participacao.get_projeto_id(),
      participacao.get_xp(),
      1 if participacao.is_ativa() else 0,
      participacao.get_classificacao()
    )
  
  def _converter_entidade_para_parametros_atualizacao(self, participacao: Participacao) -> tuple:
    """
    Converte uma instância de Participacao em uma tupla com os valores dos atributos na ordem correta
    para a atualização no banco de dados (xp_participacao, participacao_habilitada, id)
    
    Args:
      participacao (Participacao): Instância da classe de modelo
    
    Returns:
      tuple: Tupla com os valores dos atributos em ordem para a atualização
    """
    return (
      participacao.get_xp(),
      1 if participacao.is_ativa() else 0,
      participacao.get_id()
    )
  
  def inserir(self, participacao: Participacao) -> Participacao:
    """
    Insere uma nova participacao no banco de dados

    Args:
      participacao (Participacao): instância da classe Participacao a ser inserida
    
    Raises:
      sqlite3.Error: Se ocorrer algum erro durante a inserção
    
    Returns:
      Participacao: A mesma instância de Participacao passada, agora com id preenchido (no caso de sucesso na inserção)
    """

    sql = f"""
    INSERT INTO {self._obter_nome_tabela()} (usuario_id, projeto_id, xp_participacao, participacao_habilitada, classificacao) 
    Values (?, ?, ?, ?, ?);
    """
    return self._realizar_insercao_e_atribuir_id(participacao, sql)
  
  def atualizar(self, participacao: Participacao):
    """
    Atualiza todos os atributos editáveis de uma participacao no bd

    Args:
      participacao (Participacao): instância da classe Participacao a ser atualizado
    """

    sql = f"""
    UPDATE {self._obter_nome_tabela()}
    SET xp_participacao = ?, participacao_habilitada = ?
    WHERE id = ?
    """
    self._realizar_atualizacao(participacao, sql)
  
  def buscar_participacao_usuario_projeto(self, usuario_id: int, projeto_id: int) -> Participacao | None:
    """
    Busca uma participação específica de um usuário em um projeto.

    Args:
      usuario_id (int): O identificador do usuário.
      projeto_id (int): O identificador do projeto.

    Returns:
      Participacao ou None: A instância da participação se encontrada, ou None.
    """

    sql = f"""
    SELECT id, usuario_id, projeto_id, xp_participacao, participacao_habilitada, classificacao
    FROM {self._obter_nome_tabela()}
    WHERE usuario_id = ? AND projeto_id = ?;
    """
    resultado = self._obter_um(sql, (usuario_id, projeto_id))
    
    if resultado:
      return self._converter_resultado_para_entidade(resultado)
    return None
  
  def inativa_participacao(self, participacao_id):
    """
    Altera o status de uma participação para inativa (participacao_habilitada = 0).
    
    Args:
      participacao_id (int): O identificador da participação a ser inativada.
    """

    sql = f"""
    UPDATE {self._obter_nome_tabela()}
    SET participacao_habilitada = 0
    WHERE id = ?;
    """
    self._executar_consulta(sql, (participacao_id,))