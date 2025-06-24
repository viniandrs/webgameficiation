function initPage(params) {
  const form = document.getElementById('form-criar-usuario');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const body = Object.fromEntries(formData.entries());

    const response = await fetch('/api/usuario', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    const resp = await response.json();

    if (resp.ok ) {
      alert("Logado com sucesso")
      console.log(resp)
      await fetch('/api/login/'+resp.usuario_id, {
        method: 'POST'
      });
      loadPage('home');
    } else {
      alert(resp.message);
    }
  });
}
