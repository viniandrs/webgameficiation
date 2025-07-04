# src/acess_dados/ProjetoDao.py

from .BaseDao import BaseDao
from ..modelos.Projeto import Projeto
from ..modelos.ItemDeTrabalho import StatusItem
from .SingletonMeta import SingletonMeta
from datetime import date

class ProjetoDao(BaseDao, metaclass = SingletonMeta):
  """
  Classe para gerenciar as interações com o banco de dados referentes a entidade Projeto
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
      str: O nome da tabela (projetos)
    """
    return "projetos"
  
  def _converter_resultado_para_entidade(self, linha_resultado) -> Projeto:
    """
    Converte uma linha de resultado do banco de dados (sqlite3.Row)
    em uma instância da classe Projeto

    Args: 
      linha_resultado (sqlite3.Row): Linha do resultado obtido no banco de dados

    Return:
      Projeto: Instância da classe Projeto preenchida com os dados da consulta 
    """

    return Projeto(
      linha_resultado['nome'],
      linha_resultado['descricao'],
      linha_resultado['xp_acumulado'],
      linha_resultado['xp_meta'],
      linha_resultado['id']
    )
  
  def _converter_entidade_para_parametros_insercao(self, projeto: Projeto) -> tuple:
    """
    Converte uma instância de Projeto em uma tupla com os valores dos atributos na ordem correta
    para a inserção no banco de dados (nome, descricao, xp_acumulado, xp_meta)

    Args:
      projeto (Projeto): Instância da classe de modelo
    
    Returns:
      tuple: Tupla com os valores dos atributos em ordem para a inserção
    """

    return (
      projeto.get_nome(),
      projeto.get_descricao(),
      projeto.get_xp(),
      projeto.get_xp_meta()
    )
  
  def _converter_entidade_para_parametros_atualizacao(self, projeto: Projeto) -> tuple:
    """
    Converte uma instância de Projeto em uma tupla com os valores dos atributos na ordem correta
    para a atualização no banco de dados (nome, descricao, xp_acumulado, xp_meta, id)
    Args:
      projeto (Projeto): Instância da classe de modelo
    
    Returns:
      tuple: Tupla com os valores dos atributos em ordem para a atualização
    """

    return (
      projeto.get_nome(),
      projeto.get_descricao(),
      projeto.get_xp(),
      projeto.get_xp_meta(),
      projeto.get_id()
    )
  
  #Métodos públicos
  
  def inserir(self, projeto: Projeto):
    """
    Insere um novo projeto no banco de dados

    Args:
      projeto (Projeto): instância da classe Projeto a ser inserido
    
    Raises:
      sqlite3.Error: Se ocorrer algum erro durante a inserção
    
    Returns:
      Projeto: A mesma instância de Projeto passada, agora com id preenchido (no caso de sucesso na inserção)
    """

    sql = f"""
    INSERT INTO {self._obter_nome_tabela()} (nome, descricao, xp_acumulado, xp_meta) 
    Values (?, ?, ?, ?);
    """
    return self._realizar_insercao_e_atribuir_id(projeto, sql)
  
  def atualizar(self, projeto: Projeto):
    """
    Atualiza todos os atributos editáveis de um projeto no bd

    Args:
      projeto (Projeto): instância da classe Projeto a ser atualizado
    """

    sql = f"""
    UPDATE {self._obter_nome_tabela()}
    SET nome = ?, descricao = ?, xp_acumulado = ?, xp_meta = ?
    WHERE id = ?
    """
    self._realizar_atualizacao(projeto, sql)
  
  def buscar_membros_do_projeto(self, projeto_id: int):
    """
    Encontra todos os usuários com participação ativa em um projeto

    Args: 
      projeto_id (int): Identificados do projeto usado na busca

    Returns:
      lista de dict: Lista de dicionários com os dados do usuário e da sua participação no projeto,
      ordenados com base no xp_participacao 
    """
    sql = f"""
    SELECT 
    user.id AS usuario_id, 
    user.nome AS usuario_nome, 
    part.id,
    part.xp_participacao, 
    part.classificacao, 
    part.participacao_habilitada
    FROM usuarios AS user
    JOIN participacoes AS part ON user.id = part.usuario_id
    WHERE part.projeto_id = ?
    ORDER BY part.xp_participacao DESC;
    """
    resultado = self._obter_todos(sql, (projeto_id, ))
    
    membros = []

    for membro in resultado:
      membros.append({
        'usuario_id': membro['usuario_id'],
        'usuario_nome': membro['usuario_nome'],
        'id': membro['id'],
        'classificacao': membro['classificacao'],
        'xp_participacao': membro['xp_participacao'],
        'participacao_habilitada': membro['participacao_habilitada']
      })
    
    return membros
  
  def buscar_por_usuario_id(self, usuario_id:int):
    """
    Busca uma entidade no banco de dados pelo id do usuário que possui vinculo

    Args:
      usuario_id: o identificador do usuario que tera relação com o projeto
    
    Returns:
      objeto ou None: Objeto da entidade correspondente ou None caso não seja encontrado
    
    Raises:
      sqlite3.Error: Se ocorrer algum erro durante a execução da consulta
    """
    sql = """
    SELECT projetos.*
    FROM projetos
    JOIN participacoes ON projetos.id = participacoes.projeto_id AND participacoes.participacao_habilitada=1
    WHERE participacoes.usuario_id = ?;
    """
    resultado_consulta = self._obter_todos(sql, (usuario_id,))

    if resultado_consulta:
       return [self._converter_resultado_para_entidade(linha) for linha in resultado_consulta]
    return None