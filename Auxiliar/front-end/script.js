document.getElementById('cadastroForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Impede o envio do formulário

    // Obtém os valores do formulário
    var nome = document.getElementById('nome').value;
    var email = document.getElementById('email').value;
    var dataNascimento = document.getElementById('dataNascimento').value;
    var foto = document.getElementById('foto').files[0]; // Pega o arquivo da foto

    // Validação simples
    if(nome === '' || email === '' || dataNascimento === '') {
        alert('Por favor, preencha todos os campos obrigatórios.');
        return false;
    }

    // Adicione aqui o código para o upload da foto
    // E o código para salvar os dados no servidor ou localmente

    alert('Formulário enviado com sucesso!');
    // Aqui você pode limpar o formulário ou fazer outras ações necessárias
});

// const novoUsuario = {
//     nome: "João Silva",
//     email: "joao.silva@example.com",
//     dataNascimento: "1990-05-14"
// };

function criarUsuario(data) {
    fetch('https://localhost:3000/api/users/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Sucesso:', data);
    })
    .catch((error) => {
        console.error('Erro:', error);
    });
}

function carregarUsuarios() {
    fetch('http://localhost:3000/api/users')
        .then(response => response.json())
        .then(usuarios => {
            const grid = document.getElementById('usuariosGrid');
            grid.innerHTML = ''; // Limpa a grade antes de adicionar novos usuários
            usuarios.forEach(usuario => {
                const col = document.createElement('div');
                col.className = 'col-md-3 mb-3';
                col.innerHTML = `
                    <div class="card" style="position: relative;">
                        <img style='width:150px; height:150px; margin-left:25%;' src="${usuario.fotoUrl || 'path/to/default/photo.jpg'}" class="card-img-top" alt="Foto do Usuário">
                        <div class="card-body">
                            <h5 class="card-title">${usuario.nome}</h5>
                            <p class="card-text">${usuario.email}</p>
                            <p class="card-text">${new Date(usuario.dataNascimento).toLocaleDateString()}</p>
                        </div>
                        <div style="position: absolute; top: 10px; right: 10px;">
                            <button onclick="editarUsuario('${usuario.id}')" class="btn btn-primary btn-sm" style="margin-right: 5px;">
                                <i class="fa fa-edit"></i>
                            </button>
                            <button onclick="removerUsuario('${usuario.id}')" class="btn btn-danger btn-sm">
                                <i class="fa fa-trash"></i>
                            </button>
                        </div>
                    </div>
                `;
                grid.appendChild(col);
            });
        })
        .catch(error => console.error('Falha ao buscar usuários:', error));
}

function editarUsuario(id) {
    // Implemente a lógica para editar o usuário
    console.log('Editando usuário com ID:', id);
}

function removerUsuario(id) {
    // Mensagem de confirmação
    const confirmar = confirm('Tem certeza que deseja remover este usuário?');
    if (confirmar) {
        deletarUsuario(id);
    } else {
        console.log('Ação de remoção cancelada.');
    }
}


// Chame carregarUsuarios() quando a página carregar ou quando necessário
document.addEventListener('DOMContentLoaded', carregarUsuarios);


function lerUsuarioPorId(id) {
    fetch(`https://localhost:3000/api/users/${id}`)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Erro:', error));
}

function lerUsuarioPorId(id) {
    fetch(`https://suaapi.com/api/usuarios/${id}`)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Erro:', error));
}

function deletarUsuario(id) {
    fetch(`https://localhost:3000/api/users/${id}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => console.log('Usuário deletado com sucesso:', data))
    .catch(error => console.error('Erro:', error));
}

// Exemplo de uso
d//eletarUsuario(1); // Substitua 1 pelo ID do usuário a ser deletado


// Exemplo de uso
//lerUsuarioPorId(1); // Substitua 1 pelo ID do usuário desejado


// Exemplo de uso
//lerUsuarioPorId(1); // Substitua 1 pelo ID do usuário desejado

// Chamando a função para ler usuários
//lerUsuarios();


//criarUsuario(novoUsuario);

