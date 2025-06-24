function initPage(params) {
  const projeto_id = params.id;

  fetch(`/api/projeto/${projeto_id}`)
    .then(res => res.json())
    .then(projeto => renderProjeto(projeto));
}

async function renderProjeto(projeto) {
  const res = await fetch('/api/participante/' + projeto.id);
  const participante = await res.json();
  const content = document.getElementById('content');
  content.innerHTML = `
    <div class="container mt-4">
      <h1>${projeto.nome}</h1>
      <h3>${projeto.descricao}</h3>
      <h6 id="ud_sala">ID do Projeto: ${projeto.id}</h6>
      ${participante.classificacao=="DONO" ? `<button class="btn btn-sm btn-outline-secondary ms-2" onclick="editarProjeto(${projeto.id})">Editar Projeto</button>` : ''}
      ${participante.classificacao=="DONO" ? `<button class="btn btn-sm btn-outline-danger ms-2" onclick="excluirProjeto(${projeto.id})">Excluir Projeto</button>` : ''}
      ${participante.classificacao=="DONO" ? `<button class="btn btn-sm btn-outline-info ms-2" onclick="handleParticipantes(${projeto.id})">Gerenciar Participantes</button>` : ''}
      <p id="classificacao_usuario">Classificação: ${participante.classificacao}</p>
      <p id="classificacao_usuario">Contribuição: <span id="span_xp">${participante.xp}</span>xp</p>
      <button class="btn btn-sm btn-outline-info ms-2" onclick="handleRanking(${projeto.id})">Gerar ranking Contribuicoes</button>

      <div class="my-4">
      <h5>Progresso do Projeto / ${projeto.xp_meta}xp</h5>
      <div class="progress">
        <div class="progress-bar bg-success" role="progressbar"
            style="width: ${Math.min(100, (projeto.xp_acumulado / projeto.xp_meta) * 100)}%"
            aria-valuenow="${projeto.xp_acumulado}"
            aria-valuemin="0"
            aria-valuemax="${projeto.xp_meta}">
          ${projeto.xp_acumulado} / ${projeto.xp_meta} XP
        </div>
      </div>
    </div>


      <div class="row">
        <div class="col-md-8">
          <h4>Sprints</h4>
        ${participante.classificacao=="DONO" ? `<button class="btn btn-sm btn-outline-primary ms-2" onclick="criarSprint(${projeto.id})">Criar Sprint</button>` : ''}
          <div id="sprints-list"></div>
        </div>
        <div class="col-md-4" id="detalhes_container">
          
        </div>
      </div>
    </div>
  `;

  renderSprintsComTarefas(projeto.sprint_metas, projeto.id, participante);
}

