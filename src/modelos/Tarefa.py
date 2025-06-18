from datetime import date
from ItemDeTrabalho import ItemDeTrabalho, StatusItem
from Projeto import Projeto
from Participacao import Participacao

class Tarefa(ItemDeTrabalho):

    #Construtor da classe tarefa
    def __init__(self, id: int, projeto_id: int, nome: str, descricao: str, xp_valor: int, status: StatusItem,
                 participacao_responsavel_id: int, prazo: date, sprint_meta_id: int):
        super().__init__(id, projeto_id, nome, descricao, xp_valor, status)
        self.__participacao_responsavel_id = participacao_responsavel_id
        self.__prazo = prazo
        self.__sprint_meta_id = sprint_meta_id
    

    #Getters:

    #getter do id da participação responsavel pela Tarefa
    def get_participacao_responsavel_id(self) -> int:
        return self.__participacao_responsavel_id
    
    #getter do prazo da Tarefa
    def get_prazo(self) -> date:
        return self.__prazo
    
    #getter do id da SprintMeta que a Tarefa faz parte
    def get_sprint_meta_id(self) -> int:
        return self.__sprint_meta_id
    

    #Setters:

    #setter do prazo da Tarefa
    def set_prazo(self, prazo: date):
        self.__prazo = prazo
    
    #setter do id da participação responsavel pela Tarefa
    def set_participacao_responsavel_id(self, participacao_responsavel_id: int):
        self.__participacao_responsavel_id = participacao_responsavel_id
        
    #setter do id da SprintMeta que a Tarefa faz parte
    def set_sprint_meta_id(self, sprint_meta_id: int):
        self.__sprint_meta_id = sprint_meta_id

    #setter do status da Tarefa. Se a tarefa estiver sido concluida, contribui para projeto com seu xp atribuido
    def set_status(self, status: StatusItem):
        if isinstance(status, StatusItem):
            self.__status = status
            self.contribuir_para_projeto()
        else:
            raise ValueError("status tem que ser uma instancia de StatusItem")  # possivelmente trocar por algum tratamento de erro adequado
        

    #Representação textual do objeto:

    #retorna dados sobre a tarefa em formato de string
    def __str__(self):
        return (f"Tarefa '{self.__nome}':\nStatus: {self.__status.name}\nXP: {self.__xp_valor}\nPrazo: {self.__prazo}")
    

    #Implementação dos métodos abstratos de ItemDeTrabalho:

    # retorna 1 caso a tarefa esteja concluida e 0 caso nao
    def calcular_progresso(self):
        if self.__status == StatusItem.CONCLUIDA:
            return 1
        return 0
    
    #caso a tarefa esteja concluida, chama adicionar_xp do projeto e da participacao envolvidos
    def contribuir_para_projeto(self, projeto: Projeto, participacao: Participacao):
        if self.__status == StatusItem.CONCLUIDA:
            if projeto.get_id == self.__projeto_id:
                if participacao.get_id == self.__participacao_responsavel_id:
                    projeto.adicionar_xp(self.__xp_valor)
                else:
                    raise ValueError("A participacao fornecida não está associada a essa tarefa")   # substituir por um tratamento de erro adequado
            else:
                raise ValueError("O projeto fornecido não está associado a essa tarefa")    # substituir por um tratamento de erro adequado
    
    #retorna o tipo de ItemDeTrabalho (TAREFA)
    def obter_tipo_item(self) -> str:
        return "TAREFA"
    

