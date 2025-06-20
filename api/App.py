import sys
sys.path.append('src') # add src to PYTHONPATH

from datetime import date
from flask import Flask, jsonify, send_from_directory, session, render_template, request
from modelos.Usuario import Usuario
from modelos.Projeto import Projeto
from modelos.Dono import Dono
from modelos.Participante import Participante
from modelos.Tarefa import Tarefa
from modelos.SprintMeta import SprintMeta

from acesso_dados.UsuarioDao import UsuarioDao
from acesso_dados.ProjetoDao import ProjetoDao
from acesso_dados.ParticipacaoDao import ParticipacaoDao

app = Flask(__name__)
app.secret_key = 'supersecreto'

# MOCK DATA: must be raplaced with database queries
#
# # Usuários
# usuarios = [
#     Usuario(1, "Alice", "alice@example.com", "senha123"),
#     Usuario(2, "Bob", "bob@example.com", "senha456"),
#     Usuario(3, "Carol", "carol@example.com", "senha789"),
#     Usuario(4, "David", "david@example.com", "senha000")
# ]

# # Projetos
# projetos = [
#     Projeto(1, "Sistema RH", "Gestão de recursos humanos", 500, 1000),
#     Projeto(2, "Controle Estoque", "Aplicativo para controle de estoque", 300, 800),
#     Projeto(3, "App Viagem", "Organizador de viagens em grupo", 700, 1500),
#     Projeto(4, "API Financeira", "Integração com serviços bancários", 200, 1000)
# ]

# # Participações
# participacoes = [
#     Dono(1, 1, 1, 300, True, 'DONO'),
#     Dono(2, 2, 2, 250, True, 'DONO'),
#     Participante(3, 3, 1, 150, True, 'PARTICIPANTE'),
#     Participante(4, 4, 2, 100, True, 'PARTICIPANTE')
# ]

# # SprintMetas
# sprint_metas = [
#     SprintMeta(1, 1, "Sprint 1 RH", "Entrega inicial", 100, "em progresso", date(2025, 7, 1)),
#     SprintMeta(2, 2, "Sprint 1 Estoque", "Protótipo funcional", 120, "pendente", date(2025, 7, 10)),
#     SprintMeta(3, 3, "Sprint 1 Viagem", "Layout UI", 150, "em progresso", date(2025, 6, 25)),
#     SprintMeta(4, 4, "Sprint 1 API", "Endpoints básicos", 80, "pendente", date(2025, 8, 5))
# ]

# # Tarefas
# tarefas = [
#     Tarefa(1, 1, "Login RH", "Criar tela de login", 50, "pendente", date(2025, 6, 20), 3, 1),
#     Tarefa(2, 2, "Listagem Produtos", "Exibir produtos", 60, "concluida", date(2025, 6, 22), 4, 2),
#     Tarefa(3, 3, "Mapa Interativo", "Integrar mapas", 70, "pendente", date(2025, 7, 1), 3, 3),
#     Tarefa(4, 4, "Consulta Saldo", "Implementar saldo", 40, "pendente", date(2025, 6, 30), 4, 4)
# ]

# querying initial data from database
usuarios = UsuarioDao.listar_todos()
projetos = ProjetoDao.listar_todos()
participacoes = ParticipacaoDao.listar_todos()
# sprint_metas = SprintDao.listar_todos()
# tarefas = TarefaDao.listar_todos()

contador_id_tarefas = 5
contador_id_sprints = 5
contador_id_projetos = 5
contador_id_participante = 5
# ==== ROTAS ====

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/page/<page_name>')
def serve_page_data(page_name):
    try:
        return send_from_directory(f'static/view/{page_name}', f'{page_name}.html')
    except:
        return jsonify({'error': 'Página não encontrada'}), 404
    
@app.route('/api/usuarios')
def serve_users_data():
    data = []
    if usuarios:
        for usuario in usuarios:
            data.append({
                'id': usuario.id,
                'nome': usuario.nome,
                'email': usuario.email
            })

    return jsonify(data)


