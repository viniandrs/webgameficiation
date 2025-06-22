function initPage(params) {
  const projeto_id = params.projeto_id;
  fetch(`/api/projeto/${projeto_id}/participantes`)
    .then(res => res.json())
    .then(exibirParticipantes);

  document.getElementById('voltar').onclick = () =>
    loadPage('projeto', { id: projeto_id });
}

function exibirParticipantes(participantes) {
  console.log(participantes)
  const tbody = document.getElementById('tabela-participantes');
  tbody.innerHTML = '';

  participantes.forEach(p => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${p.usuario_id}</td>
      <td>${p.usuario_nome}</td>
      <td>${p.xp_participacao}</td>
      <td>
        <select class="form-select form-select-sm" data-id="${p.id}">
          <option value="DONO" ${p.classificacao==='DONO'?'selected':''}>DONO</option>
          <option value="PARTICIPANTE" ${p.classificacao==='PARTICIPANTE'?'selected':''}>PARTICIPANTE</option>
        </select>
      </td>
      <td>
        <input type="checkbox" data-id="${p.usuario_id}" class="form-check-input" ${p.participacao_habilitada?'checked':''}>
      </td>
    `;
    tbody.append(tr);
  });

  tbody.querySelectorAll('select').forEach(el =>
    el.addEventListener('change', () => atualizarParticipante(el)));
  tbody.querySelectorAll('input[type="checkbox"]').forEach(el =>
    el.addEventListener('change', () => atualizarParticipante(el)));
}

function atualizarParticipante(el) {
  const participante_id = el.getAttribute('data-id');
  const row = el.closest('tr');
  const classificacao = row.querySelector('select').value;
  const habilitado = row.querySelector('input[type="checkbox"]').checked;

  fetch(`/api/projeto/participante/${participante_id}`, {
    method: 'PUT',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ classificacao, habilitado })
  })
    .then(res => {
      if (!res.ok) alert('Erro ao atualizar participante');
    });
}
