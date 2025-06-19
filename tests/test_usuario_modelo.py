# tests/test_usuario_modelo.py

import unittest
from ..src.modelos.Usuario import Usuario
from ..src.modelos.Seguranca import gerar_hash_senha

class TestUsuarioModelo(unittest.TestCase):
  """
  Classe de testes unitários para a classe modelo Usuario
  """

  def setUp(self):
    """
    Método de preparação do ambiente de testes a ser executado antes de cada teste
    """
    self.novo_usuario = Usuario("Diogo", "diogo@gmail.com", "minha_senha")

  def tearDown(self):
    """
    Método de limpeza do ambiente de testes a ser executado ao final de cada teste
    """
    pass

  #Métodos de testes:

  def test_criar_usuario_construtor(self):
    """Verifica se o usuário é criado corretamente"""
    self.assertEqual(self.novo_usuario.get_name(), "Diogo")
    self.assertEqual(self.novo_usuario.get_email(), "diogo@gmail.com")
    self.assertNotEqual(self.novo_usuario.get_senha_hash(), "minha_senha")

  def test_set_nome(self):
    """Verifica se o nome do usuário pode ser alterado"""
    novo_nome = "Diogo Barros"
    self.novo_usuario.set_nome(novo_nome)
    self.assertEqual(self.novo_usuario.get_nome, novo_nome)

  def test_verificar_senha_correta(self):
    """Verifica se a checagem da senha retorna True com a senha correta"""
    self.assertTrue(self.novo_usuario.verificar_senha("minha_senha"))
  
  def test_verificar_senha_incorreta(self):
    """Verifica se a checagem da senha retorna False para a senha incorreta"""
    self.assertFalse(self.novo_usuario.verificar_senha("qualquer_senha"))

  def test_alterar_senha_sucesso(self):
    """Verifica se a senha é alterada quando a senha atual correta é fornecida"""
    senha_antiga = "minha_senha"
    hash_senha_antiga = self.novo_usuario.get_senha_hash()
    nova_senha = "nova_senha"
    self.assertTrue(self.novo_usuario.alterar_senha(senha_antiga, nova_senha))
    self.assertTrue(self.novo_usuario.verificar_senha(nova_senha))
    self.assertNotEqual(self.novo_usuario.get_senha_hash(), hash_senha_antiga)

  def test_alterar_senha_falha(self):
    """Verifica se a senha não é alterada quando a senha atual errada é fornecida"""
    senha_errada = "qualquer_senha"
    hash_senha_certa = self.novo_usuario.get_senha_hash()
    nova_senha = "nova_senha"
    self.assertFalse(self.novo_usuario.alterar_senha(senha_errada, nova_senha))
    self.assertFalse(self.novo_usuario.verificar_senha(senha_errada))
    self.assertEqual(self.novo_usuario.get_senha_hash, hash_senha_certa)

#Executa os testes quando o arquivo é rodado diretamente
if __name__ == '__main__': unittest.main()