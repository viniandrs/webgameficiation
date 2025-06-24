function initPage(params) {
  const projeto_id = params.projeto_id;

  fetch(`/api/projeto/${projeto_id}`)
    .then(res => res.json())
    .then(projeto => {
      document.getElementById('nome').value = projeto.nome;
      document.getElementById('descricao').value = projeto.descricao;
    });

  const form = document.getElementById('form-editar-projeto');
  form.addEventListener('submit', async e => {
    e.preventDefault();

    const dados = {
      nome: document.getElementById('nome').value,
      descricao: document.getElementById('descricao').value,
    };

    const res = await fetch(`/api/projeto/${projeto_id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dados)
    });

    if (res.ok) {
      alert('Projeto atualizado com sucesso!');
      loadPage('projeto', { id: projeto_id });
    } else {
      alert('Erro ao atualizar projeto');
    }
  });

  document.getElementById('voltar').onclick = () => {
    loadPage('home');
  };
}
