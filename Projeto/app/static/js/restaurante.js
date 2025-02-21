document.addEventListener("DOMContentLoaded", function() {
    let form = document.getElementById("comentarioForm");

    form.addEventListener("submit", function(event) {
        event.preventDefault();  // Impede o recarregamento da página

        let comentarioTexto = document.getElementById("comentarioTexto").value;
        let actionUrl = form.getAttribute("action");  // Obtém a URL correta do action

        if (!actionUrl.includes("/adicionar_comentario/")) {
            console.error("Erro: URL de ação inválida.", actionUrl);
            return;
        }

        fetch(actionUrl, {
            method: "POST",
            body: JSON.stringify({ conteudo: comentarioTexto }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                let comentariosLista = document.getElementById("comentariosLista");
                let novoComentario = document.createElement("div");
                novoComentario.classList.add("comment");
                novoComentario.innerHTML = `<strong>${data.nome}:</strong> "${data.conteudo}"`;
                comentariosLista.appendChild(novoComentario);

                document.getElementById("comentarioTexto").value = ""; // Limpa o campo de comentário
            } else {
                alert("Erro ao enviar comentário!");
            }
        })
        .catch(error => console.error("Erro:", error));
    });
});



let currentIndex = 0;
        let slides = document.querySelectorAll('.slider img');
        let thumbnails = document.querySelectorAll('.thumbnails img');
        let interval = setInterval(nextSlide, 4000); // Transição automática a cada 4 segundos

        // Atualiza a imagem ativa do slider
        function updateSlide(index) {
            slides.forEach(slide => slide.classList.remove('active'));
            thumbnails.forEach(thumb => thumb.classList.remove('active'));
            slides[index].classList.add('active');
            thumbnails[index].classList.add('active');
        }

        // Avança para a próxima imagem
        function nextSlide() {
            currentIndex = (currentIndex + 1) % slides.length;
            updateSlide(currentIndex);
        }

        // Volta para a imagem anterior
        function prevSlide() {
            currentIndex = (currentIndex - 1 + slides.length) % slides.length;
            updateSlide(currentIndex);
        }

        // Acessa uma imagem específica ao clicar na miniatura
        function goToSlide(index) {
            currentIndex = index;
            updateSlide(currentIndex);
            clearInterval(interval);
            interval = setInterval(nextSlide, 4000);
        }

        // Alterna o estado do botão de favorito
        function toggleFavorite(restaurantId) {
            let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
            const restaurantId = button.getAttribute('data-id');
            
            if (favorites.includes(restaurantId)) {
                favorites = favorites.filter(id => id !== restaurantId); // Remove se já estiver salvo
            } else {
                favorites.push(restaurantId); // Adiciona se não estiver salvo
            }
        
            localStorage.setItem('favorites', JSON.stringify(favorites));
            updateFavoriteButton(restaurantId);
        }
        
        // Atualiza o botão com base nos favoritos salvos
        function updateFavoriteButton(restaurantId) {
            const button = document.querySelector(`.favorite[data-id="${restaurantId}"]`);
            let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
        
            if (button) {
                button.classList.toggle('active', favorites.includes(restaurantId));
                button.textContent = favorites.includes(restaurantId) ? "❤️" : "♡";
            }
        }
        
        // Inicializa os favoritos ao carregar a página
        document.addEventListener("DOMContentLoaded", () => {
            let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
        
            document.querySelectorAll('.favorite').forEach(button => {
                const restaurantId = button.getAttribute('data-id');
                updateFavoriteButton(restaurantId);
        
                button.addEventListener('click', () => {
                    toggleFavorite(restaurantId);
                    updateFavoriteButton(restaurantId);
                });
            });
        });