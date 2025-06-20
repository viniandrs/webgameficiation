async function loadUsers() {
  try {
    const res = await fetch('/api/usuarios');
    if (!res.ok) throw new Error('Erro ao carregar usuários');
    const users = await res.json();

    const listDiv = document.getElementById('user-list');
    listDiv.innerHTML = '';
    users.forEach(user => {
      const btn = document.createElement('button');
      btn.textContent = user.nome;
      btn.className = 'btn btn-primary';
      btn.addEventListener('click', async () => {
        await fetch('/api/login/'+user.id, {
          method: 'POST'
        });
        loadPage('home');
      });
      listDiv.appendChild(btn);
    });
  } catch (err) {
    document.getElementById('user-list').innerHTML = `<p class="text-danger">${err.message}</p>`;
  }
}

loadUsers();
