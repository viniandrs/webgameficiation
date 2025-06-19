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
      str: O nome da tabela (usuarios)
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

    senha_hash = linha_resultado['senha']

    if isinstance(senha_hash, str):
      senha_hash = senha_hash.encode('utf-8')

    return Usuario.criar_com_hash(
      linha_resultado['id'],
      linha_resultado['nome'],
      linha_resultado['email'],
      senha_hash
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
      usuario.get_senha_hash(),
    )
  
  def _converter_entidade_para_parametros_atualizacao(self, usuario: Usuario) -> tuple:
    """
    Converte uma instância de Usuario em uma tupla com os valores dos atributos na ordem correta
    para a atualização no banco de dados (nome, email, senha, id)
    
    Args:
      usuario (Usuario): Instância da classe de modelo
    
    Returns:
      tuple: Tupla com os valores dos atributos em ordem para a atualização
    """

    return (
      usuario.get_nome(),
      usuario.get_email(),
      usuario.get_senha_hash(),
      usuario.get_id()
    )
  
  # Métodos (públicos) CRUD específicos pars Usuario

  def inserir(self, usuario: Usuario):
    """
    Insere um novo usuário no banco de dados

    Args:
      usuario (Usuario): instância da classe Usuario a ser inserido
    
    Raises:
      sqlite3.Error: Se ocorrer algum erro durante a inserção
    
    Returns:
      Usuário: A mesma instância de Usuário passada, agora com id preenchido (no caso de sucesso na inserção)
    """

    sql = f"INSERT INTO {self._obter_nome_tabela()} (nome, email, senha) Values (?, ?, ?);"
    return self._realizar_insercao_e_atribuir_id(usuario, sql)
    
    

  def buscar_por_email(self, email: str):
    """
    Busca um usuário no banco de dados pelo email

    Args:
      email(str): endereço de email que será buscado
    
    Returns:
      Usuário ou None: Uma instância de Usuario, ou None caso não seja encontrado
    """

    sql = f"SELECT id, nome, email, senha FROM {self._obter_nome_tabela()} WHERE email = ?"
    resultado_consulta = self._obter_um(sql, (email,))
    if resultado_consulta:
      return self._converter_resultado_para_entidade(resultado_consulta)
    return None
