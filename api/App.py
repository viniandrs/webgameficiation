import os
import sys

sys.path.append(os.path.join(os.getcwd()))  # add src to PYTHONPATH

from datetime import date
from flask import Flask, jsonify, send_from_directory, session, render_template, request

from models.modelos.Projeto import Projeto
from models.modelos.Tarefa import Tarefa
from models.modelos.SprintMeta import SprintMeta
from models.modelos.Dono import Dono
from models.modelos.Participante import Participante
from models.modelos.ItemDeTrabalho import StatusItem
from models.modelos.Usuario import Usuario
from models.modelos.Participacao import Participacao
from models.modelos.ItemDeTrabalho import ItemDeTrabalho

from models.acesso_dados.UsuarioDao import UsuarioDao
from models.acesso_dados.ProjetoDao import ProjetoDao
from models.acesso_dados.ParticipacaoDao import ParticipacaoDao
from models.acesso_dados.TarefaDao import TarefaDao
from models.acesso_dados.SprintMetaDao import SprintMetaDao

app = Flask(__name__)
app.secret_key = "supersecreto"

# instantiating DAOs
usuariosDAO = UsuarioDao() 
projetosDAO = ProjetoDao()
participacoesDAO = ParticipacaoDao()
tarefasDAO = TarefaDao()
sprint_metasDAO = SprintMetaDao()
# ==== ROTAS ====


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/page/<page_name>")
def serve_page_data(page_name):
    try:
        return send_from_directory(f"static/view/{page_name}", f"{page_name}.html")
    except:
        return jsonify({"error": "Página não encontrada"}), 404


@app.route("/api/usuarios")
def serve_users_data():
    usuarios = usuariosDAO.listar_todos()
    data = []
    if usuarios:
        for usuario in usuarios:
            data.append(
                {"id": usuario.get_id(), "nome": usuario.get_nome(), "email": usuario.get_email()}
            )

    return jsonify(data)


@app.route("/api/login/<int:usuario_id>", methods=["POST"])
def api_login(usuario_id):
    usuario = usuariosDAO.buscar_por_id(usuario_id)
    if not usuario:
        return jsonify({"ok": False, "message": "Usuário não encontrado"}), 404
    session["usuario_id"] = usuario_id
    return jsonify({"success": True})

@app.route("/api/usuario", methods=["POST"])
def api_criar_usuario():
    data = request.json
    
    novo_usuario = Usuario(
        nome=data["nome"],
        email=data["email"],
        senha=data["senha"]
    )

    usuario_existente = usuariosDAO.buscar_por_email(novo_usuario.get_email())
    if not usuario_existente:
        novo_usuario = usuariosDAO.inserir(novo_usuario)
        return jsonify({"ok": True, "usuario_id": novo_usuario.get_id()})
    else:
        return jsonify({"ok": False, "message": "Email já em uso"})

@app.route("/api/usuario/verifica-senha", methods=["POST"])
def api_verificar_senha_usuario():
    data = request.json
    usuario = usuariosDAO.buscar_por_email(data["email"])
    if usuario.verificar_senha(data["senha"]):
        return jsonify({"usuario_id": usuario.get_id(), "ok":True})
    else:
        return jsonify({"ok": False})
    


@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.pop("usuario_id", None)
    return jsonify({"success": True})


@app.route("/api/sessao")
def api_sessao():
    usuario_id = session.get("usuario_id")
    if not usuario_id:
        return jsonify({"usuario": None})
    
    usuario = usuariosDAO.buscar_por_id(usuario_id)
    if not usuario:
        return jsonify({"usuario": None})
    return jsonify({"usuario": {"id": usuario.get_id(), "nome": usuario.get_nome()}})


@app.route("/api/projetos")
def api_projeto_para_cliente_logado():
    usuario_id = session.get("usuario_id")
    if not usuario_id:
        return jsonify([])

    projetos_usuario = []
    projetos = projetosDAO.buscar_por_usuario_id(usuario_id)

    if projetos:
        for proj in projetos:
            projetos_usuario.append({"id": proj.get_id(), "nome": proj.get_nome()})

    return jsonify(projetos_usuario)

