from Seguranca import gerar_hash_senha, verificar_senha

class Usuario:

    #construtor da classe Usuario
    def __init__(self, id: int, nome: str, email: str, senha: str):
        self.__id = id
        self.__nome = nome
        self.__email = email
        self.__senha_hash = gerar_hash_senha(senha)    # a ser armazenada como hash
    
    #getters:

    #getter de id, retorna id do usuario
    def get_id(self) -> int:
        return self.__id

    #getter de nome, retorna nome do usuario
    def get_nome(self) -> str:
        return self.__nome
    
    #getter de email, retorna email do usuario
    def get_email(self) -> str:
        return self.__email
    
    #setters:

    #setter de nome, altera id para novo_nome
    def set_nome(self, novo_nome: str):
        self.__nome = novo_nome

    #setter de email, altera email para novo_email
    def set_email(self, novo_email: str):
        self.__email = novo_email

    #verificação e alteração de senha com hash:

    #verifica a senha usando o metodo de Seguranca.py, retorna True se a senha passada é a correta e False caso contrário
    def verificar_senha(self, senha: str) -> bool:
        return verificar_senha(senha, self.__senha_hash)

    #altera a senha usando o metodo de Seguranca.py, verifica se a senha fornecida é a correta antes
    #retorna True se foi possível alterar a senha e False caso contrário (caso a senha fornecida estiver errada)
    def alterar_senha(self, senha_atual: str, nova_senha: str) -> bool:
        if self.verificar_senha(senha_atual):
            self.__senha_hash = gerar_hash_senha(nova_senha)
            return True
        return False

