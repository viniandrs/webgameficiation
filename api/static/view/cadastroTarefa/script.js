function initPage(params) {
  const sprint_id = params.sprint_id;
  const form = document.getElementById('tarefa-form');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const body = Object.fromEntries(formData.entries());
    body.sprint_id = sprint_id;

    const response = await fetch('/api/tarefa', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    if (response.ok) {
      const tarefa = await response.json();
      loadPage('projeto', { id: params.projeto_id });
    } else {
      alert('Erro ao salvar tarefa');
    }
  });
}