def __verificar_sprint_completa(sprint_meta_id):
    tarefas = tarefasDAO.buscar_tarefas_sprint(sprint_meta_id)
    for tarefa in tarefas:
        if tarefa.get_status() != StatusItem.CONCLUIDA:
            return False
        
    return True

def __alterar_bonus_responsaveis(projeto_id, sprint_meta_id, funcao):
    participacoes = projetosDAO.buscar_membros_do_projeto(projeto_id)
    tarefas = tarefasDAO.buscar_tarefas_sprint(sprint_meta_id)
    sprint = sprint_metasDAO.buscar_por_id(sprint_meta_id)
    for tarefa in tarefas:
        for part in participacoes:
            if tarefa.get_participacao_responsavel_id() == part["id"]:
                participacao_entidade = participacoesDAO.buscar_por_id(part["id"])
                if funcao == 'adicionar':
                    print(tarefa.get_participacao_responsavel_id(), participacao_entidade.get_id())
                    participacao_entidade.adicionar_xp(sprint.get_xp_valor())
                    print("adicionou ", sprint.get_xp_valor())
                elif funcao == 'remover':
                    participacao_entidade.remover_xp(sprint.get_xp_valor())
                    print("removeu ",sprint.get_xp_valor())
                participacoesDAO.atualizar(participacao_entidade)

@app.route("/api/item/<int:item_id>/concluir", methods=["POST"])
def api_concluir_item(item_id):
    tarefa = tarefasDAO.buscar_por_id(item_id)
    sprint_meta_id = tarefa.get_sprint_meta_id()

    inicialmente_completa = __verificar_sprint_completa(sprint_meta_id)

    participacao =participacoesDAO.buscar_por_id(tarefa.get_participacao_responsavel_id())
    participacao.adicionar_xp(tarefa.get_xp_valor())
    participacoesDAO.atualizar(participacao)
    tarefasDAO.atualizar_status_tarefa(item_id, StatusItem.CONCLUIDA)

    projeto = projetosDAO.buscar_por_id(tarefa.get_projeto_id())
    projeto.adicionar_xp(tarefa.get_xp_valor())
    projetosDAO.atualizar(projeto)

    final_completa = __verificar_sprint_completa(sprint_meta_id)

    if not inicialmente_completa and final_completa:
        __alterar_bonus_responsaveis(tarefa.get_projeto_id(), sprint_meta_id, 'adicionar')
    
    return jsonify({"ok": True})


@app.route("/api/item/<int:item_id>/inacabada", methods=["POST"])
def api_desconcluir_item(item_id):
    tarefa = tarefasDAO.buscar_por_id(item_id)
    sprint_meta_id = tarefa.get_sprint_meta_id()

    inicialmente_completa = __verificar_sprint_completa(sprint_meta_id)

    participacao =participacoesDAO.buscar_por_id(tarefa.get_participacao_responsavel_id())
    participacao.remover_xp(tarefa.get_xp_valor())
    participacoesDAO.atualizar(participacao)
    tarefasDAO.atualizar_status_tarefa(item_id, StatusItem.PENDENTE)

    projeto = projetosDAO.buscar_por_id(tarefa.get_projeto_id())
    projeto.remover_xp(tarefa.get_xp_valor())
    projetosDAO.atualizar(projeto)

    final_completa = __verificar_sprint_completa(sprint_meta_id)

    if inicialmente_completa and not final_completa:
        print("desfez completo")
        __alterar_bonus_responsaveis(tarefa.get_projeto_id(), sprint_meta_id, 'remover')

    return jsonify({"ok": True})


@app.route("/api/participante/<int:projeto_id>")
def api_participante_projeto(projeto_id):
    usuario_id = session.get("usuario_id")
    if not usuario_id:
        return jsonify()

    participacao = participacoesDAO.buscar_participacao_usuario_projeto(usuario_id, projeto_id)

    dados ={
        "id": participacao.get_id(),
        "usuario_id": participacao.get_usuario_id(),
        "projeto_id": participacao.get_projeto_id(),
        "classificacao": participacao.get_classificacao(),
        "xp": participacao.get_xp(),
        "ativo": participacao.is_ativa()
    }
    return jsonify(dados)


