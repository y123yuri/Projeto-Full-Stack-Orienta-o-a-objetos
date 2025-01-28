document.getElementById('cadastroForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Evita o envio do formulário

    const senha = document.getElementById('senha').value;
    const confirmaSenha = document.getElementById('confirmaSenha').value;
    const erroMensagem = document.getElementById('erroMensagem');

    if (senha !== confirmaSenha) {
        erroMensagem.textContent = 'As senhas não conferem!';
        erroMensagem.style.display = 'block';
    } else {
        erroMensagem.style.display = 'none';
        alert('Cadastro realizado com sucesso!');
        // Aqui você pode enviar os dados para o backend
        this.submit(); // Enviar o formulário se tudo estiver correto
    }
});
