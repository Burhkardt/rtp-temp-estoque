function carregarNavbar() {
  fetch("../navbar/navbar.html")
    .then((res) => res.text())
    .then((html) => {
      document.getElementById("espaco-da-navbar").innerHTML = html;

      // Marca o link ativo com base na URL atual
      const paginaAtual = window.location.pathname
        .split("/")
        .pop()
        .replace(".html", "");
      document.querySelectorAll(".nav-link[data-page]").forEach((link) => {
        if (link.dataset.page === paginaAtual) {
          link.classList.add("active");
        }
      });

      // Controle de acesso por perfil
      const perfil = sessionStorage.getItem("usuario_perfil") || "";
      if (perfil.toLowerCase() !== "admin") {
        document.querySelectorAll('[data-role="admin-only"]').forEach((el) => {
          el.style.display = "none";
        });
      }

      // Botão Sair: limpa credenciais e redireciona usando replace (impede voltar)
      const btnSair = document.getElementById("btn-sair");
      if (btnSair) {
        btnSair.addEventListener("click", (e) => {
          e.preventDefault();
          try {
            localStorage.clear();
            sessionStorage.clear();
          } catch (err) {}
          // redireciona para a tela de login usando replace (não adiciona ao histórico)
          window.location.replace("../../../index.html");
        });
      }
    })
    .catch((err) => console.error("Erro ao carregar navbar:", err));
}

carregarNavbar();
