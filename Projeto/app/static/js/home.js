document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search");
    const resultadosLista = document.getElementById("resultados");

    searchInput.addEventListener("input", function () {
        const termo = searchInput.value.trim();

        if (termo.length < 3) {
            resultadosLista.innerHTML = ""; // Limpa a lista se o input estiver vazio
            return;
        }

        fetch(`/buscar?q=${encodeURIComponent(termo)}`)
            .then(response => response.json())
            .then(data => {
                resultadosLista.innerHTML = ""; // Limpa os resultados anteriores

                if (data.length === 0) {
                    resultadosLista.innerHTML = "<li>Nenhum restaurante encontrado</li>";
                } else {
                    data.forEach(restaurante => {
                        const li = document.createElement("li");

                        const link = document.createElement("a");
                        link.href = `/restaurante/${restaurante.id}`; // URL do restaurante
                        link.textContent = restaurante.nome;

                        li.appendChild(link); // Adiciona o link à lista
                        resultadosLista.appendChild(li);
                    });
                }
            })
            .catch(error => console.error("Erro ao buscar restaurantes:", error));
    });
});




//---------------------------------------- fitlro

document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search");
    const resultadosLista = document.getElementById("resultados");
    const tipoComidaSelect = document.getElementById("tipo_comida");

    // 🔹 Carregar os Tipos de Comida no <select>
    fetch("/tipos_comida")
        .then(response => response.json())
        .then(data => {
            data.forEach(tipo => {
                const option = document.createElement("option");
                option.value = tipo;
                option.textContent = tipo;
                tipoComidaSelect.appendChild(option);
            });
        })
        .catch(error => console.error("Erro ao carregar tipos de comida:", error));

    // 🔹 Função de Busca com Filtro de Tipo de Comida
    function buscarRestaurantes() {
        const termo = searchInput.value.trim();
        const tipoComida = tipoComidaSelect.value;

        fetch(`/filtro?q=${encodeURIComponent(termo)}&tipo=${encodeURIComponent(tipoComida)}`)
            .then(response => response.json())
            .then(data => {
                resultadosLista.innerHTML = ""; // Limpa os resultados anteriores

                if (data.length === 0) {
                    resultadosLista.innerHTML = "<li>Nenhum restaurante encontrado</li>";
                } else {
                    data.forEach(restaurante => {
                        const li = document.createElement("li");
                        
                        const link = document.createElement("a");
                        link.href = `/restaurante/${restaurante.id}`; // URL do restaurante
                        link.textContent = restaurante.nome;

                        li.appendChild(link); // Adiciona o link à lista
                        resultadosLista.appendChild(li);
                    });
                }
            })
            .catch(error => console.error("Erro ao buscar restaurantes:", error));
    }

    // 🔹 Disparar a busca ao digitar no input ou mudar o filtro
    searchInput.addEventListener("input", buscarRestaurantes);
    tipoComidaSelect.addEventListener("change", buscarRestaurantes);
});
