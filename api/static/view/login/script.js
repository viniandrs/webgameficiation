function initPage(params) {
  const form = document.getElementById('login');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const body = Object.fromEntries(formData.entries());

    const response = await fetch('/api/usuario/verifica-senha', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    const data = await response.json();

    if (response.ok && data.ok) {
      await fetch('/api/login/' + data.usuario_id, {
        method: 'POST'
      });
      loadPage('home');
    } else {
      alert('Email ou Senha Incorretos');
    }
  })

}

function criarUsuario(){
  loadPage("cadastroUsuario")
}
