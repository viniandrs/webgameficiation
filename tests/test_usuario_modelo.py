# tests/test_usuario_modelo.py

import unittest
from ..src.modelos.Usuario import Usuario

class TestUsuarioModelo(unittest.TestCase):
  """
  Classe de testes unitários para a classe modelo Usuario
  """

  def setUp(self):
    """
    Método de preparação do ambiente de testes a ser executado antes de cada teste
    """
    pass

  def tearDown(self):
    """
    Método de limpeza do ambiente de testes a ser executado ao final de cada teste
    """
    pass

  #Métodos de testes:

  def test_criar_usuario_construtor(self):
    """Verifica se o usuário é criado corretamente"""
    pass

  def test_set_nome(self):
    """Verifica se o nome do usuário pode ser alterado"""
    pass

  def test_verificar_senha_correta(self):
    """Verifica se a checagem da senha retorna True com a senha correta"""
    pass
  
  def test_verificar_senha_incorreta(self):
    """Verifica se a checagem da senha retorna False para a senha incorreta"""
    pass

  def test_alterar_senha_sucesso(self):
    """Verifica se a senha é alterada quando a senha atual correta é fornecida"""
    pass

  def test_alterar_senha_falha(self):
    """Verifica se a senha não é alterada quando a senha atual errada é fornecida"""
    pass

#Executa os testes quando o arquivo é rodado diretamente
if __name__ == '__main__': unittest.main()