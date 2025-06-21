from abc import ABC, abstractmethod


class IGerenciadorXP(ABC):

    # Métodos abstratos para gerenciamento de XP:

    @abstractmethod
    def adicionar_xp(self, valor: int):
        pass

    @abstractmethod
    def remover_xp(self, valor: int):
        pass

    @abstractmethod
    def get_xp(self) -> int:
        pass
