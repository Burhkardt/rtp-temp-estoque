// ============================================================
// USUÁRIOS LOCAIS
// ============================================================

const usuarios = [
  {
    cpf: "12345678900",
    senha: "1234",
    nome: "Administrador",
    perfil: "admin",
  },
  // {
  //     cpf: "11111111111",
  //     senha: "teste",
  //     nome: "Usuário Teste",
  //     perfil: "usuario"
  // }
];

// ============================================================
// LOADING + LOGIN
// ============================================================

document.addEventListener("DOMContentLoaded", () => {
  // ============================================================
  // TRANSIÇÃO LOADING
  // ============================================================

  setTimeout(() => {
    const loadingScreen = document.getElementById("loading-screen");

    const loginScreen = document.getElementById("login-screen");

    loadingScreen.style.opacity = "0";

    setTimeout(() => {
      loadingScreen.style.display = "none";

      loginScreen.style.display = "block";

      document.body.style.overflow = "auto";
    }, 500);
  }, 2500);

  // ============================================================
  // APENAS NÚMEROS NO CPF
  // ============================================================

  const camposNumeros = document.querySelectorAll(".apenas-numeros");

  camposNumeros.forEach((campo) => {
    campo.addEventListener("input", (event) => {
      event.target.value = event.target.value.replace(/\D/g, "");
    });
  });

  // ============================================================
  // FORMULÁRIO LOGIN
  // ============================================================

  const formulario = document.getElementById("form-acesso");

  formulario.addEventListener("submit", function (evento) {
    evento.preventDefault();

    // ============================================================
    // CAPTURA DADOS
    // ============================================================

    const email = document.getElementById("inputEmail").value;

    const senha = document.getElementById("inputSenha").value;

    // ============================================================
    // BOTÃO
    // ============================================================

    const botaoLogin = formulario.querySelector("button");

    botaoLogin.disabled = true;

    botaoLogin.innerText = "Entrando...";

    // ============================================================
    // CHAMA API DE LOGIN (BACKEND)
    // ============================================================

    const payload = {
      username: email,
      password: senha,
    };

    fetch("http://localhost:5000/api/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    })
      .then(async (res) => {
        if (!res.ok) {
          let err = { erro: "Erro no login" };
          try {
            err = await res.json();
          } catch (e) {}
          alert(err.erro || "CPF ou senha inválidos!");
          return;
        }

        const data = await res.json();
        const token = data.token;

        if (token) {
          localStorage.setItem("token", token);
          localStorage.setItem(
            "usuario",
            JSON.stringify({ nome: "Administrador", perfil: "admin" }),
          );

          alert("Login realizado com sucesso!");
          window.location.href = "assets/pages/produtos/produtos.html";
        } else {
          alert("Resposta inesperada do servidor.");
        }
      })
      .catch((err) => {
        console.error(err);
        alert("Erro de conexão com o servidor.");
      })
      .finally(() => {
        // ============================================================
        // REATIVA BOTÃO
        // ============================================================
        botaoLogin.disabled = false;
        botaoLogin.innerText = "Acessar";
      });

    // ============================================================
    // REATIVA BOTÃO
    // ============================================================

    botaoLogin.disabled = false;

    botaoLogin.innerText = "Acessar";
  });
});