@app.route('/api/login/<int:usuario_id>', methods=['POST'])
def api_login(usuario_id):
    usuario = next((u for u in usuarios if u.id == usuario_id), None)
    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    session['usuario_id'] = usuario_id
    return jsonify({'success': True})


@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.pop('usuario_id', None)
    return jsonify({'success': True})


@app.route('/api/sessao')
def api_sessao():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'usuario': None})
    usuario = next((u for u in usuarios if u.id == usuario_id), None)
    if not usuario:
        return jsonify({'usuario': None})
    return jsonify({'usuario': {'id': usuario.id, 'nome': usuario.nome}})


@app.route('/api/projetos')
def api_projetos():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify([])

    projetos_usuario = []
    for pa in participacoes:
        if pa.usuario_id == usuario_id and pa.participacao_habilitada:
            proj = next((p for p in projetos if p.id == pa.projeto_id), None)
            if proj:
                projetos_usuario.append({'id': proj.id, 'nome': proj.nome})

    return jsonify(projetos_usuario)

@app.route('/api/item/<int:item_id>/concluir', methods=['POST'])
def api_concluir_item(item_id):
    item = next((t for t in tarefas if t.id == item_id), None)
    if not item:
        return jsonify({'error': 'Item não encontrado'}), 404

    item.status = 'concluida'
    return jsonify({'success': True})

@app.route('/api/item/<int:item_id>/inacabada', methods=['POST'])
def api_desconcluir_item(item_id):
    item = next((t for t in tarefas if t.id == item_id), None)
    if not item:
        return jsonify({'error': 'Item não encontrado'}), 404

    item.status = 'pendente'
    return jsonify({'success': True})

@app.route('/api/participante/<int:projeto_id>')
def api_participante_projeto(projeto_id):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify()

    participante_usuario = None
    for pa in participacoes:
        if pa.usuario_id == usuario_id:
            proj = next((p for p in projetos if projeto_id == pa.projeto_id), None)
            if proj:
                participante_usuario = {
                    'id': pa.id,
                    'xp_participacao': pa.xp_participacao,
                    'participacao_habilitada': pa.participacao_habilitada,
                    'classificacao': pa.obter_classificacao()
                }
                return jsonify(participante_usuario)
    return jsonify()

    
@app.route('/api/page/cadastroTarefa')
def page_cadastro_tarefa():
    return send_from_directory(f'static/view/cadastroTarefa', f'cadastroTarefa.html')

@app.route('/api/tarefa', methods=['POST'])
def api_criar_tarefa():
    global contador_id_tarefas
    data = request.json

    nova_tarefa = Tarefa(
        id=contador_id_tarefas,
        nome=data['nome'],
        descricao=data.get('descricao', ''),
        prazo=data.get('prazo'),
        xp_valor=data['xp_pontos'],
        status='pendente',
        sprint_meta_id=data['sprint_id'], 
        projeto_id=None,
        participacao_responsavel_id=None
    )

    contador_id_tarefas+=1

    tarefas.append(nova_tarefa)

    return jsonify({'status': 'sucess'})

@app.route('/api/tarefa/<int:tarefa_id>', methods=['DELETE'])
def excluir_tarefa(tarefa_id):
    global tarefas
    novas_tarefas = []
    for tarefa in tarefas:
        if tarefa.id != tarefa_id:
            novas_tarefas.append(tarefa)
    
    tarefas = novas_tarefas
    return '', 204


@app.route('/api/page/editarTarefa')
def page_editar_tarefa():
    return send_from_directory(f'static/view/editarTarefa', f'editarTarefa.html')


@app.route('/api/tarefa/<int:tarefa_id>', methods=['GET'])
def get_tarefa(tarefa_id):
    for tarefa in tarefas:
        if tarefa.id == tarefa_id:
            return jsonify({
                'id': tarefa.id,
                'nome': tarefa.nome,
                'descricao': tarefa.descricao,
                'prazo': str(tarefa.prazo),
                'xp_pontos': tarefa.xp_valor,
                'status': tarefa.status,
                'sprint_id': tarefa.sprint_meta_id
            })
    return jsonify()   

