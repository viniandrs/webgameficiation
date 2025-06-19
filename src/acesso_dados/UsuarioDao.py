#src/acesso_dados/UsuarioDao.py

from .BaseDao import BaseDao
from ..modelos.Usuario import Usuario

class UsuarioDao(BaseDao):
  """
  Classe para gerenciar as interações com o banco de dados referentes a entidade Usuario
  """
  
  def __init__(self):
    """
    Inicializa a classe UsuarioDao
    """
    super().__init__()

  # Implementação dos métodos abstratos da classe BaseDao

  def _obter_nome_tabela(self) -> str:
    """
    Retorna o nome da tabela correspondente à Usuario no bd
    
    Returns:
      (str): O nome da tabela (usuarios)
    """
    return "usuarios"
  
  def _converter_resultado_para_entidade(self, linha_resultado) -> Usuario:
    """
    Converte uma linha de resultado do banco de dados (sqlite3.Row)
    em uma instância da classe Usuario

    Args: 
      linha_resultado (sqlite3.Row): Linha do resultado obtido no banco de dados

    Return:
      Usuario: Instância da classe Usuario preenchida com os dados da consulta 
    """
    return Usuario(
      linha_resultado['id'],
      linha_resultado['nome'],
      linha_resultado['email'],
      linha_resultado['senha']
    )
  
  def _converter_entidade_para_parametros_insercao(self, usuario: Usuario) -> tuple:
    """
    Converte uma instância de Usuario em uma tupla com os valores dos atributos na ordem correta
    para a inserção no banco de dados (nome, email, senha)

    Args:
      usuario (Usuario): Instância da classe de modelo
    
    Returns:
      tuple: Tupla com os valores dos atributos em ordem para a inserção
    """

    return (
      usuario.get_nome(),
      usuario.get_email(),
      usuario.get_senha(),
    )
  
  # Métodos (públicos) CRUD específicos pars Usuario

  def inserir(self, usuario: Usuario):
    """
    Insere um novo usuário no banco de dados

    Args:
      usuario (Usuario): instância da classe Usuario a ser inserido
    
    Raises:
      sqlite3.Error: Se ocorrer algum erro durante a inserção
    """

    sql = f"INSERT INTO {self._obter_nome_tabela()} (nome, email, senha) Values (?, ?, ?);"
    parametros_sql = self._converter_entidade_para_parametros(usuario)
    self._executar_consulta(sql, parametros_sql)

  