@app.route("/api/page/cadastroTarefa")
def page_cadastro_tarefa():
    return send_from_directory(f"static/view/cadastroTarefa", f"cadastroTarefa.html")


@app.route("/api/tarefa", methods=["POST"])
def api_criar_tarefa():
    data = request.json

    sprint = sprint_metasDAO.buscar_por_id(data["sprint_id"])

    nova_tarefa = Tarefa(
        nome=data["nome"],
        descricao=data["descricao"],
        prazo=data["prazo"],
        xp_valor=int(data["xp_pontos"]),
        status=StatusItem.AGUARDANDO_REASSIGNACAO,
        sprint_meta_id=data["sprint_id"],
        participacao_responsavel_id=None,
        projeto_id=sprint.get_projeto_id()
    )

    nova_tarefa = tarefasDAO.inserir(nova_tarefa)

    projeto = projetosDAO.buscar_por_id(nova_tarefa.get_projeto_id())
    projeto.set_xp_meta(projeto.get_xp_meta() + nova_tarefa.get_xp_valor())
    projetosDAO.atualizar(projeto)

    return jsonify({"ok": True})


@app.route("/api/tarefa/<int:tarefa_id>", methods=["DELETE"])
def excluir_tarefa(tarefa_id):
    tarefa = tarefasDAO.buscar_por_id(tarefa_id)
    projeto = projetosDAO.buscar_por_id(tarefa.get_projeto_id())
    if tarefa.get_xp_valor():
        projeto.set_xp_meta(projeto.get_xp_meta() - tarefa.get_xp_valor())
        projetosDAO.atualizar(projeto)
    tarefasDAO.remover(tarefa_id)
    return "", 204


@app.route("/api/page/editarTarefa")
def page_editar_tarefa():
    return send_from_directory(f"static/view/editarTarefa", f"editarTarefa.html")


@app.route("/api/tarefa/<int:tarefa_id>", methods=["GET"])
def get_tarefa(tarefa_id):
    tarefa = tarefasDAO.buscar_por_id(tarefa_id)
    return jsonify(
        {
            "id": tarefa.get_id(),
            "nome": tarefa.get_nome(),
            "descricao": tarefa.get_descricao(),
            "prazo": str(tarefa.get_prazo()),
            "xp_pontos": tarefa.get_xp_valor(),
            "status": tarefa.get_status().name,
            "sprint_id": tarefa.get_sprint_meta_id(),
        }
    )


@app.route("/api/tarefa/<int:tarefa_id>", methods=["PUT"])
def atualizar_tarefa(tarefa_id):
    data = request.get_json()
    tarefa = tarefasDAO.buscar_por_id(tarefa_id)

    antigos_pontos = tarefa.get_xp_valor()

    tarefa.set_nome(data["nome"])
    tarefa.set_descricao(data["descricao"])
    tarefa.set_prazo(data["prazo"])
    tarefa.set_xp_valor(data["xp_pontos"])
    tarefasDAO.atualizar(tarefa)

    if tarefa.get_xp_valor() != antigos_pontos:
        diferenca = tarefa.get_xp_valor() - antigos_pontos
        projeto = projetosDAO.buscar_por_id(tarefa.get_projeto_id())
        projeto.set_xp_meta(projeto.get_xp_meta() + diferenca)
        projetosDAO.atualizar(projeto)

    return jsonify({"ok": True})


@app.route("/api/sprint/<int:sprint_id>", methods=["DELETE"])
def excluir_sprint(sprint_id):
    try:
        tarefas = tarefasDAO.buscar_tarefas_sprint(sprint_id)
        soma_xp = sum([tarefa.get_xp_valor() for tarefa in tarefas])
        if soma_xp:
            projeto = projetosDAO.buscar_por_id(tarefas[0].get_projeto_id())
            projeto.set_xp_meta(projeto.get_xp_meta() - soma_xp)
            projetosDAO.atualizar(projeto)
        sprint_metasDAO.remover(sprint_id)
    except:
        return jsonify({"ok": False})
    return "", 204


