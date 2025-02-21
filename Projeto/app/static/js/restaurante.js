document.getElementById("comentarioForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Impede o recarregamento da página

    let comentarioInput = document.getElementById("comentarioInput");
    let restauranteId = document.getElementById("restauranteId").value;
    let comentarioTexto = comentarioInput.value.trim();

    if (comentarioTexto === "") {
        alert("O comentário não pode estar vazio!");
        return;
    }

    fetch("/adicionar_comentario", {
        method: "POST",
        body: new URLSearchParams({
            "conteudo": comentarioTexto,
            "restaurante_id": restauranteId
        }),
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            let comentariosLista = document.getElementById("comentariosLista");
            
            // Criando um novo elemento de comentário
            let novoComentario = document.createElement("div");
            novoComentario.classList.add("comment");
            novoComentario.innerHTML = `<strong>${data.username}:</strong> "${data.conteudo}"`;

            // Adicionando o novo comentário ao topo da lista
            comentariosLista.prepend(novoComentario);

            // Limpando o campo de comentário
            comentarioInput.value = "";
        }
    })
    .catch(error => console.error("Erro ao adicionar comentário:", error));
});





//-----------------------------------------FOTOS
document.addEventListener("DOMContentLoaded", function () {
    console.log("Fotos carregadas no frontend:", fotos); // Debug

    let slider = document.getElementById("imageSlider");
    let thumbnails = document.getElementById("thumbnails");

    if (fotos.length > 0) {
        fotos.forEach((foto, index) => {
            let img = document.createElement("img");
            img.src = foto.trim();
            img.alt = "Foto do restaurante";
            if (index === 0) img.classList.add("active");
            slider.appendChild(img);

            let thumb = document.createElement("img");
            thumb.src = foto.trim();
            thumb.onclick = () => goToSlide(index);
            if (index === 0) thumb.classList.add("active");
            thumbnails.appendChild(thumb);
        });

        initializeCarousel();
    }
});

function initializeCarousel() {
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

    // Expõe as funções globalmente para serem chamadas no HTML
    window.nextSlide = nextSlide;
    window.prevSlide = prevSlide;
    window.goToSlide = goToSlide;
}
