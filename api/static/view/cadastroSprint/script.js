function initPage(params) {
  const form = document.getElementById('form-criar-sprint');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const body = Object.fromEntries(formData.entries());
    body.projeto_id = params.projeto_id

    const response = await fetch('/api/sprint', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    data = await response.json()
    if (response.ok) {
      alert("Sprint criada corretamentea")
      loadPage('projeto', { id: params.projeto_id });
    } else {
      alert('Erro ao salvar a sprint meta');
    }
  });
}