async function renderSprintsComTarefas(sprints, id_projeto, participante) {
  const container = document.getElementById('sprints-list');
  container.innerHTML = '';

  sprints.forEach((sprint, sprintIndex) => {
    const sprintDiv = document.createElement('div');
    sprintDiv.className = 'mb-4';
    const header = document.createElement('div');
    header.className = 'd-flex align-items-center justify-content-between';

    const divTitulo = document.createElement("div")
    divTitulo.className = 'd-flex'
    const titulo = document.createElement('h5');
    titulo.className = 'mb-2';
    titulo.innerHTML = "<strong>"+sprint.nome+"</strong>"
    titulo.style.cursor = 'pointer'
    titulo.addEventListener("click", (e)=>{
      handleDetalhesSprint(e, sprint, id_projeto, participante.classificacao)
    })
    const infos = document.createElement("p")
    infos.textContent = " ("+sprint.xp_valor+"xp)  -  "+ sprint.data
    divTitulo.appendChild(titulo)
    divTitulo.appendChild(infos)

    const botaoAdicionar = document.createElement('button');
    botaoAdicionar.className = 'btn btn-sm btn-outline-primary';
    botaoAdicionar.innerHTML = '<strong>+</strong>';
    botaoAdicionar.onclick = () =>
      loadPage('cadastroTarefa', {
        sprint_id: sprint.id,
        projeto_id: id_projeto
      });

    header.appendChild(divTitulo);
    if(participante.classificacao == "DONO") header.appendChild(botaoAdicionar);
    sprintDiv.appendChild(header);

    const tarefasDiv = document.createElement('div');
    tarefasDiv.className = 'ps-3';

    sprint.tarefas.forEach((item, tarefaIndex) => {
      const canCheck = (participante.classificacao == 'DONO' || item.participacao_responsavel_id === participante.id);
      let [statusClass, textoMostrado] = acharCorStatus(item.status)

      const itemId = `sprint-${sprintIndex}-tarefa-${tarefaIndex}`;

      const itemWrapper = document.createElement('div');
      itemWrapper.className = 'd-flex align-items-start mb-3';

      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.name = item.id;
      checkbox.checked = item.status === 'CONCLUIDA';
      checkbox.disabled = !canCheck || item.status == "AGUARDANDO_REASSIGNACAO";
      checkbox.className = 'custom-circle-checkbox me-3';
      checkbox.addEventListener('change', () => toggleConcluir(item.id, checkbox, id_projeto));

      const accordion = document.createElement('div');
      accordion.className = 'accordion w-100';
      accordion.id = `accordion-${itemId}`;
      accordion.innerHTML = `
        <div class="accordion-item">
          <h2 class="accordion-header" id="heading-${itemId}">
            <div class="d-flex align-items-center">
              <button class="accordion-button collapsed bg-white w-100" type="button"
                data-bs-toggle="collapse"
                data-bs-target="#collapse-${itemId}"
                aria-expanded="false"
              >
                <div class="fw-semibold me-3">${item.nome}</div>
                <div class="ms-auto text-end">
                  <div class="text-muted small">${item.data || ''}</div>
                  <span class="badge ${statusClass}">${textoMostrado}</span>
              ${participante.classificacao == 'DONO' ? `<button class="btn btn-sm btn-outline-danger ms-2" onclick="excluirTarefa(${item.id}, ${id_projeto})">🗑</button>` : ''}
                </div>
              </button>
            </div>
          </h2>
          <div id="collapse-${itemId}" class="accordion-collapse collapse" aria-labelledby="heading-${itemId}" data-bs-parent="#accordion-${itemId}">
            <div class="accordion-body">
             <div class="row">
              <div class="col-6">
                <strong>Responsável:</strong>
                  <select ${(canCheck && item.status !='CONCLUIDA') ||  item.status == 'AGUARDANDO_REASSIGNACAO'? '': 'disabled'} id="select-${item.id}" class="form-select form-select-sm w-auto d-inline ms-2" data-tarefa-id="${item.id}" onchange="atualizarResponsavel(this, ${id_projeto})">
                    <option value="">Carregando...</option>
                  </select>
              </div>
              <div class="col-6"><strong>Prazo:</strong> ${item.prazo}</div>
             </div>


              <p><strong>Descrição: </strong>${item.descricao || 'Sem descrição.'}</p>
              <p><strong>XP valor:</strong> ${item.xp_valor|| 0}</p>
              ${participante.classificacao == 'DONO' ? `<button class="btn btn-sm btn-outline-secondary mt-2" onclick="editarTarefa(${item.id}, ${id_projeto})">Editar</button>` : ''}
            </div>
          </div>
        </div>
      `;
      itemWrapper.appendChild(checkbox);
      itemWrapper.appendChild(accordion);
      tarefasDiv.appendChild(itemWrapper);

      createListenerSelect(accordion, item, id_projeto, participante)
      
    });

    sprintDiv.appendChild(tarefasDiv);
    container.appendChild(sprintDiv);
  });
}

function createListenerSelect(accordion, item, id_projeto, participante){
  fetch(`/api/projeto/${id_projeto}/participantes`)
    .then(res => res.json())
    .then(participantes => {
      const select = accordion.querySelector(`[data-tarefa-id="${item.id}"]`);
      select.innerHTML = '';
      const opcaoVazia = document.createElement('option');
      opcaoVazia.value = "";
      select.appendChild(opcaoVazia)

      if(item.status== 'AGUARDANDO_REASSIGNACAO' && participante.classificacao=='PARTICIPANTE'){
        const option_unica = document.createElement('option');
        option_unica.value = participante.id;
        option_unica.textContent = "atribuir para si";
        select.appendChild(option_unica)
      }else{
        participantes.forEach(p => {
          if(p.participacao_habilitada){
            const option = document.createElement('option');
            option.value = p.id;
            option.textContent = p.usuario_nome;
            if (p.id == item.participacao_responsavel_id) option.selected = true;
            select.appendChild(option);     
          }
        });
      }
    });
}

function toggleConcluir(itemId, checkboxEl, id_projeto) {
  const wrapper = checkboxEl.closest('.d-flex');
  const badge = wrapper.querySelector('.badge');

  const concluida = checkboxEl.checked;
  let endpoint
  if(concluida) {
    endpoint = `/api/item/${itemId}/concluir`
  }else{
    endpoint = `/api/item/${itemId}/inacabada`
  }

  fetch(endpoint, { method: 'POST' })
    .then(res => {
      if (res.ok) {
        loadPage("projeto", {id: id_projeto})
      } else {
        alert("Erro ao excluir tarefa.");
      }
    });
}

function editarTarefa(tarefa_id, projeto_id) {
  loadPage('editarTarefa', {
    tarefa_id: tarefa_id,
    projeto_id: projeto_id
  });
}

