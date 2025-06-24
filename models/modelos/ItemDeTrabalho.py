from abc import ABC, abstractmethod
from enum import Enum, auto


class StatusItem(Enum):
    PENDENTE = auto()
    EM_ANDAMENTO = auto()
    CONCLUIDA = auto()
    AGUARDANDO_REASSIGNACAO = auto()


class ItemDeTrabalho(ABC):

    # construtor da classe ItemDeTrabalho
    def __init__(
        self,
        id: int | None,
        projeto_id: int,
        nome: str,
        descricao: str,
        xp_valor: int,
        status: StatusItem,
    ):
        self.__id = id
        self.__projeto_id = projeto_id
        self.__nome = nome
        self.__descricao = descricao
        self.__xp_valor = xp_valor
        self.__status = status

    # Getters:

    # getter de id do ItemDeTrabalho
    def get_id(self) -> int:
        return self.__id

    # getter de id do projeto do ItemDeTrabalho
    def get_projeto_id(self) -> int:
        return self.__projeto_id

    # getter de nome do ItemDeTrabalho
    def get_nome(self) -> str:
        return self.__nome

    # getter de descricao do ItemDeTrabalho
    def get_descricao(self) -> str:
        return self.__descricao

    # getter de valor de xp do ItemDeTrabalho
    def get_xp_valor(self) -> int:
        return self.__xp_valor

    # getter de status do ItemDeTrabalho
    def get_status(self) -> StatusItem:
        return self.__status

    # Setters:

    # setter de id do ItemDeTrabalho
    def set_id(self, id: int):
        self.__id = id

    # setter de nome do ItemDeTrabalho
    def set_nome(self, nome: str):
        self.__nome = nome

    # setter de descricao do ItemDeTrabalho
    def set_descricao(self, descricao: str):
        self.__descricao = descricao

    # setter de valor de xp do ItemDeTrabalho
    def set_xp_valor(self, xp_valor: int):
        self.__xp_valor = xp_valor

    # setter de status do ItemDeTrabalho
    def set_status(self, status: StatusItem):
        if isinstance(status, StatusItem):
            self.__status = status
        else:
            raise ValueError(
                "status tem que ser uma instancia de StatusItem"
            )  # possivelmente trocar por algum tratamento de erro adequado

    # Métodos abstratos da classe:

    @abstractmethod
    def calcular_progresso(self):
        pass

    @abstractmethod
    def contribuir_para_projeto(self):
        pass

    @abstractmethod
    def obter_tipo_item(self):
        pass
