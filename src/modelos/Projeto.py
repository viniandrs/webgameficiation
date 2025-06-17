class Projeto:

    #Construtor da classe Projeto
    def __init__(self, id: int, nome: str, descricao: str, xp_meta: int):
        self.__id = id
        self.__nome = nome
        self.__descricao = descricao
        self.__xp_acumulado = 0
        self.__xp_meta = xp_meta
    
    #getters:

    #getter da id do Projeto
    def get_id(self) -> int:
        return self.__id
    
    #getter do nome do Projeto
    def get_nome(self) -> str:
        return self.__nome
    
    #getter da descricao do Projeto
    def get_descricao(self) -> str:
        return self.__descricao
    
    #getter do xp meta do Projeto
    def get_xp_meta(self) -> int:
        return self.__xp_meta
    
    #getter do xp acumulado do Projeto
    def get_xp_acumulado(self) -> int:
        return self.__xp_acumulado

    #setters:

    #setter de nome, altera nome do Projeto
    def set_nome(self, novo_nome: str):
        self.__nome = novo_nome

    #setter de descricao, altera descricao do Projeto
    def set_descricao(self, nova_descricao: str):
        self.__descricao = nova_descricao

    #setter de xp_meta, altera xp_meta do Projeto
    def set_xp_meta(self, novo_xp_meta: int):
        self.__xp_meta = novo_xp_meta


    #Gerenciamento de XP:

    #adiciona um valor de xp ao valor acumulado de xp do Projeto
    def adicionar_xp(self, valor: int):
        if valor > 0:
            self.__xp_acumulado += valor

    #remove um valor de xp do valor acumulado de xp
    def remover_xp(self, valor: int):
        if valor > 0:
            self.__xp_acumulado = max(0, self.__xp_acumulado - valor)

    #retorna o progresso total de xp do projeto, de 0 a 1
    def progresso_total(self) -> float:
        if self.__xp_meta == 0:     # pra ter certeza que nao sera dividido por 0
            return 0.0
        return min(1.0, self.__xp_acumulado / self.__xp_meta)

    #Representação textual:

    #retorna dados sobre o projeto em formato de string
    def __str__(self) -> str:
        porcentagem_concluida = self.progresso_total() * 100
        return (f"Projeto '{self.__nome}': {porcentagem_concluida:.2f} % concluído. "
                f"XP acumulado do projeto: {self.__xp_acumulado}. "
                f"XP meta do projeto: {self.__xp_meta}.")





