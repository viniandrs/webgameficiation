from datetime import date
from ItemDeTrabalho import ItemDeTrabalho, StatusItem
from Tarefa import Tarefa
from Projeto import Projeto

class SprintMeta(ItemDeTrabalho):

    #Construtor da classe SprintMeta
    def __init__(self, id: int, projeto_id: int, nome: str, descricao: str, xp_valor: int, status: StatusItem, data_alvo: date):
        super().__init__(id, projeto_id, nome, descricao, xp_valor, status)
        self.__data_alvo = data_alvo
        self.__tarefas = []     # a lista de tarefas associadas


    #Getters:

    #getter da data alvo do SprintMeta
    def get_data_alvo(self) -> date:
        return self.__data_alvo
    
    #getter da lista de tarefas do SprintMeta
    def get_tarefas(self):
        return self.__tarefas


    #Setters:

    #setter da data alvo do SprintMeta
    def set_data_alvo(self, data_alvo: date):
        self.__data_alvo = data_alvo


    #Metodos relacionados a lista de tarefas:

    #adiciona uma tarefa a lista de tarefas do SprintMeta
    def adicionar_tarefa(self, tarefa: Tarefa):
        if not isinstance(tarefa, Tarefa):
            raise TypeError("O objeto a ser adicionado a lista de tarefas do Sprint Meta deve ser um objeto Tarefa")    # possivelmente substituir por um tratamento de erro amis adequado posteriormente
        else:
            self.__tarefas.append(tarefa)
    
    #remove uma tarefa da lista de tarefas do SprintMeta
    def remover_tarefa(self, tarefa: Tarefa):
        if tarefa in self.__tarefas:
            self.__tarefas.remove(tarefa)
        else:
            raise ValueError("A tarefa não está associada a este SprintMeta")   # possivelmente substituir por um tratamento de erro mais adequado posteriormente


    #Implementação dos métodos abstratos de ItemDeTrabalho:

    #retorna o progresso em termos de xp conseguido em relação ao xp total do sprint. retorna um flaot de 0 a 1
    def calcular_progresso(self) -> float:
        contador_xp_tarefas_concluidas = 0
        contador_xp_total_tarefas = 0
        for tarefa in self.__tarefas:
            contador_xp_total_tarefas += tarefa.get_xp_valor()
            if tarefa.get_status() == StatusItem.CONCLUIDA:
                contador_xp_tarefas_concluidas += tarefa.get_xp_valor()
        return min(1, contador_xp_tarefas_concluidas / contador_xp_total_tarefas)
        

    #chamada quando todas as tarefas foram concluidas
    def contribuir_para_projeto(self, projeto: Projeto):
        if projeto.get_id == self.get_projeto_id():
            if all(tarefa.get_status() == StatusItem.CONCLUIDA for tarefa in self.__tarefas):
                projeto.adicionar_xp(self.get_xp_valor())

    
    #retorna o tipo de ItemDeTrabalho (SprintMeta)
    def obter_tipo_item(self):
        return "SprintMeta"
