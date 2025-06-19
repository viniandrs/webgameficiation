from .Seguranca import gerar_hash_senha, verificar_senha

class Usuario:
    """
    Representa a entidade Usuario no sistema

    Encapsula os atributos de um usuário e gerencia a segurança da senha

    Um objeto Usuario pode ser inicializado de duas formas diferentes:
    1. Novo usuário, com senha em texto claro (uso do construtor __init__)
    2. Usuário existente (lido do BD), com senha_hash conhecida (uso do método de classe criar_com_hash)
    """

    #construtor da classe Usuario
    def __init__(self, nome: str, email: str, senha: str):
        self.__id = None #Inicialização para novos usuários
        self.__nome = nome
        self.__email = email
        self.__senha_hash = gerar_hash_senha(senha)    # a ser armazenada como hash
    
    @classmethod
    def criar_com_hash(cls, id_usuario: int, nome: str, email: str, senha_hash: bytes):
        """
        Construtor alternativo para Usuario. 
        
        Cria uma instância de Usuario a partir de um hash da senha já existente
        """

        instancia = cls.__new__(cls) #Cria uma nova instância sem chamar o __init__
        instancia.__id = id_usuario
        instancia.__nome = nome
        instancia.__email = email
        instancia.__senha_hash = senha_hash
        return instancia

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

    #getter de senha, retorna o hash da senha do usuario
    def get_senha_hash(self) -> str:
        return self.__senha_hash
    
    #setters:

    #setter de id, altera id para novo_nome
    def set_id(self, novo_id: int):
        self.__id = novo_id

    #setter de nome, altera nome para novo_nome
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

    def __str__(self) -> str:
        """
        Retorna uma representação textual do objeto Usuario
        """
        return f"Usuario(id: {self.get_id()}, nome: {self.get_nome()}, email: {self.get_email()})"

