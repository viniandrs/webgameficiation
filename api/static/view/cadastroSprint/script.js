function initPage(params) {
  const form = document.getElementById('form-criar-sprint');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const body = Object.fromEntries(formData.entries());
    body.projeto_id = params.projeto_id
    console.log(formData, body)

    const response = await fetch('/api/sprint', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    if (response.ok) {
      loadPage('projeto', { id: params.projeto_id });
    } else {
      alert('Erro ao salvar tarefa');
    }
  });
}
