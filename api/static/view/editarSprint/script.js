function initPage(params) {
  const sprint_id = params.sprint_id;
  const projeto_id = params.projeto_id;

  fetch(`/api/sprint/${sprint_id}`)
    .then(res => res.json())
    .then(sprint => {
      document.getElementById('nome').value = sprint.nome;
      document.getElementById('descricao').value = sprint.descricao;
      document.getElementById('data_alvo').value = sprint.data_alvo;
      document.getElementById('xp_valor').value = sprint.xp_valor;
    });

  const form = document.getElementById('form-editar-sprint');
  form.addEventListener('submit', async e => {
    e.preventDefault();

    const dados = {
      nome: document.getElementById('nome').value,
      descricao: document.getElementById('descricao').value,
      data_alvo: document.getElementById('data_alvo').value,
      xp_valor: parseInt(document.getElementById('xp_valor').value)
    };

    const res = await fetch(`/api/sprint/${sprint_id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dados)
    });

    if (res.ok) {
      alert('sprint atualizada com sucesso!');
      loadPage('projeto', { id: projeto_id });
    } else {
      alert('Erro ao atualizar sprint');
    }
  });

  document.getElementById('voltar').onclick = () => {
    loadPage('projeto', { id: projeto_id });
  };
}
