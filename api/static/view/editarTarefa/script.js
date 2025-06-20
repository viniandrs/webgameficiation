function initPage(params) {
  const tarefa_id = params.tarefa_id;
  const projeto_id = params.projeto_id;

  fetch(`/api/tarefa/${tarefa_id}`)
    .then(res => res.json())
    .then(tarefa => {
      document.getElementById('nome').value = tarefa.nome;
      document.getElementById('descricao').value = tarefa.descricao;
      document.getElementById('prazo').value = tarefa.prazo;
      document.getElementById('xp_pontos').value = tarefa.xp_pontos;
    });

  const form = document.getElementById('form-editar-tarefa');
  form.addEventListener('submit', async e => {
    e.preventDefault();

    const dados = {
      nome: document.getElementById('nome').value,
      descricao: document.getElementById('descricao').value,
      prazo: document.getElementById('prazo').value,
      xp_pontos: parseInt(document.getElementById('xp_pontos').value)
    };

    const res = await fetch(`/api/tarefa/${tarefa_id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dados)
    });

    if (res.ok) {
      alert('Tarefa atualizada com sucesso!');
      loadPage('projeto', { id: projeto_id });
    } else {
      alert('Erro ao atualizar tarefa');
    }
  });

  document.getElementById('voltar').onclick = () => {
    loadPage('projeto', { id: projeto_id });
  };
}
