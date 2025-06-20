async function showUser() {
  try {
    const res = await fetch('/api/sessao');
    const data = await res.json();
    document.getElementById('home-user').textContent = data.usuario.nome || 'visitante';
  } catch {
    document.getElementById('home-user').textContent = 'visitante';
  }
}

showUser();