function excluirTarefa(tarefa_id, projeto_id) {
  if (!confirm("Tem certeza que deseja excluir esta tarefa?")) return;

  fetch(`/api/tarefa/${tarefa_id}`, {
    method: 'DELETE'
  })
    .then(res => {
      if (res.ok) {
        alert("Tarefa excluída com sucesso!");
        loadPage('projeto', { id: projeto_id });
      } else {
        alert("Erro ao excluir tarefa.");
      }
    });
}

function excluirProjeto(projeto_id) {
  if (!confirm("Tem certeza que deseja excluir este Projeto?")) return;

  fetch(`/api/projeto/${projeto_id}`, {
    method: 'DELETE'
  })
    .then(res => {
      if (res.ok) {
        alert("Projeto excluída com sucesso!");
        loadPage('home');
      } else {
        alert("Erro ao excluir o projeto.");
      }
    });
}

function excluirSprint(sprint_id, projeto_id) {
  if (!confirm("Tem certeza que deseja excluir esta Sprint?")) return;

  fetch(`/api/sprint/${sprint_id}`, {
    method: 'DELETE'
  })
    .then(res => {
      if (res.ok) {
        alert("Sprint excluída com sucesso!");
        loadPage('projeto', { id: projeto_id });
      } else {
        alert("Erro ao excluir tarefa.");
      }
    });
}

function editarSprint(sprint_id, projeto_id) {
  loadPage('editarSprint', {
    sprint_id: sprint_id,
    projeto_id: projeto_id
  });
}

function editarProjeto(projeto_id) {
  loadPage('editarProjeto', {projeto_id: projeto_id});
}

function handleDetalhesSprint(e, sprint, id_projeto, classificacao){
  const detalhes_container = document.getElementById("detalhes_container")

  detalhes_container.innerHTML = ''

  const card_div = document.createElement("div")
  card_div.innerHTML= `
    <div class="card">
    <h5 class="card-header">[Sprint]</h5>
    <div class="card-body">
      <h5 class="card-title">${sprint.nome}</h5>
      <h6>Valor XP: ${sprint.xp_valor}</h5>
      <h6>Data Alvo: ${sprint.data}</h5>
      <p class="card-text">${sprint.descricao}</p>
      ${classificacao=="DONO"? `
      <button class="btn btn-sm btn-outline-secondary ms-2" onclick="editarSprint(${sprint.id}, ${id_projeto})">Editar</button>
      <button class="btn btn-sm btn-outline-danger ms-2" onclick="excluirSprint(${sprint.id}, ${id_projeto})">🗑</button>`:``}
    </div>
  </div>`

  detalhes_container.appendChild(card_div)
}

function atualizarResponsavel(selectEl, projeto_id) {
  const tarefa_id = selectEl.getAttribute('data-tarefa-id');

  const novo_responsavel_id = selectEl.value;

  fetch(`/api/tarefa/${tarefa_id}/responsavel`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ responsavel_id: novo_responsavel_id })
  })
    .then(res => {
      if (res.ok) {
        alert("Responsável atualizado!");
        loadPage('projeto', { id: projeto_id });
      } else {
        alert("Erro ao atualizar responsável.");
      }
    });
}

function handleParticipantes(projeto_id) {
  loadPage('mostrarParticipantes', { projeto_id });
}

function criarSprint(projeto_id){
  loadPage('cadastroSprint', {projeto_id: projeto_id})
}

function handleRanking(projeto_id){
  fetch(`/api/projeto/${projeto_id}/ranking`)
  .then(res => res.json())
  .then(participantes =>{
    const detalhes_container = document.getElementById("detalhes_container")
    detalhes_container.innerHTML = ''
    let texto_dados = ''
    if(participantes){
      let contador = 1
      
      participantes.forEach(participante =>{
        texto_dados += `<p>${contador}: ${participante.usuario_nome} - ${participante.xp_participacao}xp`
        contador++
      })

      const card_div = document.createElement("div")
      card_div.innerHTML= `        
      <div class="card">
        <h5 class="card-header">Ranking top 10</h5>
        <div class="card-body">
          `+texto_dados+`
        </div>
      </div>`

  detalhes_container.appendChild(card_div)
    }else{
      detalhes_container.innerHTML = 'Erro ao carregar Ranking'
    }
  })
}

function acharCorStatus(status){
  switch (status) {
    case 'CONCLUIDA':
      return ['bg-success text-white', 'concluida']
    case 'PENDENTE':
      return ['bg-danger text-white', 'pendente']
    case 'AGUARDANDO_REASSIGNACAO':
      return ['bg-warning text-white', 'aguardando responsável']
    default:
      return ['bg-secondary', 'status desconhecido']
  }
}