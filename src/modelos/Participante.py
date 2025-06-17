from Participacao import Participacao

class Participante(Participacao):

    #Construtor da classe Participante
    def __init__(self, id: int, usuario_id: int, projeto_id: int):
        super().__init__(id, usuario_id, projeto_id)

    #Implementações concretas dos metodos abstratos de Participacao:

    #Retorna a classificacao da Participacao (PARTICIPANTE)
    def get_classificacao(self) -> str:
        return "PARTICIPANTE"

    #Retorna se pode criar tarefa (False)
    def pode_criar_tarefa(self) -> bool:
        return False
    
    #Retorna se pode adicionar membros (False)
    def pode_adicionar_membro(self) -> bool:
        return False

    #Retorna se pode remover membros (False)
    def pode_remover_membro(self) -> bool:
        return False
    
    #Retorna se pode atualizar status: True caso seja responsavel pela tarefa e False caso contrário
    def pode_atualizar_status(self) -> bool:
        # FALTA: validar se o participante é o responsável pela tarefa. se for, retorna True, se nao for retorna False
        return True # apenas para testes
        

