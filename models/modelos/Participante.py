from .Participacao import Participacao
from .Tarefa import Tarefa


class Participante(Participacao):

    # Construtor da classe Participante
    def __init__(
        self,
        usuario_id: int,
        projeto_id: int,
        id: int | None = None,
        xp_participacao: int = 0,
        ativa: bool = False,
    ):
        super().__init__(usuario_id, projeto_id, id, xp_participacao, ativa)

    # Implementações concretas dos metodos abstratos de Participacao:

    # Retorna a classificacao da Participacao (PARTICIPANTE)
    def get_classificacao(self) -> str:
        return "PARTICIPANTE"

    # Retorna se pode criar tarefa (False)
    def pode_criar_tarefa(self) -> bool:
        return False

    # Retorna se pode adicionar membros (False)
    def pode_adicionar_membro(self) -> bool:
        return False

    # Retorna se pode remover membros (False)
    def pode_remover_membro(self) -> bool:
        return False

    # Retorna se pode atualizar status: True caso seja responsavel pela tarefa e False caso contrário
    def pode_atualizar_status(self, tarefa: Tarefa) -> bool:
        if tarefa.get_participacao_responsavel_id() == self.get_id():
            return True
        return False