@app.route('/api/tarefa/<int:tarefa_id>', methods=['PUT'])
def atualizar_tarefa(tarefa_id):
    data = request.get_json()
    for tarefa in tarefas:
        if tarefa.id == tarefa_id:
            tarefa.nome = data.get('nome', tarefa.nome)
            tarefa.descricao = data.get('descricao', tarefa.descricao)
            tarefa.prazo = data.get('prazo', tarefa.prazo)
            tarefa.xp_valor = data.get('xp_pontos', tarefa.xp_valor)

    return jsonify({'message': 'Tarefa atualizada com sucesso'})


@app.route('/api/sprint/<int:sprint_id>', methods=['DELETE'])
def excluir_sprint(sprint_id):
    global sprint_metas
    global tarefas

    novas_tarefas = []
    novas_sprints = []
    for tarefa in tarefas:
        if tarefa.sprint_meta_id != sprint_id:
            novas_tarefas.append(tarefa)
    
    tarefas = novas_tarefas

    for sprint in sprint_metas:
        if sprint.id != sprint_id:
            novas_sprints.append(sprint)

    sprint_metas = novas_sprints
    return '', 204


@app.route('/api/sprint/<int:sprint_id>', methods=['PUT'])
def atualizar_sprint(sprint_id):
    data = request.get_json()
    for sprint in sprint_metas:
        if sprint.id == sprint_id:
            sprint.nome = data.get('nome', sprint.nome)
            sprint.descricao = data.get('descricao', sprint.descricao)
            sprint.data_alvo = data.get('data_alvo', sprint.data_alvo)
            sprint.xp_valor = data.get('xp_valor', sprint.xp_valor)

    return jsonify({'message': 'Sprint atualizada com sucesso'})

@app.route('/api/sprint/<int:sprint_id>', methods=['GET'])
def get_sprint(sprint_id):
    for sprint in sprint_metas:
        if sprint.id == sprint_id:
            return jsonify({
                'id': sprint.id,
                'nome': sprint.nome,
                'descricao': sprint.descricao,
                'data_alvo': str(sprint.data_alvo),
                'xp_valor': sprint.xp_valor,
                'status': sprint.status
            })
    return jsonify()  

@app.route('/api/sprint', methods=['POST'])
def api_criar_sprint():
    global contador_id_sprints
    data = request.json

    nova_sprint = SprintMeta(
        id=contador_id_tarefas,
        nome=data['nome'],
        descricao=data.get('descricao', ''),
        data_alvo=data.get('data_alvo'),
        xp_valor=data['xp_valor'],
        status='pendente',
        projeto_id=data['projeto_id']
    )

    contador_id_sprints+=1

    sprint_metas.append(nova_sprint)

    return jsonify({'ok': True})

@app.route('/api/projeto/<int:projeto_id>', methods=['DELETE'])
def excluir_projeto(projeto_id):
    global projetos

    novo_projetos = []
    for projeto in projetos:
        if projeto.id != projeto_id:
            novo_projetos.append(projeto)
    
    projetos = novo_projetos
    return '', 204


@app.route('/api/projeto/<int:projeto_id>', methods=['PUT'])
def atualizar_projeto(projeto_id):
    data = request.get_json()
    for projeto in projetos:
        if projeto.id == projeto_id:
            projeto.nome = data.get('nome', projeto.nome)
            projeto.descricao = data.get('descricao', projeto.descricao)
            projeto.xp_meta = data.get('xp_meta', projeto.xp_meta)

    return jsonify({'message': 'Projeto atualizado com sucesso'})

@app.route('/api/projeto', methods=['POST'])
def api_criar_projeto():
    global contador_id_projetos
    global projetos
    global contador_id_participante
    global participacoes

    data = request.json

    novo_projeto = Projeto(
        id=contador_id_projetos,
        nome=data['nome'],
        descricao=data.get('descricao', ''),
        xp_meta=data['xp_meta'],
        xp_acumulado=0
    )
    
    id_usuario = session.get('usuario_id')

    participante_criador = Dono(
        contador_id_participante,
        id_usuario,
        contador_id_projetos,
        0,
        True,
        "DONO"
    )

    contador_id_projetos+=1

    projetos.append(novo_projeto)
    participacoes.append(participante_criador)

    print(novo_projeto.id, participante_criador, (contador_id_projetos-1))

    return jsonify({'projeto_id': (contador_id_projetos-1)})

