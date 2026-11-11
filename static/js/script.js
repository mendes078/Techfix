
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