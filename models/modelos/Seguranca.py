# Esse arquivo foi gerado por IA generativa, utilizando ChatGPT

import bcrypt


# gera um hash seguro da senha
def gerar_hash_senha(senha: str) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha.encode("utf-8"), salt)


# verifica se a senha fornecida corresponde ao hash armazenado
def verificar_senha(senha: str, hash_senha: bytes) -> bool:
    return bcrypt.checkpw(senha.encode("utf-8"), hash_senha)