@app.route("/api/sprint/<int:sprint_id>", methods=["PUT"])
def atualizar_sprint(sprint_id):
    data = request.get_json()

    try:
        sprint = sprint_metasDAO.buscar_por_id(sprint_id)
        sprint.set_nome(data["nome"])
        sprint.set_descricao(data["descricao"])
        sprint.set_data_alvo(data["data_alvo"])
        sprint.set_xp_valor(data["xp_valor"])

        sprint_metasDAO.atualizar(sprint)
    except:
        jsonify({"ok": False})

    return jsonify({"ok": True})


@app.route("/api/sprint/<int:sprint_id>", methods=["GET"])
def get_sprint(sprint_id):
    try:
        sprint = sprint_metasDAO.buscar_por_id(sprint_id)
        print(str(sprint.get_data_alvo()))
        return jsonify(
            {
                "id": sprint.get_id(),
                "nome": sprint.get_nome(),
                "descricao": sprint.get_descricao(),
                "data_alvo": str(sprint.get_data_alvo()),
                "xp_valor": sprint.get_xp_valor(),
                "status": sprint.get_status().name,
            }
        )
    except:
        return jsonify()


@app.route("/api/sprint", methods=["POST"])
def api_criar_sprint():
    data = request.json

    nova_sprint = SprintMeta(
        id=None,
        nome=data["nome"],
        descricao=data["descricao"],
        data_alvo=data["data_alvo"],
        xp_valor= int(data["xp_valor"]),
        status=StatusItem.PENDENTE,
        projeto_id= int(data["projeto_id"])
    )

    try:
        print(data)
        nova_sprint = sprint_metasDAO.inserir(nova_sprint)
        return jsonify({"ok": True})
    except:
        return jsonify({"ok": False})


@app.route("/api/projeto/<int:projeto_id>", methods=["DELETE"])
def excluir_projeto(projeto_id):
    try:
        projetosDAO.remover(projeto_id)
        return "", 204
    except:
        return "", 404

    


@app.route("/api/projeto/<int:projeto_id>", methods=["PUT"])
def atualizar_projeto(projeto_id):
    data = request.get_json()
    print(data)
    try:
        projeto = projetosDAO.buscar_por_id(projeto_id)
        projeto.set_nome(data["nome"])
        projeto.set_descricao(data["descricao"])

        projetosDAO.atualizar(projeto)
    except:
        return jsonify({"message": "Projeto falhou para atualizar"})
    return jsonify({"message": "Projeto atualizado com sucesso"})


@app.route("/api/projeto", methods=["POST"])
def api_criar_projeto():
    data = request.json

    novo_projeto = Projeto(
        nome=data["nome"],
        descricao=data.get("descricao", ""),
        xp_meta=0,
        xp_acumulado=0,
    )

    id_usuario = session.get("usuario_id")
    try:
        novo_projeto = projetosDAO.inserir(novo_projeto)
    except:
        return jsonify("ok", False)

    participante_criador = Dono(
        usuario_id= id_usuario,
        projeto_id= novo_projeto.get_id(),
        xp_participacao= 0,
        ativa=True
    )

    try:
        participante_criador = participacoesDAO.inserir(participante_criador)
    except:
        return jsonify("ok", False)

    return jsonify({"ok": True,"projeto_id":novo_projeto.get_id()})


def achar_tarefas(sprint_id):
    tarefas_filtro = []

    tarefas_achadas = tarefasDAO.buscar_tarefas_sprint(sprint_id)
    for tarefa in tarefas_achadas:
        tarefas_filtro.append(
            {
                "id": tarefa.get_id(),
                "nome": tarefa.get_nome(),
                "prazo": tarefa.get_prazo(),
                "status": tarefa.get_status().name,
                "xp_valor": tarefa.get_xp_valor(),
                "descricao": tarefa.get_descricao(),
                "participacao_responsavel_id": tarefa.get_participacao_responsavel_id(),
            }
        )


    return tarefas_filtro


