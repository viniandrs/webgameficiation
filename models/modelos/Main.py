# codigozinho apenas para testar as implementacoes ate aqui. gerado pelo chatGPT


from Usuario import Usuario
from Projeto import Projeto
from Dono import Dono
from Participante import Participante

# Criando um novo usuário com senha
usuario = Usuario(1, "João", "joao@email.com", "minhaSenha123")

# Verificando login
print(usuario.verificar_senha("minhaSenha123"))  # ✅ True
print(usuario.verificar_senha("senhaErrada"))  # ❌ False

# Tentando alterar senha com a senha errada
print(usuario.alterar_senha("errada", "novaSenha123"))  # ❌ False

# Alterando senha corretamente
print(usuario.alterar_senha("minhaSenha123", "novaSenha123"))  # ✅ True

# Verificando nova senha
print(usuario.verificar_senha("novaSenha123"))  # ✅ True

# Criando um novo projeto
projeto = Projeto(
    id=1,
    nome="Sistema Gamificado MC322",
    descricao="Projeto final da disciplina para aplicar POO com gamificação.",
    xp_meta=1000,
)

# Imprime o estado inicial do projeto
print(projeto)

# Adicionando XP simulado (tarefas realizadas)
projeto.adicionar_xp(150)
projeto.adicionar_xp(200)

print("\nApós progresso:")
print(projeto)

# Tentando remover XP (simulando erro, ou revisão de tarefa)
projeto.remover_xp(100)

print("\nApós correção (remoção de XP):")
print(projeto)

# Testando limites
projeto.adicionar_xp(900)  # ultrapassando a meta
print("\nApós adicionar muito XP:")
print(projeto)


dono = Dono(id=1, usuario_id=10, projeto_id=100)

print("\nClassificação:", dono.get_classificacao())
print("Pode criar tarefa?", dono.pode_criar_tarefa())
print("XP atual:", dono.get_xp())

# Simulando contribuição
dono.adicionar_xp(150)
print("XP após contribuição:", dono.get_xp())


p = Participante(id=2, usuario_id=20, projeto_id=100)

print("\nClassificação:", p.get_classificacao())
print("Pode criar tarefa?", p.pode_criar_tarefa())
print("Pode atualizar status?", p.pode_atualizar_status())

p.adicionar_xp(50)
print("XP:", p.get_xp())
