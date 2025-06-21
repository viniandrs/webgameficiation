# test/test_usuario_dao.py

import sqlite3
import unittest
from unittest.mock import patch
from models.modelos.Usuario import Usuario
from models.acesso_dados.UsuarioDao import UsuarioDao
from models.utils import obter_conexao_teste
from models.configuracao_banco_dados import (
    criar_tabelas_em_conexao,
    apagar_tabelas_em_conexao,
)


class TestUsuarioDao(unittest.TestCase):
    """
    Classe de testes unitários para a classe de acesso aos dados UsuarioDao
    """

    def setUp(self):
        """
        Método de preparação do ambiente de testes a ser executado antes de cada teste
        Cria e inicializa um banco de dados em memória para o teste, garantindo que esteja limpo
        Moca a função 'obter_conexao' para que a DAO utilize este DB em memória
        """
        self.conexao_teste = obter_conexao_teste()

        cursor = self.conexao_teste.cursor()
        apagar_tabelas_em_conexao(self.conexao_teste)
        criar_tabelas_em_conexao(self.conexao_teste)
        self.conexao_teste.commit()
        cursor.close()

        # MOCAR a função obter_conexao para que ela retorne conexão em memória.
        self.patcher_obter_conexao = patch(
            "src.acesso_dados.BaseDao.obter_conexao", return_value=self.conexao_teste
        )
        self.patcher_obter_conexao.start()

        # Instancia a classe UsuarioDao
        self.dao = UsuarioDao()

    def tearDown(self):
        """
        Método de limpeza do ambiente de testes a ser executado ao final de cada teste
        Para o mock e fecha a conexão com o banco de dados em memória, que o apaga
        """
        self.patcher_obter_conexao.stop()  # Para o patcher para restaurar a função original 'obter_conexao'.
        if self.conexao_teste:
            self.conexao_teste.close()

    # Métodos de testes

    def test_inserir_usuario(self):
        """Verifica se um usuário pode ser inserido no banco de dados"""
        novo_usuario = Usuario("Diogo", "diogo@gmail.com", "minha_senha")

        usuario_inserido = self.dao.inserir(novo_usuario)

        self.assertIsNotNone(
            usuario_inserido.get_id()
        )  # Verifica se um id foi atribuído
        self.assertIs(novo_usuario, usuario_inserido)

    def test_buscar_por_id_usuario(self):
        """Verifica se um usuário pode ser buscado no banco de dados com o id"""
        novo_usuario = Usuario("Diogo1", "diogo1@gmail.com", "minha_senha1")

        usuario_inserido = self.dao.inserir(novo_usuario)

        self.assertIsNotNone(usuario_inserido.get_id())
        self.assertIsNotNone(self.dao.buscar_por_id(usuario_inserido.get_id()))

    def test_buscar_usuario_por_email(self):
        """Verifica se um usuário pode ser buscado no banco de dados com o email"""
        novo_usuario = Usuario("Diogo2", "diogo2@gmail.com", "minha_senha2")

        usuario_inserido = self.dao.inserir(novo_usuario)
        self.assertIsNotNone(usuario_inserido.get_id())
        self.assertIsNotNone(self.dao.buscar_por_email(novo_usuario.get_email()))

        # Busca por email que não existe
        self.assertIsNone(self.dao.buscar_por_email("inexistente@gmail.com"))

    def test_unicidade_email(self):
        """Verifica se o banco de dados impede a duplicidade de emails"""
        email_duplicado = "duplicado@gmail.com"
        usuario1 = Usuario("Usuario1", email_duplicado, "senha1")
        self.dao.inserir(usuario1)

        usuario2 = Usuario("Usuario2", email_duplicado, "senha2")

        with self.assertRaises(sqlite3.IntegrityError):
            self.dao.inserir(usuario2)

    def test_remover_usuario(self):
        """Verifica se um usuário pode ser removido do banco de dados"""
        usuario_a_remover = self.dao.inserir(
            Usuario("Removido", "removido@gmail.com", "senha")
        )

        self.assertIsNotNone(usuario_a_remover.get_id())

        self.dao.remover(usuario_a_remover.get_id())

        self.assertIsNone(self.dao.buscar_por_id(usuario_a_remover.get_id()))


if __name__ == "__main__":
    unittest.main()
