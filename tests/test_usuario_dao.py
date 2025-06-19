# test/test_usuario_dao.py

import unittest
from src.modelos.Usuario import Usuario
from src.acesso_dados.UsuarioDao import UsuarioDao
from utilidades_banco_dados import obter_conexao_teste
from configuracao_banco_dados import criar_tabelas_em_conexao, apagar_tabelas_em_conexao

class TestUsuarioDao(unittest.TestCase):
  """
  Classe de testes unitários para a classe de acesso aos dados UsuarioDao
  """

  def setUp(self):
    """
    Método de preparação do ambiente de testes a ser executado antes de cada teste
    """
    #Cria uma conexão com o banco de dados
    self.conexao = obter_conexao_teste()

    #Apaga as tabelas existentes
    apagar_tabelas_em_conexao(self.conexao)

    #Cria as tabelas necessárias para a manipulação do banco de dados
    criar_tabelas_em_conexao(self.conexao)

    #Salva as alterações executadas no banco de dados
    self.conexao.commit()

    self.dao = UsuarioDao()

  def tearDown(self):
    """
    Método de limpeza do ambiente de testes a ser executado ao final de cada teste
    """
    
    self.conexao.close() #Encerra a conexão com o banco de dados

  #Métodos de testes

  def test_inserir_usuario(self):
    """Verifica se um usuário pode ser inserido no banco de dados"""
    pass

  def test_buscar_por_id_usuario(self):
    """Verifica se um usuário pode ser buscado no banco de dados com o id"""
    pass

  def test_buscar_usuario_por_email(self):
    """Verifica se um usuário pode ser buscado no banco de dados com o email"""
    pass

  def test_unicidade_email(self):
    """Verifica se o banco de dados impede a duplicidade de emails"""
    pass

  def test_remover_usuario(self):
    """Verifica se um usuário pode ser removido do banco de dados"""
    pass

if __name__ == '__main__':
  unittest.main()