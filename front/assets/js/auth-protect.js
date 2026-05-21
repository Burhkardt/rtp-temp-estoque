// auth-protect.js — protege páginas restritas verificando token no início
(function () {
  // Checa se há token válido no localStorage
  const token = localStorage.getItem("token");

  if (!token) {
    try {
      // Limpa qualquer resíduo de autenticação
      localStorage.clear();
      sessionStorage.clear();
    } catch (e) {}

    // Redireciona para a tela de login substituindo histórico (impede voltar)
    window.location.replace("../../../index.html");
    return;
  }

  // Evita que a página fique acessível via botão 'Voltar' após logout
  // (adiciona um estado extra e bloqueia popstate para este comportamento)
  try {
    history.pushState(null, document.title, location.href);
    window.addEventListener("popstate", function () {
      // Se o token sumir por algum motivo, força redirect
      const t = localStorage.getItem("token");
      if (!t) {
        window.location.replace("../../../index.html");
        return;
      }
      history.pushState(null, document.title, location.href);
    });
  } catch (e) {}
})();
