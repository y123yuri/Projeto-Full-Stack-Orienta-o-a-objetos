document.addEventListener("DOMContentLoaded", function() {
    // Função para alternar a exibição da seção de edição de username
    document.querySelector(".edit-username").addEventListener("click", function() {
        const usernameSection = document.querySelector(".edit-username-section");
        usernameSection.style.display = usernameSection.style.display === "block" ? "none" : "block";
    });

    // Função para salvar o novo username
    document.querySelector(".save-username-button").addEventListener("click", function() {
        const newUsername = document.querySelector("#new-username").value;
        
        if (newUsername) {
            document.querySelector(".profile-name").textContent = newUsername;
            alert("Username atualizado com sucesso!");
            document.querySelector(".edit-username-section").style.display = "none";
        } else {
            alert("Por favor, insira um novo username!");
        }
    });

    // Alteração de senha
    document.querySelector(".change-password").addEventListener("click", function() {
        alert("Alteração de senha ainda não implementada");
    });

    // Exclusão de conta
    document.querySelector(".delete-account").addEventListener("click", function() {
        if (confirm("Tem certeza que deseja excluir sua conta?")) {
            alert("Conta excluída com sucesso!");
        }
    });

    // Abrir mensagens
    document.querySelector(".open-messages").addEventListener("click", function() {
        alert("Abrindo mensagens privadas...");
    });

    // Ver cupons
    document.querySelector(".view-coupons").addEventListener("click", function() {
        alert("Visualizando cupons...");
    });
});