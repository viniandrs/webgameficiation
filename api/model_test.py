from abc import ABC, abstractmethod
from datetime import date


# ==== Usuário ====
class Usuario:
    def __init__(self, id, nome, email, senha):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha


# ==== Projeto ====
class Projeto:
    def __init__(self, id, nome, descricao, xp_acumulado, xp_meta):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.xp_acumulado = xp_acumulado
        self.xp_meta = xp_meta
        self.sprints = []


# ==== Interface IGerenciadorXP ====
class IGerenciadorXP(ABC):
    @abstractmethod
    def adicionar_xp(self, valor):
        pass

    @abstractmethod
    def remover_xp(self, valor):
        pass

    @abstractmethod
    def obter_xp(self):
        pass


# ==== Participacao ====
class Participacao(IGerenciadorXP):
    def __init__(
        self,
        id,
        usuario_id,
        projeto_id,
        xp_participacao,
        participacao_habilitada,
        classificacao,
    ):
        self.id = id
        self.usuario_id = usuario_id
        self.projeto_id = projeto_id
        self.xp_participacao = xp_participacao
        self.participacao_habilitada = participacao_habilitada
        self.classificacao = classificacao

    def obter_classificacao(self):
        return self.classificacao

    def pode_atualizar_status_tarefa(self):
        return self.classificacao == "DONO"

    def adicionar_xp(self, valor):
        self.xp_participacao += valor

    def remover_xp(self, valor):
        self.xp_participacao -= valor

    def obter_xp(self):
        return self.xp_participacao


class Dono(Participacao):
    def __init__(self, *args):
        super().__init__(*args)
        self.classificacao = "DONO"


class Participante(Participacao):
    def __init__(self, *args):
        super().__init__(*args)
        self.classificacao = "PARTICIPANTE"


# ==== ItemDeTrabalho ====
class ItemDeTrabalho(ABC):
    def __init__(self, id, projeto_id, nome, descricao, xp_valor, status):
        self.id = id
        self.projeto_id = projeto_id
        self.nome = nome
        self.descricao = descricao
        self.xp_valor = xp_valor
        self.status = status

    def get_status(self):
        return self.status


# ==== SprintMeta ====
class SprintMeta(ItemDeTrabalho):
    def __init__(self, id, projeto_id, nome, descricao, xp_valor, status, data_alvo):
        super().__init__(id, projeto_id, nome, descricao, xp_valor, status)
        self.data_alvo = data_alvo


# ==== Tarefa ====
class Tarefa(ItemDeTrabalho):
    def __init__(
        self,
        id,
        projeto_id,
        nome,
        descricao,
        xp_valor,
        status,
        prazo,
        participacao_responsavel_id,
        sprint_meta_id,
    ):
        super().__init__(id, projeto_id, nome, descricao, xp_valor, status)
        self.prazo = prazo
        self.participacao_responsavel_id = participacao_responsavel_id
        self.sprint_meta_id = sprint_meta_id
