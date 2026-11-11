
// ==========================================
// 1. IDENTIFICAÇÃO DA PÁGINA ATUAL
// ==========================================

const caminhoAtual = window.location.pathname;

const linksMenu = document.querySelectorAll(".menu-item");

linksMenu.forEach((link) => {
    const endereco = new URL(link.href).pathname;

    const paginaInicial = endereco === "/";
    const estaNaPaginaInicial = caminhoAtual === "/";

    const corresponde =
        endereco === caminhoAtual ||
        (!paginaInicial && caminhoAtual.startsWith(endereco + "/"));

    if (corresponde || (paginaInicial && estaNaPaginaInicial)) {
        link.classList.add("active");
        link.setAttribute("aria-current", "page");
    }
});


// ==========================================
// 2. MENU LATERAL RESPONSIVO
// ==========================================

const menuLateral = document.querySelector(".sidebar");
const cabecalho = document.querySelector(".topbar");

if (menuLateral && cabecalho) {

    // Cria o botão de menu
    const botaoMenu = document.createElement("button");

    botaoMenu.classList.add("menu-toggle");
    botaoMenu.type = "button";
    botaoMenu.textContent = "☰";
    botaoMenu.setAttribute("aria-label", "Abrir menu");
    botaoMenu.setAttribute("aria-expanded", "false");

    cabecalho.prepend(botaoMenu);

    // Abre e fecha o menu
    botaoMenu.addEventListener("click", () => {

        const menuAberto = document.body.classList.toggle("sidebar-open");

        botaoMenu.setAttribute("aria-expanded", menuAberto);
        botaoMenu.setAttribute(
            "aria-label",
            menuAberto ? "Fechar menu" : "Abrir menu"
        );
    });

    // Fecha o menu ao clicar em um link
    linksMenu.forEach((link) => {
        link.addEventListener("click", () => {
            document.body.classList.remove("sidebar-open");
            botaoMenu.setAttribute("aria-expanded", "false");
        });
    });

    // Fecha o menu ao clicar fora dele
    document.addEventListener("click", (evento) => {

        const clicouNoMenu = menuLateral.contains(evento.target);
        const clicouNoBotao = botaoMenu.contains(evento.target);

        if (
            document.body.classList.contains("sidebar-open") &&
            !clicouNoMenu &&
            !clicouNoBotao
        ) {
            document.body.classList.remove("sidebar-open");
            botaoMenu.setAttribute("aria-expanded", "false");
        }
    });

    // Fecha o menu ao voltar para uma tela maior
    window.addEventListener("resize", () => {
        if (window.innerWidth > 768) {
            document.body.classList.remove("sidebar-open");
            botaoMenu.setAttribute("aria-expanded", "false");
        }
    });
}


// ==========================================
// PESQUISA DE CLIENTES
// ==========================================

const pesquisaCliente = document.getElementById("pesquisaCliente");
const tabelaClientes = document.getElementById("tabelaClientes");

if (pesquisaCliente && tabelaClientes) {

    // Obtém as linhas que representam clientes
    const linhas = Array.from(
        tabelaClientes.querySelectorAll("tr")
    ).filter(linha => !linha.querySelector(".empty-message"));

    pesquisaCliente.addEventListener("input", function () {

        // Obtém o texto digitado
        const termo = pesquisaCliente.value
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .trim();

        let resultadosEncontrados = 0;

        // Percorre todos os clientes
        linhas.forEach(linha => {

            const textoCliente = linha.textContent
                .toLowerCase()
                .normalize("NFD")
                .replace(/[\u0300-\u036f]/g, "");

            // Verifica se o cliente corresponde à pesquisa
            if (textoCliente.includes(termo)) {

                linha.style.display = "";
                resultadosEncontrados++;

            } else {

                linha.style.display = "none";

            }

        });

        // Gerencia a mensagem de pesquisa sem resultados
        let mensagem = tabelaClientes.querySelector(".no-results-row");

        if (resultadosEncontrados === 0 && linhas.length > 0) {

            if (!mensagem) {

                mensagem = document.createElement("tr");
                mensagem.classList.add("no-results-row");

                mensagem.innerHTML = `
                    <td colspan="5" class="empty-message">
                        Nenhum cliente encontrado.
                    </td>
                `;

                tabelaClientes.appendChild(mensagem);
            }

        } else if (mensagem) {

            mensagem.remove();

        }

    });

}