def achar_tarefas(sprint_id):
    tarefas_filtro = []
    
    for tarefa in tarefas:
        if tarefa.sprint_meta_id == sprint_id:
            tarefas_filtro.append({
                'id': tarefa.id,
                'nome': tarefa.nome,
                'status': tarefa.status,
                'data': tarefa.prazo,
                'xp_valor': tarefa.xp_valor,
                'descricao': tarefa.descricao,
                'participacao_responsavel_id': tarefa.participacao_responsavel_id
            })

    return tarefas_filtro

@app.route('/api/projeto/<int:projeto_id>')
def api_projeto_id(projeto_id):
    projeto = next((p for p in projetos if p.id == projeto_id), None)
    if not projeto:
        return jsonify({'error': 'Projeto não encontrado'}), 404
    sprint_metas_p = [
        {
            'id': s.id,
            'nome': s.nome,
            'status': s.status,
            'data': s.data_alvo,
            'descricao': s.descricao,
            'xp_valor': s.xp_valor,
            'tarefas': achar_tarefas(s.id)
        }
        for s in sprint_metas if s.projeto_id == projeto_id
    ]

    return jsonify({
        'id': projeto.id,
        'nome': projeto.nome,
        'descricao': projeto.descricao,
        'xp_meta': projeto.xp_meta,
        'xp_acumulado': projeto.xp_acumulado,
        'sprint_metas': sprint_metas_p
    })

@app.route("/api/tarefa/<int:id_tarefa>/responsavel", methods=["PUT"])
def atualizar_responsavel(id_tarefa):
    dados = request.get_json()
    responsavel_id = dados.get('responsavel_id')

    for tarefa in tarefas:
        if tarefa.id == id_tarefa:
            tarefa.participacao_responsavel_id = responsavel_id
            break  

    return jsonify({'ok': True})


def achar_usuario(participacao):
    for user in usuarios:
        if user.id == participacao.usuario_id:
            return user


@app.route("/api/projeto/<int:id_projeto>/participantes")
def participantes_projeto_todos(id_projeto):
    participante_json = []

    for part in participacoes:
        if id_projeto == part.projeto_id:
            usuario = achar_usuario(part)
            participante_json.append({
                'id': part.id,
                'nome': usuario.nome,
                'xp_contribuido': part.obter_xp(),
                'classificacao': part.obter_classificacao(),
                'habilitado': part.participacao_habilitada
            })

    return jsonify(participante_json)

@app.route("/api/projeto/<int:id_projeto>/ranking")
def ranking_projeto(id_projeto):
    participante_json = []

    for part in participacoes:
        if id_projeto == part.projeto_id:
            usuario = achar_usuario(part)
            participante_json.append({
                'id': part.id,
                'nome': usuario.nome,
                'xp_contribuido': part.obter_xp(),
                'classificacao': part.obter_classificacao(),
                'habilitado': part.participacao_habilitada
            })
            if len(participante_json) >=10:
                break

    return jsonify(participante_json)

@app.route('/api/projeto/participante/<int:participacao_id>', methods=['PUT'])
def atualizar_participacao(participacao_id):
    global participacoes
    
    data = request.get_json()
    classificacao = data.get('classificacao')
    habilitado = data.get('habilitado')

    for part in participacoes:
        if part.id == participacao_id:
            part.classificacao = classificacao
            part.participacao_habilitada = habilitado
    
    return jsonify({'ok': True})

@app.route("/api/projeto/<int:id_projeto>/solicitar_entrar", methods=['POST'])
def usuario_solicita_entrar_projeto(id_projeto):
    global contador_id_participante
    global participacoes

    id_usuario = session.get('usuario_id')

    nova_participacao = Participante(
        contador_id_participante,
        id_usuario,
        id_projeto,
        0, 
        False,
        "PARTICIPANTE"
    )
    contador_id_participante +=1
    participacoes.append(nova_participacao)
    return jsonify({'ok': True})



if __name__ == '__main__':
    app.run(debug=True)
