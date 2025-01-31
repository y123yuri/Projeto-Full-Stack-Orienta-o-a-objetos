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
        function toggleFavorite() {
            const button = document.querySelector('.favorite');
            const isActive = button.classList.toggle('active');
            button.textContent = isActive ? "❤️" : "♡";
        }