function buscarProjeto(){
    const id_projeto = document.getElementById("id_projeto").value

    fetch(`/api/projeto/${id_projeto}`, {
        method: 'GET'
    })
    .then(res => res.json())
    .then(projeto => {
        const container = document.getElementById("projeto_buscado")
        container.innerHTML = ''
        if (projeto) {
            const h1 = document.createElement("h1")
            h1.innerHTML = projeto.nome

            const p = document.createElement("p")
            p.innerHTML = projeto.descricao

            const botao_solicitar = document.createElement("button")
            botao_solicitar.className = "btn btn-secondary m3"
            botao_solicitar.innerHTML = "Solicitar"
            botao_solicitar.addEventListener("click", e => {solicitar_acesso(projeto.id)})

            document.getElementsByClassName("container-header")[0].appendChild(botao_solicitar)
            container.appendChild(h1)
            container.appendChild(p)
        } else {
            alert("Projeto não encontrado");
        }
    });

}

function solicitar_acesso(projeto_id){
    fetch(`/api/projeto/${projeto_id}/solicitar_entrar`, {
    method: 'POST'
  })
    .then(res => {
      if (res.ok) {
        alert("Solicitação enviada!");
      } else {
        alert("Erro ao solicitar.");
      }
    });
}
