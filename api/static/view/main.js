async function loadPage(page, params = {}) {
  try {
    const response = await fetch(`/api/page/${page}`);
    if (!response.ok) throw new Error('Página não encontrada');
    const html = await response.text();
    document.getElementById('content').innerHTML = html;

    loadCSS(`static/view/${page}/style.css`);
    loadScript(`static/view/${page}/script.js`, params);

    updateCurrentUserDisplay();
  } catch (err) {
    document.getElementById('content').innerHTML = `<p class="text-danger">${err.message}</p>`;
  }
}

function loadCSS(url) {
  const oldLink = document.getElementById('page-style');
  if (oldLink) oldLink.remove();

  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = url;
  link.id = 'page-style';
  document.head.appendChild(link);
}

function loadScript(url, params = {}) {
  const oldScript = document.getElementById('page-script');
  if (oldScript) oldScript.remove();

  const script = document.createElement('script');
  script.src = url;
  script.id = 'page-script';
  script.onload = () => {
    if (window.initPage) window.initPage(params);
  };
  document.body.appendChild(script);
}

async function updateCurrentUserDisplay() {
  try {
    const resUser = await fetch('/api/sessao');
    const data = await resUser.json();
    const el = document.getElementById('current-user');

    if (data.usuario) {
      el.textContent = `Usuário: ${data.usuario.nome}`;
      document.getElementById("nav-buttons").style.display = "block"
      await carregarProjetos();
    } else {
      el.textContent = '';
      document.getElementById("nav-buttons").style.display = "none"
    }
  } catch {
    document.getElementById('current-user').textContent = '';
    renderProjectList([]);
  }
}

async function carregarProjetos() {
  try {
    const res = await fetch('/api/projetos');
    const projetos = await res.json();
    renderProjectList(projetos);
  } catch {
    renderProjectList([]);
  }
}

function renderProjectList(projetos) {
  const listDiv = document.getElementById('group-list');
  listDiv.innerHTML = '';
  if (projetos.length === 0) {
    listDiv.innerHTML = '<p class="p-2">Nenhum projeto</p>';
    return;
  }

  projetos.forEach(projeto => {
    const a = document.createElement('a');
    a.href = "#";
    a.className = "d-block p-2 project-link";
    a.textContent = projeto.nome;
    a.addEventListener('click', async e => {
      e.preventDefault();
      await carregarDetalhesProjeto(projeto.id);
    });
    listDiv.appendChild(a);
  });
}

async function carregarDetalhesProjeto(projetoId) {
  try {
    const res = await fetch(`/api/projeto/${projetoId}`);
    if (!res.ok) throw new Error('Projeto não encontrado');
    const projeto = await res.json();
    loadPage('projeto', projeto)
  } catch (err) {
    document.getElementById('content').innerHTML = `<p class="text-danger">${err.message}</p>`;
  }
}

function criarProjeto(){
  loadPage("cadastroProjeto")
}

function entrarProjeto(){
  loadPage("entrarProjeto")
}

document.getElementById('change-user')?.addEventListener('click', e => {
  e.preventDefault();
  loadPage('login');
});

document.getElementById('logout')?.addEventListener('click', async e => {
  e.preventDefault();
  await fetch('/api/logout', { method: 'POST' });
  loadPage('login');
});

loadPage('home');
