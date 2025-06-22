function initPage() {
  const form = document.getElementById('form-criar-projeto');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const body = Object.fromEntries(formData.entries());

    const response = await fetch('/api/projeto', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    if (response.ok) {
        alert("Projeto Criado com sucesso")
        const res = await response.json()
        loadPage('projeto', { id: res.projeto_id });
    } else {
      alert('Erro ao salvar o projeto');
    }
  });
}