@app.route("/api/projeto/<int:projeto_id>")
def api_projeto_id(projeto_id):
    projeto = projetosDAO.buscar_por_id(projeto_id)
    if not projeto:
        return jsonify({"error": "Projeto não encontrado"}), 404
    
    sprint_metas = sprint_metasDAO.buscar_sprint_metas_projeto(projeto.get_id())
    sprint_metas_p = [
        {
            "id": s.get_id(),
            "nome": s.get_nome(),
            "status": s.get_status().name,
            "data": s.get_data_alvo(),
            "descricao": s.get_descricao(),
            "xp_valor": s.get_xp_valor(),
            "tarefas": achar_tarefas(s.get_id()),
        }
        for s in sprint_metas
    ]

    return jsonify(
        {
            "id": projeto.get_id(),
            "nome": projeto.get_nome(),
            "descricao": projeto.get_descricao(),
            "xp_meta": projeto.get_xp_meta(),
            "xp_acumulado": projeto.get_xp(),
            "sprint_metas": sprint_metas_p,
        }
    )


@app.route("/api/tarefa/<int:id_tarefa>/responsavel", methods=["PUT"])
def atualizar_responsavel(id_tarefa):
    dados = request.get_json()
    responsavel_id = dados.get("responsavel_id")

    tarefa = tarefasDAO.buscar_por_id(id_tarefa)
    tarefa.set_participacao_responsavel_id(responsavel_id)
    if tarefa.get_status() == StatusItem.AGUARDANDO_REASSIGNACAO:
        tarefa.set_status(StatusItem.PENDENTE)
    tarefasDAO.atualizar(tarefa)

    return jsonify({"ok": True})


@app.route("/api/projeto/<int:id_projeto>/participantes")
def participantes_projeto_todos(id_projeto):
    participantes = projetosDAO.buscar_membros_do_projeto(id_projeto)

    return jsonify(participantes)


@app.route("/api/projeto/<int:id_projeto>/ranking")
def ranking_projeto(id_projeto):
    participantes = projetosDAO.buscar_membros_do_projeto(id_projeto)

    return jsonify(participantes[:9])


@app.route("/api/projeto/participante/<int:participacao_id>", methods=["PUT"])
def atualizar_participacao(participacao_id):
    data = request.get_json()
    habilitado = data["habilitado"]
    
    participante = participacoesDAO.buscar_por_id(participacao_id)
    participante.set_ativa(habilitado)

    if not habilitado:
        tarefas = tarefasDAO.buscar_tarefas_por_id_participacao_responsavel(participacao_id)
        if tarefas:
            for tarefa in tarefas:
                if tarefa.get_status() == StatusItem.PENDENTE:
                    tarefa.set_participacao_responsavel_id(None)
                    tarefa.set_status(StatusItem.AGUARDANDO_REASSIGNACAO)
                    tarefasDAO.atualizar(tarefa)
                    break

    participacoesDAO.atualizar(participante)
    
    return jsonify({"ok": True})


@app.route("/api/projeto/<int:id_projeto>/solicitar_entrar", methods=["POST"])
def usuario_solicita_entrar_projeto(id_projeto):
    id_usuario = session.get("usuario_id")

    nova_participacao = Participante(
        usuario_id=id_usuario, 
        projeto_id=id_projeto, 
        xp_participacao=0, 
        ativa=False
    )

    part_existente = participacoesDAO.buscar_participacao_usuario_projeto(usuario_id=id_usuario, projeto_id=id_projeto)

    if not part_existente:
        participacoesDAO.inserir(nova_participacao)
        return jsonify({"ok": True})
    else:
        return jsonify({
            "ok": False, 
            "message": "usuário já solicitou entrada"
        })


if __name__ == "__main__":
    app.run(debug=True)
