from Participacao import Participacao
from Tarefa import Tarefa

class Dono(Participacao):

    #Construtor da classe Dono
    def __init__(self, usuario_id: int, projeto_id: int, id: int | None = None, xp_participacao: int = 0, ativa: bool = True):
        super().__init__(usuario_id, projeto_id, id, xp_participacao, ativa)
    
    #Implementações concretas dos metodos abstratos de Participacao:

    #Retorna a classificacao da Participacao (DONO)
    def get_classificacao(self) -> str:
        return "DONO"
    
    #Retorna se pode criar tarefa (True)
    def pode_criar_tarefa(self) -> bool:
        return True
    
    #Retorna se pode adicionar membro (True)
    def pode_adicionar_membro(self) -> bool:
        return True
    
    #Retorna se pode remover membro (True)
    def pode_remover_membro(self) -> bool:
        return True
    
    #Retorna se pode atualizar status (True)
    def pode_atualizar_status(self, tarefa: Tarefa) -> bool:
        return True



