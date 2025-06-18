from abc import ABC, abstractmethod
from IGerenciadorXP import IGerenciadorXP
from Tarefa import Tarefa

class Participacao(IGerenciadorXP):

    #Construtor da classe Participacao
    def __init__(self, id: int, usuario_id: int, projeto_id: int):
        self.__id = id
        self.__usuario_id = usuario_id
        self.__projeto_id = projeto_id
        self.__xp_participacao = 0
        self.__ativa = True


    #Getters:

    #getter de id da Participacao
    def get_id(self) -> int:
        return self.__id
    
    #getter de uduario_id da Participacao
    def get_usuario_id(self) -> int:
        return self.__usuario_id
    
    #getter de projeto_id da Participacao
    def get_projeto_id(self) -> int:
        return self.__projeto_id
    
    #verifica se a Participacao esta ativa
    def is_ativa(self) -> bool:
        return self.__ativa
    

    #Setters:

    #Altera o status de ativa da Participacao
    def set_ativa(self, ativa: bool):
        self.__ativa = ativa


    #Gerenciamento de XP:

    #adiciona um valor de xp ao xp_participacao da Participacao
    def adicionar_xp(self, valor: int):
        if valor > 0:
            self.__xp_participacao += valor

    #remove um valor de xp do xp_participacao da Participacao
    def remover_xp(self, valor: int):
        if valor > 0:
            self.__xp_participacao = max(0, self.__xp_participacao - valor)

    #getter de xp_participacao da Participacao
    def get_xp(self):
        return self.__xp_participacao
    

    #Metodos abstratos para permissoes:

    @abstractmethod
    def get_classificacao(self) -> str:
        pass

    @abstractmethod
    def pode_criar_tarefa(self) -> bool:
        pass

    @abstractmethod
    def pode_adicionar_membro(self) -> bool:
        pass

    @abstractmethod
    def pode_remover_membro(self) -> bool:
        pass

    @abstractmethod
    def pode_atualizar_status(self, tarefa: Tarefa) -> bool:
        pass
