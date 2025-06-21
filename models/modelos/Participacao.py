from .IGerenciadorXP import IGerenciadorXP
from abc import abstractmethod

class Participacao(IGerenciadorXP):

    # Construtor da classe Participacao
    def __init__(
        self,
        usuario_id: int,
        projeto_id: int,
        id: int | None,
        xp_participacao: int,
        ativa: bool,
    ):
        self.__id = id
        self.__usuario_id = usuario_id
        self.__projeto_id = projeto_id
        self.__xp_participacao = xp_participacao
        self.__ativa = ativa

    # Getters:

    # getter de id da Participacao
    def get_id(self) -> int | None:
        return self.__id

    # getter de uduario_id da Participacao
    def get_usuario_id(self) -> int:
        return self.__usuario_id

    # getter de projeto_id da Participacao
    def get_projeto_id(self) -> int:
        return self.__projeto_id

    # verifica se a Participacao esta ativa
    def is_ativa(self) -> bool:
        return self.__ativa

    # Setters:

    # setter de id, altera id da Participacao
    def set_id(self, novo_id: int):
        self.__id = novo_id

    # Altera o status de ativa da Participacao
    def set_ativa(self, ativa: bool):
        self.__ativa = ativa

    # Gerenciamento de XP:

    # adiciona um valor de xp ao xp_participacao da Participacao
    def adicionar_xp(self, valor: int):
        if valor > 0:
            self.__xp_participacao += valor

    # remove um valor de xp do xp_participacao da Participacao
    def remover_xp(self, valor: int):
        if valor > 0:
            self.__xp_participacao = max(0, self.__xp_participacao - valor)

    # obtem o xp vinculado a Participacao
    def get_xp(self):
        return self.__xp_participacao

    # Metodos abstratos para permissoes:

    @abstractmethod
    def get_classificacao(self) -> str:
        """Retorna a classificação da Participacao"""
        pass

    @abstractmethod
    def pode_criar_tarefa(self) -> bool:
        """Verifica se a Participacao pode criar tarefas"""
        pass

    @abstractmethod
    def pode_adicionar_membro(self) -> bool:
        """Verifica se a Participacao pode adicionar membros"""
        pass

    @abstractmethod
    def pode_remover_membro(self) -> bool:
        """Verifica se a Participacao pode remover membros"""
        pass

    @abstractmethod
    def pode_atualizar_status(self, tarefa) -> bool:
        """
        Verifica se a Participacao pode atualizar o status de uma tarefa

        Args:
            tarefa (Tarefa): Instância de Tarefa para qual está sendo verificada a permissão

        Returns:
            bool: True se possui permissão, False caso contrário
        """
        pass
